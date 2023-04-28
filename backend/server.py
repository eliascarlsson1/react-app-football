from flask import Flask, request
from flask_cors import CORS
from typing import Dict, Any
from src.data_handling.data_handling_utils import get_historical_data_list
from src.train_model.train_model import train_model

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes


# Historical data API Route
@app.route("/api/historical")
def historical():
    return get_historical_data_list()


# Train model API Route
@app.route("/api/train-model-call", methods=["POST"])
def train_model_call() -> str:
    object:Dict[str, Any] = request.get_json()
    ret:str = train_model(object)
    return ret


# {'type': 'train model', 'trainingData': [],
# 'testData': [], 'evaluateSplit': True, 'xParameters': [],
# 'yParameters': [], 'learningRate': 0.3, 'maxDepth': 4,
# 'numberEstimators': 250}


if __name__ == "__main__":
    app.run(debug=True)
