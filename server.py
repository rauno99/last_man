#!/usr/bin/python

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/stopper/time", methods=["GET"])
def get_stopper_time():
    pass

@app.route("/stopper/start", methods=["POST"])
def start_stopper():
    pass

@app.route("/stopper/reset", methods=["POST"])
def reset_stopper():
    pass

@app.route("/stopper/stop", methods=["POST"])
def stop_stopper():
    pass

@app.route("/timer/time", methods=["GET"])
def get_timer_time():
    pass

@app.route("/timer/start", methods=["POST"])
def start_timer():
    pass

@app.route("/timer/stop", methods=["POST"])
def stop_timer():
    pass

@app.route("/timer/reset", methods=["POST"])
def reset_timer():
    pass

@app.route("/timer/resume", methods=["POST"])
def resume_timer():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)