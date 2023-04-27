from typing import Dict, Any
import pandas as pd
from ..data_handling.data_handling_utils import get_prepared_data, concatenate_df_dict
#from .train_model_utils import train_XGB, model_statistics



def train_model(parameters: Dict[str, Any]) -> None:
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

    ## FIXME: This should be done somehwer else, preparing for the data
    # data = data.assign(OvUn=[">2.5" if TG > 2.5 else "<2.5" for TG in data["TG"]]) # type: ignore
    # data = data.assign(OvUnB=[1 if TG > 2.5 else 0 for TG in data["TG"]]) # type: ignore
    # data = data.assign( # type: ignore
    #     FTRB=[0 if FTR == "H" else 1 if FTR == "D" else 2 for FTR in data["FTR"]] # type: ignore
    # )
    # data = data.dropna() # type: ignore


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
        seed=seed,
    )

    model_statistics(xgb, train, val, test, x_par, "OvUnB")

    for df in [train, test, val]:
        df["prediction"] = xgb.predict(df[x_par])
        df["prob_0_xgb"] = [proba[0] for proba in xgb.predict_proba(df[x_par])]
        df["prob_1_xgb"] = [proba[1] for proba in xgb.predict_proba(df[x_par])]
        if len(df[y_par].unique()) == 3:
            df["prob_2_xgb"] = [proba[2] for proba in xgb.predict_proba(df[x_par])]

    train.to_csv("./interface_files/current_train.csv")
    test.to_csv("./interface_files/current_test.csv")
    val.to_csv("./interface_files/current_val.csv")
    xgb.save_model("./interface_files/current_model.json")
