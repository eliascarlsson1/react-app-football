from flask import Flask, request
from flask_cors import CORS
import json
from threading import Thread
from typing import Dict, Any, List
from src.data_handling.data_handling_utils import (
    get_historical_data_list,
    get_all_historical_data_dict,
)
from src.data_handling.database_con import (
    get_all_X_parameters,
    get_all_Y_parameters,
    get_test_names,
    delete_test,
)
from src.model_handling.train_model import train_model
from src.model_handling.manage import (
    delete_model,
    save_model,
    get_model_information,
    save_test,
)
from src.prepare_data.prepare_data import prepare_relevant_data
from src.scrape.update_csv import update_leagues
from src.model_handling.test_model import (
    get_stats_for_model_and_test,
    get_roi_for_model,
)

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes
app.config["CORS_HEADERS"] = "Content-Type"


### Variables ###
all_historical_data_dict = get_all_historical_data_dict()

### Live update ###
global prepareDataTotal
prepareDataTotal = 13
global prepareDataStatus
prepareDataStatus = 0


def setPrepareDataStatus(newStatus: int, newTotal: int):
    global prepareDataStatus
    prepareDataStatus = newStatus
    global prepareDataTotal
    prepareDataTotal = newTotal


@app.route("/prepare-data-progress", methods=["GET"])
def get_prepare_data_progress() -> str:
    statusList: Any = {"status": prepareDataStatus, "total": prepareDataTotal}
    return json.dumps(statusList)


### API Routes ###


# Historical data API Route
@app.route("/api/historical")
def historical_data():
    return get_historical_data_list()


# X parameters API Route
@app.route("/api/parameters/x")
def x_parameters():
    return get_all_X_parameters()


# Y parameters API Route
@app.route("/api/parameters/y")
def y_parameters():
    return get_all_Y_parameters()


# Get current models API Route
@app.route("/api/current-models")
def current_models():
    return get_model_information()


# Get current tests API Route
@app.route("/api/current-tests")
def current_tests():
    return get_test_names()


# Train model API Route
@app.route("/api/train-model-call", methods=["POST"])
def train_model_call() -> str:
    object: Dict[str, Any] = request.get_json()
    ret: str = train_model(object)
    return ret


# Prepare data API Route
@app.route("/api/prepare-data-call", methods=["POST"])
def prepare_data_call() -> str:
    t1 = Thread(
        target=prepare_relevant_data,
        args=(all_historical_data_dict, True, setPrepareDataStatus),
    )
    t1.start()
    return "Started"


# Download latest data API Route
@app.route("/api/download-latest-data-call", methods=["POST"])
def download_latest_data_call() -> str:
    ret: str = update_leagues()
    return ret


# Delete model API Route
@app.route("/api/delete-model-call", methods=["POST"])
def delete_model_call() -> str:
    object = request.get_json()
    name: str = object.get("modelName")
    ret: str = delete_model(name)
    return ret


# Delete test API Route
@app.route("/api/delete-test-call", methods=["POST"])
def delete_test_call() -> str:
    object = request.get_json()
    name: str = object.get("testName")
    ret: str = delete_test(name)
    return ret


# Save model API Route
@app.route("/api/save-model-call", methods=["POST"])
def save_model_call() -> str:
    object = request.get_json()
    name: str = object.get("modelName")
    ret: str = save_model(name)
    return ret


# Save test API Route
@app.route("/api/save-test-call", methods=["POST"])
def save_test_call() -> str:
    object = request.get_json()
    filterData: str = object.get("filterData")
    ret: str = save_test(filterData)
    return ret


# Get roi from model API Route
@app.route("/api/get-roi-model", methods=["POST"])
def roi_model() -> Dict[str, Any]:
    object = request.get_json()
    testData: List[str] = object.get("testData")
    modelName: str = object.get("modelName")
    ret: Dict[str, Any] = get_roi_for_model(testData, modelName)
    return ret


# Get roi from model and test API Route
@app.route("/api/get-roi-model-test", methods=["POST"])
def roi_test_model() -> Dict[str, Any]:
    object = request.get_json()
    print(object)
    modelName: str = object.get("modelName")
    testName = object.get("testName")
    testData: List[str] = object.get("testData")
    ret: Dict[str, Any] = get_stats_for_model_and_test(testData, modelName, testName)
    return ret


if __name__ == "__main__":
    app.run(debug=True)
