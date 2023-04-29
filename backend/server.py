from flask import Flask, request
from flask_cors import CORS
from typing import Dict, Any, List
from src.data_handling.data_handling_utils import (
    get_historical_data_list,
    get_all_historical_data_dict,
)
from src.data_handling.database_con import (
    get_all_X_parameters,
    get_all_Y_parameters,
    get_model_names,
)
from src.model_handling.train_model import train_model
from src.model_handling.manage import delete_model, save_model
from src.prepare_data.prepare_data import prepare_relevant_data
from src.scraping.update_csv import update_leagues
from src.model_handling.test_model import get_roi_for_model_and_test

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes


### Variables ###
all_historical_data_dict = get_all_historical_data_dict()


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
    return get_model_names()


# Train model API Route
@app.route("/api/train-model-call", methods=["POST"])
def train_model_call() -> str:
    object: Dict[str, Any] = request.get_json()
    ret: str = train_model(object)
    return ret


# Prepare data API Route
@app.route("/api/prepare-data-call", methods=["POST"])
def prepare_data_call() -> str:
    ret: str = prepare_relevant_data(
        all_df_dict=all_historical_data_dict, only_current_year=False
    )
    return ret


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


# Save model API Route
@app.route("/api/save-model-call", methods=["POST"])
def save_model_call() -> str:
    object = request.get_json()
    name: str = object.get("modelName")
    ret: str = save_model(name)
    return ret

# Get roi from model and test API Route
@app.route("/api/get-roi-model-test", methods=["POST"])
def roi_test_model() -> Dict[str, str]:
    object = request.get_json()
    modelName: str = object.get("modelName")
    testData: List[str] = object.get("testData")
    testName: str = object.get("testName") # type: ignore
    ret: Dict[str, str] = get_roi_for_model_and_test(testData, modelName)
    return ret

if __name__ == "__main__":
    app.run(debug=True)
