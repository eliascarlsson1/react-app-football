import shutil
from typing import List, Dict, Any
from ..data_handling.database_con import (
    get_model_names,
    add_delete_model,
    add_test,
    get_test_names,
)
from .apply_model_utils import (
    load_x_and_y_parameters_from_model,
    load_training_data_from_model,
)
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


def get_model_information():
    if not ensure_save_models_to_database():
        raise Exception("Error: models folder and database are not in sync")

    model_information: List[Dict[str, Any]] = []
    model_names = get_model_names()

    for name in model_names:
        model_information.append(
            {
                "name": name,
                "xParameters": load_x_and_y_parameters_from_model(name)[0],
                "yParameter": load_x_and_y_parameters_from_model(name)[1],
                "trainingData": load_training_data_from_model(name),
            }
        )

    return model_information


def save_test(filterData: Any):
    # 'filterData':
    # {'odds': [number, number],
    # 'testName: string,
    # 'confidenceOverOdds': [number, number],
    # 'probability': [int, int],
    # 'outcome': [0, 1, ...]}}

    # FIXME: Test all parameters, so that they are as expected, especially outcome, array...
    odds_high = float(filterData["odds"][1])
    odds_low = float(filterData["odds"][0])
    confidence_over_odds_high = float(filterData["confidenceOverOdds"][1])
    confidence_over_odds_low = float(filterData["confidenceOverOdds"][0])
    probability_high = int(filterData["probability"][1])
    probability_low = int(filterData["probability"][0])
    outcome = ",".join(filterData["outcome"])
    testName = filterData["testName"]

    if testName in get_test_names():
        print(testName)
        if  testName != "current":
            return "Error: test name already exists"

    add_test(
        testName,
        odds_high,
        odds_low,
        confidence_over_odds_high,
        confidence_over_odds_low,
        probability_high,
        probability_low,
        outcome,
    )
    return "success"
