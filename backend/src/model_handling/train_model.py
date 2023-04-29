from typing import Dict, Any, List
import os
import shutil
import pandas as pd
from ..data_handling.data_handling_utils import (
    get_prepared_data_dict,
    concatenate_df_dict,
    get_is_all_relevant_data_prepared,
)
from ..data_handling.database_con import get_model_names, add_delete_model
from .train_model_utils import train_XGB, save_model_parameters
from ..error_handling.error_utils import is_non_empty_string_list

script_dir = os.path.dirname(__file__)
temporary_relative_path = "../../data/temporary_storage"
models_relative_path = "../../data/models"
temporary_storage_path = os.path.join(script_dir, temporary_relative_path)
models_path = os.path.join(script_dir, models_relative_path)


def train_model(parameters: Dict[str, Any]) -> str:
    """
    parameters (Dict[str, Any]): A dictionary containing the following keys:
        - type (str): 'train model'
        - trainingData (List[any]):
        - xParameters (List[str]):
        - yParameter (List[str]):
        - learningRate (float):
        - maxDepth (int):
        - numberEstimators (int):
    """
    ## Check that all variables are as expected
    training_data: List[str] = parameters["trainingData"]
    if not is_non_empty_string_list(training_data):
        return "Error: trainingData is not a list of strings"

    x_par: List[str] = parameters["xParameters"]
    if not is_non_empty_string_list(x_par):
        return "Error: xParameters is not a list of strings"

    y_par = parameters["yParameter"]
    if not isinstance(y_par, str):
        return "Error: yParameter is not a string"

    learning_rate = parameters["learningRate"]
    if not isinstance(learning_rate, float):
        return "Error: learningRate is not a float"

    max_depth = parameters["maxDepth"]
    if not isinstance(max_depth, int):
        return "Error: maxDepth is not an int"

    n_estimators = parameters["numberEstimators"]
    if not isinstance(n_estimators, int):
        return "Error: numberEstimators is not an int"

    ## Function

    df_dict: dict[str, pd.DataFrame] = get_prepared_data_dict()

    if not get_is_all_relevant_data_prepared():
        return "Error: not all relevant data is prepared"
    train = concatenate_df_dict(dataframes_dict=df_dict, to_concatenate=training_data)

    # Check that x and y parameters are in the dataframe
    for par in x_par:
        if par not in train.columns:
            return "Error: xParameter not in dataframe"

    if y_par not in train.columns:
        return "Error: yParameter not in dataframe"

    xgb = train_XGB(
        train=train,
        x_par=x_par,
        y_par=y_par,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
    )

    xgb.save_model(temporary_storage_path + "/current_model.json")

    save_model_parameters(
        train=training_data,
        x_par=x_par,
        y_par=y_par,
        path=temporary_storage_path,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
    )

    return "success"


def save_model(name:str) -> str:
    if (not ensure_save_models_to_database()):
        raise Exception("Error: models folder and database are not in sync")
    
    names = get_model_names()
    if name in names:
        return "Error: model name already exists"
    
    os.mkdir(models_path + "/" + name)
    # Copy files from temporary storage to models folder
    shutil.copy(temporary_storage_path + "/current_model.json", models_path + "/" + name + "/current_model.json")
    shutil.copy(temporary_storage_path + "/current_model_parameters.json", models_path + "/" + name + "/model_parameters.json")
    add_delete_model(True, name)
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