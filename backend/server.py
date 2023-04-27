from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all routes

# Historical data API Route
@app.route("/api/historical")
def historical():
    return ["BE2223", "PL2223", "LL2223"]

if __name__ == "__main__":
    app.run(debug=True)
