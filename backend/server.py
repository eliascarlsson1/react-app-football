from flask import Flask
from flask_cors import CORS
from src.simpleutils import get_historical_data_list

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Historical data API Route
@app.route("/api/historical")
def historical():
    return get_historical_data_list()

if __name__ == "__main__":
    app.run(debug=True)
