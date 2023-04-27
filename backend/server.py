from flask import Flask, request
from flask_cors import CORS
from src.data_handling.data_handling_utils import get_historical_data_list

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes


# Historical data API Route
@app.route("/api/historical")
def historical():
    return get_historical_data_list()


# Train model API Route
@app.route("/api/train-model", methods=["POST"])
def train_model():
    object = request.get_json()
    print(object)
    # print the type of object
    print("The type of object is: ", type(object))
    return "Success"


# {'type': 'train model', 'trainingData': [],
# 'testData': [], 'evaluateSplit': True, 'xParameters': [],
# 'yParameters': [], 'learningRate': 0.3, 'maxDepth': 4,
# 'numberEstimators': 250}


if __name__ == "__main__":
    app.run(debug=True)
