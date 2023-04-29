import pandas as pd
import json
import datetime
from typing import List, Any
from xgboost import XGBClassifier

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestClassifier
# import eli5
# from eli5.sklearn import PermutationImportance
# from sklearn.pipeline import make_pipeline
# from sklearn.pipeline import Pipeline
# import category_encoders as ce
# from sklearn.impute import SimpleImputer

# Default parameters
n_jobs = -1
seed = 142
subsample = 1

def train_XGB(
    train: pd.DataFrame,
    x_par: List[str],
    y_par: str,
    n_estimators: int,
    learning_rate: float,
    max_depth: int,
    n_jobs: int = n_jobs,
    subsample: int = subsample,
    seed: int = seed,
) -> Any:
    import warnings

    warnings.filterwarnings("ignore")

    model1 = XGBClassifier(
        n_estimators=n_estimators,
        random_state=seed,
        n_jobs=n_jobs,
        learning_rate=learning_rate,
        subsample=subsample,
        max_depth=max_depth,
    )
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    y_train = le.fit_transform(train[y_par])  # type: ignore

    model1.fit(train[x_par], y_train)

    return model1


def save_model_parameters(
    train: List[str],
    x_par: List[str],
    y_par: str,
    n_estimators: int,
    learning_rate: float,
    max_depth: int,
    path: str,
    n_jobs: int = n_jobs,
    subsample: int = subsample,
    seed: int = seed,
) -> Any:
    ## save parameters to file
    parameters = {
        "trainingData": train,
        "xParameters": x_par,
        "yParameter": y_par,
        "learningRate": learning_rate,
        "maxDepth": max_depth,
        "numberEstimators": n_estimators,
        "n_jobs": n_jobs,
        "subsample": subsample,
        "seed": seed,
        "date": str(datetime.datetime.now()),
    }
    #todays date
    with open(path + "/current_model_parameters.json", "w") as f:
        json.dump(parameters, f)





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
