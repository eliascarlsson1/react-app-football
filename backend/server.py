from flask import Flask

app = Flask(__name__)


# Historical data API Route
@app.route("/api/historical")
def historical():
    return ["BE2223", "PL2223", "LL2223"]
