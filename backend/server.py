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
    get_country_and_tournament_from_league_id,
    get_all_league_ids_to_names,
    get_pipeline_names,
    get_pipeline_parameters,
    add_pipeline,
    delete_pipeline,
)
from src.model_handling.train_model import train_model
from src.model_handling.manage import (
    delete_model,
    save_model,
    get_model_information,
    save_test,
)
from src.prepare_data.prepare_data import prepare_relevant_data, prepared_scraped_games
from src.scrape.update_csv import update_leagues
from src.scrape.scrape_oddsportal import scrape_league
from src.model_handling.test_model import (
    get_stats_for_model_and_test,
    get_roi_for_model,
)
import traceback

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


# Scrape leagues by id API Route
@app.route("/api/scrape-leagues-by-id", methods=["POST"])
def scrape_leagues_by_id() -> str:
    leagueIds: List[str] = request.get_json()

    def scrape_leagues_in_background(leagueIds: List[str]) -> None:
        for leagueId in leagueIds:
            country_league_list = get_country_and_tournament_from_league_id(leagueId)
            country = country_league_list[0]  # type: ignore
            tournament = country_league_list[1]  # type: ignore

            if not isinstance(country, str) or not isinstance(tournament, str):
                print("Error finding country and tournament from leagueId: " + leagueId)
            else:
                print("Scraping " + country + " " + tournament)
                scrape_league(country, tournament)

    thread = Thread(target=scrape_leagues_in_background, args=(leagueIds,))
    thread.start()

    return "Scrape started"


# Test this api in powershell:
# Invoke-RestMethod -Uri 'http://localhost:5000/api/scrape-leagues-by-id'
# -Method POST -Body '["BL", "PL"]' -Headers @{'Content-Type' = 'application/json'}


# Prepare scraped data
@app.route("/api/prepare-scraped-data", methods=["POST"])
def prepare_scraped_data() -> str:
    try:
        prepared_scraped_games(all_df_dict=all_historical_data_dict)
    except:
        print("An error occurred:")
        traceback.print_exc()
        return "Failed"
    return "Success"


# Get all league ids to names
@app.route("/api/get-league-ids-to-names", methods=["GET"])
def get_league_ids_to_names() -> str:
    return json.dumps(get_all_league_ids_to_names())


# Get all pipeline information
@app.route("/api/get-pipeline-information", methods=["GET"])
def get_pipeline_information_call() -> str:
    pipeline_names = get_pipeline_names()
    pipeline_information: List[Any] = []
    for pipeline_name in pipeline_names:
        pipeline_information.append(get_pipeline_parameters(pipeline_name))
    return json.dumps(pipeline_information)


# Delete pipeline
@app.route("/api/delete-pipeline", methods=["POST"])
def delete_pipeline_call() -> str:
    object = request.get_json()
    pipeline_name: str = object.get("pipelineName")
    ret: str = delete_pipeline(pipeline_name)
    return ret


# Save pipeline
@app.route("/api/save-pipeline", methods=["POST"])
def save_pipeline_call() -> str:
    object = request.get_json()
    name: str = object.get("name")
    model: str = object.get("model")
    test: str = object.get("test")
    leagues: List[str] = object.get("leagues")
    ret = add_pipeline(name, model, test, leagues)
    return ret


if __name__ == "__main__":
    app.run(debug=True)
