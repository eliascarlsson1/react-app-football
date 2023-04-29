import shutil
from ..data_handling.database_con import get_model_names, add_delete_model
import os

script_dir = os.path.dirname(__file__)
temporary_relative_path = "../../data/temporary_storage"
models_relative_path = "../../data/models"
temporary_storage_path = os.path.join(script_dir, temporary_relative_path)
models_path = os.path.join(script_dir, models_relative_path)


def save_model(name: str) -> str:
    if not ensure_save_models_to_database():
        raise Exception("Error: models folder and database are not in sync")

    names = get_model_names()
    if name in names:
        return "Error: model name already exists"

    os.mkdir(models_path + "/" + name)
    # Copy files from temporary storage to models folder
    shutil.copy(
        temporary_storage_path + "/current_model.json",
        models_path + "/" + name + "/model.json",
    )
    shutil.copy(
        temporary_storage_path + "/current_model_parameters.json",
        models_path + "/" + name + "/model_parameters.json",
    )
    add_delete_model(True, name)
    return "success"


def delete_model(name: str) -> str:
    if not ensure_save_models_to_database():
        raise Exception("Error: models folder and database are not in sync")

    names = get_model_names()
    if name not in names:
        return "Error: model name does not exist"

    shutil.rmtree(models_path + "/" + name)
    add_delete_model(False, name)
    return "success"


def ensure_save_models_to_database() -> bool:
    database_names = get_model_names()
    path_names = os.listdir(models_path)

    if len(database_names) != len(path_names):
        return False

    for name in database_names:
        if name not in path_names:
            return False

    for name in path_names:
        if name not in database_names:
            return False

    return True
