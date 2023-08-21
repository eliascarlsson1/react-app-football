import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Use the 'Agg' backend (non-GUI)
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
from sklearn.inspection import permutation_importance  # type: ignore
import xgboost as xgb
import os

relative_image_path = "../../data/temporary_storage/images"
file_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(file_path, relative_image_path)


def generate_model_statistics(model_name: str, test_data_list: list[str]) -> list[str]:
    # Generated plots and returns accuracy list
    model_names = get_model_names()
    if model_name not in model_names:
        print("Error: model name not found")
        return []

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

    feature_importance(model, training_data, test_data, val_data, x_par, y_par)
    probability_histogram_plot(model, training_data, test_data, val_data, x_par, y_par)
    return model_statistics(model, training_data, test_data, val_data, x_par, y_par)


def model_statistics(
    classifier: xgb.XGBClassifier,
    train: pd.DataFrame,
    test: pd.DataFrame,
    val: pd.DataFrame,
    x_par: list[str],
    y_par: str,
) -> list[str]:
    # Print accuracy
    accuracy_list: list[str] = []

    accuracy_list.append(  # type: ignore
        "Training data accuracy: "
        + str(round(classifier.score(train[x_par], train[y_par]) * 100, 1))  # type: ignore
    )
    accuracy_list.append(  # type: ignore
        "Test data accuracy: "
        + str(round(classifier.score(test[x_par], test[y_par]) * 100, 1))  # type: ignore
    )

    accuracy_list.append(  # type: ignore
        "Validation data accuracy: "
        + str(round(classifier.score(val[x_par], val[y_par]) * 100, 1))  # type: ignore
    )

    return accuracy_list


def feature_importance(
    classifier: xgb.XGBClassifier,
    train: pd.DataFrame,
    test: pd.DataFrame,
    val: pd.DataFrame,
    x_par: list[str],
    y_par: str,
):
    ## FIXME: Make for validation and test!!
    perm_importance = permutation_importance(classifier, train[x_par], train[y_par])
    sorted_idx = perm_importance.importances_mean.argsort()  # type: ignore
    xp_par_array = np.array(x_par)
    plt.barh(xp_par_array[sorted_idx], perm_importance.importances_mean[sorted_idx])  # type: ignore
    plt.xlabel("Permutation Importance " + "Training data")  # type: ignore
    plt.savefig(image_path + "/permutation_importance_training.png")  # type: ignore
    plt.close()  # type: ignore

    perm_importance = permutation_importance(classifier, test[x_par], test[y_par])
    sorted_idx = perm_importance.importances_mean.argsort()  # type: ignore
    xp_par_array = np.array(x_par)
    plt.barh(xp_par_array[sorted_idx], perm_importance.importances_mean[sorted_idx])  # type: ignore
    plt.xlabel("Permutation Importance " + "Test data")  # type: ignore
    plt.savefig(image_path + "/permutation_importance_test.png")  # type: ignore
    plt.close()  # type: ignore

    perm_importance = permutation_importance(classifier, val[x_par], val[y_par])
    sorted_idx = perm_importance.importances_mean.argsort()  # type: ignore
    xp_par_array = np.array(x_par)
    plt.barh(xp_par_array[sorted_idx], perm_importance.importances_mean[sorted_idx])  # type: ignore
    plt.xlabel("Permutation Importance " + "Validation data")  # type: ignore
    plt.savefig(image_path + "/permutation_importance_validation.png")  # type: ignore
    plt.close()  # type: ignore

    plt.clf()
    xgb.plot_importance(classifier)  # type: ignore
    plt.savefig(image_path + "/test2.png")  # type: ignore
    plt.close()  # type: ignore

    ## FIXME: Confidence plot histogram.


def probability_histogram_plot(
    classifier: xgb.XGBClassifier,
    train: pd.DataFrame,
    test: pd.DataFrame,
    val: pd.DataFrame,
    x_par: list[str],
    y_par: str,
):
    train_data_prob = classifier.predict_proba(train[x_par])  # type: ignore
    train_data_prob_max = np.amax(train_data_prob, axis=1)  # type: ignore
    test_data_prob = classifier.predict_proba(test[x_par])  # type: ignore
    test_data_prob_max = np.amax(test_data_prob, axis=1)  # type: ignore
    val_data_prob = classifier.predict_proba(val[x_par])  # type: ignore
    val_data_prob_max = np.amax(val_data_prob, axis=1)  # type: ignore

    # plot all three histograms in frame with three plots
    fig, axs = plt.subplots(3, sharex=True, sharey=False, gridspec_kw={"hspace": 0.5})  # type: ignore
    fig.suptitle("Probability histogram")  # type: ignore
    axs[0].set_title("Training data")  # type: ignore
    axs[0].hist(train_data_prob_max, bins=20)
    axs[1].set_title("Test data")  # type: ignore
    axs[1].hist(test_data_prob_max, bins=20)
    axs[2].set_title("Validation data")  # type: ignore
    axs[2].hist(val_data_prob_max, bins=20)
    plt.savefig(image_path + "/probability_histogram.png")  # type: ignore
    plt.close()  # type: ignore
