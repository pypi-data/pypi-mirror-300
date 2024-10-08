from io import BytesIO
import logging
import os
import shutil
from importlib.util import spec_from_file_location, module_from_spec
import sys
import uuid

from dpt import Project
import pymongo
from pymongo.database import Database
from dpt.mongo.commands import upsert_one_with_timestamp
from dpt.mongo.files import delete_file, upload_file
from dpt.processor import Port
from dpt.deployment.common import coll_prefix
from dpt.deployment import common

_logger = logging.getLogger(__name__)


def _dict_from_obj(obj):
    dict = {}
    for name in dir(obj):
        if not name.startswith("_"):
            val = getattr(obj, name)
            if isinstance(val, (str, bool)):
                dict[name] = val
    return dict


def remove_deployment(project_name):
    _logger.info(f"Remove deployment: start")
    client = pymongo.MongoClient(common.mongo_uri)
    db = client[common.sys_db_name]
    collection = db[f"{coll_prefix}project"]
    filter = {
        "name": project_name,
        "workspace": common.workspace_name,
    }
    for doc in collection.find(filter):
        old_file_id = doc["file_id"]
        delete_file(old_file_id, db)

    collection.delete_many(filter)
    filter = {
        "project": project_name,
        "workspace": common.workspace_name,
    }
    db[f"{coll_prefix}module"].delete_many(filter)
    db[f"{coll_prefix}processor"].delete_many(filter)
    _logger.info(f"Remove deployment: success")


def get_metadata(db: Database, workspace_name, project_name) -> dict:

    project_info = db[f"{coll_prefix}project"].find_one(
        {
            "name": project_name,
            "workspace": workspace_name,
        }
    )
    del project_info["_id"]
    del project_info["changed_at"]
    del project_info["file_id"]

    return {
        "project_info": project_info,
        "modules_info": _get_modules_info(db, project_name, workspace_name),
        "processors_info": _get_processors_info(db, project_name, workspace_name),
    }


def _prepare_metadata(
    project: Project, main_file_path, main_func_name, temp_path
) -> dict:
    version_info = _get_version_info()
    project_info = _dict_from_obj(project)
    project_info.update(
        {
            "published_by": os.getlogin(),
            "version_info": version_info,
            "main_file_path": main_file_path,
            "main_func_name": main_func_name,
        }
    )
    return {
        "project_info": project_info,
        "modules_info": _prepare_modules_info(project, temp_path, version_info),
        "processors_info": _prepare_processors_info(project, temp_path, version_info),
    }


def save_project(db: Database, archive_data: BytesIO, metadata: dict, workspace_name):
    project_info: dict = metadata["project_info"]
    project_name = project_info["name"]
    collection = db[f"{coll_prefix}project"]
    file_id = upload_file(archive_data, db)
    filter = {
        # "name": project_name,
        "workspace": workspace_name,
    }
    for doc in collection.find(filter):
        old_file_id = doc["file_id"]
        delete_file(old_file_id, db)

    project_info.update(
        {
            "file_id": file_id,
            "deployment_id": str(uuid.uuid4()),
            "workspace": workspace_name,
        }
    )

    upsert_one_with_timestamp(
        collection,
        filter,
        project_info,
    )
    # _update_metadata(db, project_name, metadata)
    _update_modules_info(db, project_name, workspace_name, metadata["modules_info"])
    _update_processors_info(
        db, project_name, workspace_name, metadata["processors_info"]
    )


def upload_project(
    archive_path,
    project: Project,
    main_file_path,
    main_func_name,
    temp_path,
):
    _logger.info(f"Upload project: start")
    client = pymongo.MongoClient(common.mongo_uri)
    db = client[common.sys_db_name]
    collection = db[f"{coll_prefix}project"]
    archive_data = open(archive_path, "rb")
    filter = {
        "name": project.name,
        "workspace": common.workspace_name,
    }
    for doc in collection.find(filter):
        old_file_id = doc["file_id"]
        delete_file(old_file_id, db)
    metadata = _prepare_metadata(project, main_file_path, main_func_name, temp_path)
    save_project(db, archive_data, metadata, common.workspace_name)
    client.close()
    project_info = metadata["project_info"]
    _logger.info(f"Upload project: success")
    _logger.info(f"- {project_info}")


def _normalize_def_in_file(info: dict, root_path, version_info):
    if version_info != None:
        path = (
            os.path.relpath(info["defined_in_file"], start=version_info["git_dir"])
            .replace("\\", "/")
            .replace("../", "")
        )
        info["defined_in_file"] = path


def _prepare_modules_info(project: Project, temp_path: str, version_info):
    info_list = []
    for module in project.modules.values():
        info = _dict_from_obj(module)
        info.update(
            {
                "workspace": common.workspace_name,
                "project": project.name,
            }
        )
        _normalize_def_in_file(info, temp_path, version_info)
        info_list.append(info)
    return info_list


def _update_modules_info(db: Database, project_name, workspace_name, info_list):
    collection = db[f"{coll_prefix}module"]

    for item in info_list:
        item["workspace"] = workspace_name

    collection.delete_many(
        {
            # "project": project_name,
            "workspace": workspace_name,
        }
    )
    collection.insert_many(info_list)


def _get_modules_info(db: Database, project_name, workspace_name):
    collection = db[f"{coll_prefix}module"]

    result = list(
        collection.find(
            {
                "project": project_name,
                "workspace": workspace_name,
            }
        )
    )
    for item in result:
        del item["_id"]
    return result


# def _update_metadata(db: Database, project_name, metadata: dict):
#     collection = db[f"{coll_prefix}metadata"]
#     collection.delete_many(
#         {
#             "project": project_name,
#             "workspace": common.workspace_name,
#         }
#     )
#     collection.insert_one(metadata)


def _prepare_processors_info(project: Project, temp_path: str, version_info):
    info_list = []
    for module in project.modules.values():
        for processor in module.processors.values():
            info = _dict_from_obj(processor)

            info.update(
                {
                    "workspace": common.workspace_name,
                    "project": project.name,
                    "module": module.name,
                    "source_link": "",
                }
            )

            _normalize_def_in_file(info, temp_path, version_info)
            if version_info != None:
                repo: str = version_info["repository"]

                suffix = ".git"
                if repo.endswith(suffix):
                    repo = repo[: -len(suffix)]

                repo_root = "http://gl.astu.lan/"
                repo_without_root = repo.replace(repo_root, "")

                # TODO усовершенствовать алгоритм определения ссылки вынести в настройки частично
                link = f"{repo_root}-/ide/project/{repo_without_root}/edit/{version_info['branch']}/-/{info['defined_in_file']}"

                info.update(
                    {
                        "source_link": link,
                    }
                )

            def make_port_info(ports: dict[str, Port]):
                ports_info = []
                for port in ports.values():
                    if port.name == "статистика":
                        pass
                    port_info = _dict_from_obj(port)
                    # TODO Enum не вписался в этот подход _dict_from_obj, переделать если будем развивать
                    if port.collection_type != None:
                        port_info["collection_type"] = port.collection_type.value

                    ports_info.append(port_info)
                    port_info["data_schema"] = port.schema
                return ports_info

            info["inputs"] = make_port_info(processor.inputs)
            info["outputs"] = make_port_info(processor.outputs)

            # info["temp_path"] = temp_path
            info_list.append(info)
    return info_list


def _update_processors_info(db: Database, project_name, workspace_name, info_list):
    collection = db[f"{coll_prefix}processor"]

    for item in info_list:
        item["workspace"] = workspace_name

    collection.delete_many(
        {
            # "project": project_name,
            "workspace": workspace_name,
        }
    )
    collection.insert_many(info_list)


def _get_processors_info(db: Database, project_name, workspace_name):
    collection = db[f"{coll_prefix}processor"]

    result = list(
        collection.find(
            {
                "project": project_name,
                "workspace": workspace_name,
            }
        )
    )
    for item in result:
        del item["_id"]
    return result


def _get_version_info():
    _logger.info("Get version info: start")
    try:
        import git

        repo = git.Repo(search_parent_directories=True)
        version_info = {
            "repository": repo.remotes.origin.url,
            "branch": repo.active_branch.name,
            "commit": repo.head.commit.hexsha,
            "is_dirty": bool(repo.is_dirty()),
            "git_dir": repo.git_dir,
        }
    except:
        _logger.info("Get version info: git repository not found")  # todo не проверено
        return None
    if version_info != None:
        _logger.info("Get version info: success")
        _logger.info(version_info)
    return version_info


def make_archive(temp_path, project_name):
    _logger.info("Make archive: start")
    archive_path = os.path.join(
        os.path.dirname(temp_path), "df_prep_projects", f"{project_name}"
    )
    archive_path_ext = archive_path + ".zip"
    if os.path.isfile(archive_path):
        os.remove(archive_path)
    for dirpath, dirnames, filenames in os.walk(temp_path):
        for dirname in dirnames:
            if dirname == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, dirname))
    shutil.make_archive(archive_path, "zip", temp_path)
    shutil.rmtree(temp_path)
    _logger.info("Make archive: success")
    _logger.info(f"- temp dir path: {archive_path_ext}")
    return archive_path_ext


def copy_files_to_temp_dir(root_path, include: list[str] = None):
    _logger.info("Collect source files: start")
    temp_path = os.path.join(root_path, "build", "df_prep_temp")

    if os.path.isdir(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)

    if include == None:
        include = os.listdir(root_path)

    for item in include:
        src_path = os.path.join(root_path, item)
        trg_path = os.path.join(temp_path, item)
        if os.path.isdir(src_path):
            shutil.copytree(
                src_path,
                trg_path,
                ignore=shutil.ignore_patterns("__pycache__", "build"),
            )
        else:
            os.makedirs(os.path.dirname(trg_path), exist_ok=True)
            shutil.copy(src_path, trg_path)
    _logger.info("Collect source files: success")
    _logger.info(f"- temp dir path: {temp_path}")
    return temp_path


def _run_function(root_path, file_path, func_name="main"):
    if root_path not in sys.path:
        sys.path.append(root_path)
    file_full_path = os.path.join(root_path, file_path)
    spec = spec_from_file_location("module", file_full_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    func = getattr(module, func_name)
    return func()


def run_main_function(tmp_path, main_file_path, main_func_name):
    _logger.info("Build project: start")
    project: Project = _run_function(tmp_path, main_file_path, main_func_name)
    if not isinstance(project, Project):
        raise Exception(
            f"Main function '{main_func_name}' should return instance of 'df_prep.Project' class"
        )
    _logger.info("Build project: success")
    _logger.info(f"- project: {project.name}")
    for module_name in project.modules:
        module = project.modules[module_name]
        _logger.info(f"- - module: {module.name}")
        for proc_name in module.processors:
            _logger.info(f"- - - processor: {proc_name}")
    return project
