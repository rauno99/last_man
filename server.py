#!/usr/bin/python

#MVP-d:
#Markus, Markus, Samsungi monitor, huge ass chonky Samsungi monitor, Robert
from math import floor
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
tasks = {}

stopwatch_stop_flag = False
timer_stop_flag = False

def time_convert(sec):
    sec = floor(sec)
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

    if sec < 10:
        sec = "0" + str(sec)

    if mins < 10:
        mins = "0" + str(mins)

    if hours < 10:
        hours = "0" + str(hours)

    return str(hours) + ":" + str(mins) + ":" + str(sec)

def stopwatch():
    global stopwatch_value
    start = time.time()

    while True:
        if stopwatch_stop_flag:
            break
        stopwatch_value = time.time() - start

def timer(duration):
    global timer_value
    start = time.time()

    while True:
        if timer_stop_flag:
            break
        timer_value = duration - (time.time() - start)

def read_players():
    global players
    with open("players_database.json") as players_database:
        players = json.load(players_database)

def update_players_file():
    global players
    with open("players_database.json", "w") as database:
        json.dump(players, database)

def read_tasks():
    global tasks
    with open("tasks_database.json") as tasks_database:
        tasks = json.load(tasks_database)

@app.route("/stopper/time", methods=["GET"])
def get_stopper_time():
    global stopwatch_value
    return jsonify({"stopwatch": time_convert(stopwatch_value)})

@app.route("/stopper/start", methods=["POST"])
def start_stopper():
    global stopwatch_thread, stopwatch_stop_flag
    stopwatch_stop_flag = False
    stopwatch_thread = Thread(target=stopwatch)
    stopwatch_thread.start()
    return "Stopper käib", 200

@app.route("/stopper/reset", methods=["POST"])
def reset_stopper():
    global stopwatch_value, stopwatch_stop_flag, stopwatch_thread

    stopwatch_stop_flag = True
    stopwatch_thread.join()
    stopwatch_value = 0
    return "stopper reset", 200

@app.route("/stopper/stop", methods=["POST"])
def pause_stopper():
    global stopwatch_thread, stopwatch_stop_flag

    stopwatch_stop_flag = True
    stopwatch_thread.join()
    return "Stopper stopped", 200

@app.route("/timer/time", methods=["GET"])
def get_timer_time():
    global timer_value
    return jsonify({"timer": time_convert(timer_value)})

@app.route("/timer/start", methods=["POST"])
def start_timer():
    global timer_thread
    data = request.json
    duration = data["duration"]
    timer_thread = Thread(target=timer, args=(duration,))
    timer_thread.start()
    return "", 200

@app.route("/timer/stop", methods=["POST"])
def stop_timer():
    pass

@app.route("/timer/reset", methods=["POST"])
def reset_timer():
    pass

@app.route("/timer/resume", methods=["POST"])
def resume_timer():
    pass

@app.route("/player/get", methods=["GET"])
def get_players():
    return jsonify(players), 200

@app.route("/fail/add/<name>", methods=["POST"])
def add_fail(name):
    players[name] += 1
    update_players_file()
    return jsonify(players), 200

@app.route("/fail/remove/<name>", methods=["POST"])
def remove_fail(name):
    if players[name] <= 0:
        players[name] = 0
    else:
        players[name] -= 1
    update_players_file()
    return jsonify(players), 200

@app.route("/player/add", methods=["POST"])
def add_player():
    data = request.json
    print(data)
    players[data["name"]] = 0
    update_players_file()
    return jsonify(players), 200


if __name__ == "__main__":
    read_players()
    #print(players)
    app.run(host="0.0.0.0", port=5000, debug=False)



