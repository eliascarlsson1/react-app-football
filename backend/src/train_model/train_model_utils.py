import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
import category_encoders as ce
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier


def sample_ML_data(
    dataframes_dict,
    sample_dataframes=[],
    fraction_test=0.3,
    fraction_val=0.15,
    train_dataframes=[],
    test_dataframes=[],
    val_dataframes=[],
    seed=142,
):
    # Creating a list of all dataframes
    dataframes_names = [key for key in dataframes_dict]
    dataframes = [dataframes_dict[key] for key in dataframes_names]

    # Preparing test and train data
    for i, df in enumerate(dataframes):
        df["n_df"] = dataframes_names[i]

    data = pd.concat(dataframes).reset_index()
    data = data.assign(OvUn=[">2.5" if TG > 2.5 else "<2.5" for TG in data["TG"]])
    data = data.assign(OvUnB=[1 if TG > 2.5 else 0 for TG in data["TG"]])
    data = data.assign(
        FTRB=[0 if FTR == "H" else 1 if FTR == "D" else 2 for FTR in data["FTR"]]
    )
    data = data.dropna()

        test = data[data.n_df.isin(test_dataframes)]
        val = data[data.n_df.isin(val_dataframes)]
        train = data[data.n_df.isin(train_dataframes)]

    return train, test, val


# def model_statistics(classifier, train, val, test, x_par, y_par):
#     # Print accuracy
#     print(
#         "Training data accuracy: "
#         + str(round(classifier.score(train[x_par], train[y_par]) * 100, 1))
#     )
#     print(
#         "Validation data accuracy: "
#         + str(round(classifier.score(val[x_par], val[y_par]) * 100, 1))
#     )
#     print(
#         "Test data accuracy: "
#         + str(round(classifier.score(test[x_par], test[y_par]) * 100, 1))
#     )


# def feature_importance_RF(classifier, x_par):
#     # Plot importance
#     importances = classifier.feature_importances_
#     std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)

#     forest_importances = pd.Series(importances, index=x_par)

#     fig, ax = plt.subplots()
#     forest_importances.plot.bar(yerr=std, ax=ax)
#     ax.set_title("Feature importances using MDI")
#     ax.set_ylabel("Mean decrease in impurity")
#     fig.tight_layout()


# def feature_selection(classifier, val, x_par, y_par):
#     permuter = PermutationImportance(
#         classifier, scoring="accuracy", n_iter=5, random_state=42
#     )

#     permuter.fit(val[x_par], val[y_par])

#     return permuter


# def train_XGB(
#     train,
#     x_par,
#     y_par,
#     n_estimators,
#     learning_rate,
#     max_depth,
#     n_jobs=-1,
#     subsample=1,
#     seed=142,
# ):
#     import warnings

#     warnings.filterwarnings("ignore")

#     model1 = XGBClassifier(
#         n_estimators=n_estimators,
#         random_state=seed,
#         n_jobs=n_jobs,
#         learning_rate=learning_rate,
#         subsample=subsample,
#         max_depth=max_depth,
#     )

#     model1.fit(train[x_par], train[y_par])

#     return model1
