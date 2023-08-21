import os
from typing import List, Dict, Tuple
import pandas as pd
import xgboost as xgb
import json
from ..data_handling.dataframes_handling import add_odds_pred

# Paths
script_dir = os.path.dirname(__file__)
rel_path_models = "../../data/models"
abs_path_models = os.path.join(script_dir, rel_path_models)
rel_path_current_model = "../../data/temporary_storage/current_model.json"
abs_path_current_model = os.path.join(script_dir, rel_path_current_model)
rel_path_current_model_parameters = (
    "../../data/temporary_storage/current_model_parameters.json"
)
abs_path_current_model_parameters = os.path.join(
    script_dir, rel_path_current_model_parameters
)
rel_path_prepared_data = "../../data/prepared_data"
abs_path_prepared_data = os.path.join(script_dir, rel_path_prepared_data)

# Body


def load_model(name: str) -> xgb.XGBClassifier:
    # ternary operator for path
    path = (
        abs_path_current_model
        if (name == "current_model")
        else abs_path_models + "/" + name + "/model.json"
    )

    ## Check that path is a json file and exists
    if not os.path.exists(path):
        raise ValueError("Path does not exist, {}".format(path))
    if not path.endswith(".json"):
        raise ValueError("Path must be a json file")

    clf = xgb.XGBClassifier()
    xgb.XGBClassifier.load_model(clf, path)  # type: ignore
    return clf


# Note: model_name "current_model" is a special case
# Returns a dictionary of dataframes, key "PL2122" etc.
# FIXME: y_pars


def apply_model(model_name: str, data_list: List[str]) -> Dict[str, pd.DataFrame]:
    classifier = load_model(model_name)
    [xPar, yPar] = load_x_and_y_parameters_from_model(model_name)  # type: ignore

    df_dict: Dict[str, pd.DataFrame] = {}
    for df_name in data_list:
        if df_name.endswith(".csv"):
            df_name = df_name[:-4]
        if not os.path.exists(abs_path_prepared_data + "/" + df_name + ".csv"):
            raise ValueError("Dataframe does not exist")
        df = pd.read_csv(abs_path_prepared_data + "/" + df_name + ".csv")  # type: ignore
        df["prediction"] = classifier.predict(df[xPar])  # type: ignore
        df["prob_0"] = classifier.predict_proba(df[xPar])[:, 0]  # type: ignore
        df["prob_1"] = classifier.predict_proba(df[xPar])[:, 1]  # type: ignore
        df = add_odds_pred(df, "AvgO25", "AvgU25")
        df_dict[df_name] = df

    return df_dict


def apply_model_to_df(model_name: str, df: pd.DataFrame) -> pd.DataFrame:
    classifier = load_model(model_name)
    [xPar, yPar] = load_x_and_y_parameters_from_model(model_name)  # type: ignore

    df["prediction"] = classifier.predict(df[xPar])  # type: ignore
    df["prob_0"] = classifier.predict_proba(df[xPar])[:, 0]  # type: ignore
    df["prob_1"] = classifier.predict_proba(df[xPar])[:, 1]  # type: ignore
    df = add_odds_pred(df, "AvgO25", "AvgU25")

    return df


# Tuple[x_pars, y_par]
def load_x_and_y_parameters_from_model(model_name: str) -> Tuple[List[str], str]:
    # ternary operator for path
    path = (
        abs_path_current_model_parameters
        if (model_name == "current_model")
        else abs_path_models + "/" + model_name + "/model_parameters.json"
    )
    if not os.path.exists(path):
        raise ValueError("Path does not exist")

    # Load json from path
    with open(path, "r") as f:
        json_dict = json.load(f)
    x_pars = json_dict["xParameters"]
    y_par = json_dict["yParameter"]
    return (x_pars, y_par)


def load_training_data_from_model(model_name: str) -> List[str]:
    # ternary operator for path
    path = (
        abs_path_current_model_parameters
        if (model_name == "current_model")
        else abs_path_models + "/" + model_name + "/model_parameters.json"
    )
    if not os.path.exists(path):
        raise ValueError("Path does not exist")

    # Load json from path
    with open(path, "r") as f:
        json_dict = json.load(f)
    training_data = json_dict["trainingData"]
    return training_data
