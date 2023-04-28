from typing import Dict, Any
import pandas as pd
from ..data_handling.data_handling_utils import get_prepared_data, concatenate_df_dict
from .train_model_utils import train_XGB



def train_model(parameters: Dict[str, Any]) -> str:
    """
    parameters (Dict[str, Any]): A dictionary containing the following keys:
        - type (str): 'train model'
        - trainingData (List[any]):
        - testData (List[any]):
        - evaluateSplit (bool):
        - xParameters (List[str]):
        - yParameters (List[str]):
        - learningRate (float):
        - maxDepth (int):
        - numberEstimators (int):
    """  

    df_dict: dict[str, pd.DataFrame] = get_prepared_data()

    train = concatenate_df_dict(
        dataframes_dict=df_dict,
        to_concatenate=parameters["testData"]
    )

    x_par = parameters["x_par"]
    y_par = parameters["y_par"]
    n_estimators = parameters["n_estimators"]
    learning_rate = parameters["learning_rate"]
    max_depth = parameters["max_depth"]


    xgb = train_XGB(
        train=train,
        x_par=x_par,
        y_par=y_par,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
    )

    xgb.save_model("./current_model.json")

    return "Success"
