from typing import Dict, Any
import pandas as pd
from ..data_handling.data_handling_utils import get_prepared_data
from .train_model_utils import sample_ML_data, 
#train_XGB, model_statistics



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
    all_dataframes = [key for key in df_dict]


    train, test, val = sample_ML_data(
        dataframes_dict=df_dict,
        sample_dataframes=all_dataframes,
        fraction_test=0.2,
        fraction_val=0.15,
        train_dataframes=arguments["train_dataframes"],
        test_dataframes=arguments["test_dataframes"],
        val_dataframes=arguments["val_dataframes"],
        seed=seed,
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
