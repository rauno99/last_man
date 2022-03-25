#!/usr/bin/python

#MVP-d:
#Markus, Markus, Samsungi monitor, huge ass chonky Samsungi monitor, Robert

from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
import time
import json

app = Flask(__name__)
CORS(app)

stopwatch_thread = None
timer_thread = None

stopwatch_value = 0
timer_value = 0

players = {}

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  return str(hours) + ":" + str(mins) + ":" + str(sec)

def stopwatch():
    global stopwatch_value
    start = time.time()

    while True:
        stopwatch_value = time.time() - start

def timer(duration):
    global timer_value
    start = time.time()

    while True:
        timer_value = duration - (time.time() - start)

def read_players():
    global players
    with open("players_database.json") as database:
        players = json.load(database)

def update_players_file():
    global players
    with open("players_database.json", "w") as database:
        json.dump(players, database)


@app.route("/stopper/time", methods=["POST", "GET"])
def get_stopper_time():
    global stopwatch_value
    return jsonify({"stopwatch": time_convert(stopwatch_value)})

@app.route("/stopper/start", methods=["POST", "GET"])
def start_stopper():
    global stopwatch_thread
    stopwatch_thread = Thread(target=stopwatch)
    stopwatch_thread.start()
    return "Stopper käib"

@app.route("/stopper/reset", methods=["POST"])
def reset_stopper():
    pass

@app.route("/stopper/stop", methods=["POST"])
def pause_stopper():
    global stopwatch_thread

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

@app.route("/fail/add/<name>", methods=["POST", "GET"])
def add_fail(name):
    players[name] += 1
    update_players_file()
    return str(players.get("Robert"))

@app.route("/fail/remove/<name>", methods=["POST", "GET"])
def remove_fail(name):
    players[name] -= 1
    update_players_file()
    if players[name] <= 0:
        return "U dead sucker"
    return str(players.get(name))


if __name__ == "__main__":
    read_players()
    #print(players)
    app.run(host="0.0.0.0", port=5000, debug=True)


