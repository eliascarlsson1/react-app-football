import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..data_handling.database_con import get_model_names
from ..data_handling.data_handling_utils import get_historical_data_list
from .apply_model_utils import (
    load_x_and_y_parameters_from_model,
    load_training_data_from_model,
    load_model,
)
from ..data_handling.data_handling_utils import (
    get_prepared_data_dict,
    concatenate_df_dict,
)
from eli5.sklearn import PermutationImportance
import xgboost as xgb


def generate_model_statistics(model_name: str, test_data_list: list[str]):
    model_names = get_model_names()
    if model_name not in model_names:
        print("Error: model name not found")
        return

    df_dict: dict[str, pd.DataFrame] = get_prepared_data_dict()

    training_data_list = load_training_data_from_model(model_name)
    training_data = concatenate_df_dict(df_dict, training_data_list)

    all_data_list = get_historical_data_list()
    ## Val data list is all data list minus trainning and test data list
    val_data_list = [
        x
        for x in all_data_list
        if x not in training_data_list and x not in test_data_list
    ]
    val_data = concatenate_df_dict(df_dict, val_data_list)

    test_data = concatenate_df_dict(df_dict, test_data_list)
    [x_par, y_par] = load_x_and_y_parameters_from_model(model_name)
    model = load_model(model_name)

    model_statistics(model, training_data, test_data, val_data, x_par, y_par)
    # feature_selection(model, test_data, x_par, y_par)
    # feature_importance_RF(model, x_par)


def model_statistics(
    classifier: xgb.XGBClassifier,
    train: pd.DataFrame,
    test: pd.DataFrame,
    val: pd.DataFrame,
    x_par: list[str],
    y_par: str,
):
    # Print accuracy
    print(
        "Training data accuracy: "
        + str(round(classifier.score(train[x_par], train[y_par]) * 100, 1))  # type: ignore
    )
    print(
        "Test data accuracy: "
        + str(round(classifier.score(test[x_par], test[y_par]) * 100, 1))  # type: ignore
    )
    print(
        "Validation data accuracy: "
        + str(round(classifier.score(val[x_par], val[y_par]) * 100, 1))  # type: ignore
    )


# def feature_importance_RF(classifier: xgb.XGBClassifier, x_par: list[str]):
#     # Plot importance
#     importances = classifier.feature_importances_ # type: ignore
#     std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0) # type: ignore

#     forest_importances = pd.Series(importances, index=x_par) # type: ignore

#     fig, ax = plt.subplots() # type: ignore
#     forest_importances.plot.bar(yerr=std, ax=ax) # type: ignore
#     ax.set_title("Feature importances using MDI") # type: ignore
#     ax.set_ylabel("Mean decrease in impurity") # type: ignore
#     fig.tight_layout()


# def feature_selection(classifier: xgb.XGBClassifier, test: pd.DataFrame, x_par: list[str], y_par: str):
#     permuter = PermutationImportance(
#         classifier, scoring="accuracy", n_iter=5, random_state=42
#     )

#     permuter.fit(test[x_par], test[y_par]) # type: ignore

#     return permuter

### OLD SCRIPT!
# import pandas as pd
# import numpy as np
# import xgboost as xgb
# from sklearn.inspection import permutation_importance
# from matplotlib import pyplot as plt
# from matplotlib import pyplot

# # Reading files
# parameters = pd.read_json("./interface_files/prediction_parameters.json", typ="series")

# path = "./interface_files/"
# model_parameters = pd.read_json(path + "current_model_parameters.json", typ = "series")
# x_par = np.array(model_parameters["x_par"])
# y_par = model_parameters["y_par"]
# train = pd.read_csv(path+"current_val.csv")

# clf = xgb.XGBClassifier()
# xgb.XGBClassifier.load_model(clf, path+"current_model.json")


# plt.clf()
# perm_importance = permutation_importance(clf, train[x_par], train[y_par])
# sorted_idx = perm_importance.importances_mean.argsort()
# plt.barh(x_par[sorted_idx], perm_importance.importances_mean[sorted_idx])
# plt.xlabel("Permutation Importance")
# plt.savefig("./interface_files/current_perumtation_importance.png")

# plt.clf()
# xgb.plot_importance(clf)
# pyplot.savefig("./interface_files/current_feature_importance.png")
