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

stopwatch_stop_flag = False
timer_stop_flag = False

stopwatch_value = 0
timer_value = 0

players = {}
tasks = {}

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
    with open("players_database.json", encoding="utf8") as players_database:
        players = json.load(players_database)

def update_players_file():
    global players
    with open("players_database.json", "w", encoding="utf8") as players_database:
        json.dump(players, players_database)

def read_tasks():
    global tasks
    with open("tasks_database.json", encoding="utf8") as tasks_database:
        tasks = json.load(tasks_database)

def choose_tasks():
    global tasks

    choices_needed = 2
    chosen_amount = 0
    choice = []

    for i in range(len(tasks["tasks"][0])):
        candidate = tasks["tasks"][0][str(i + 1)]
        if candidate["include"] == 1:
            choice.append(candidate)
            tasks["tasks"][0][str(i + 1)]["include"] = 0
            update_tasks_file()
            chosen_amount += 1
            if chosen_amount >= choices_needed:
                break

    return choice

def update_tasks_file():
    global tasks
    with open("tasks_database.json", "w", encoding="utf8") as tasks_database:
        json.dump(tasks, tasks_database)

@app.route("/stopper/time", methods=["GET"])
def get_stopper_time():
    global stopwatch_value
    return jsonify({"stopwatch": time_convert(stopwatch_value)})

@app.route("/stopper/start", methods=["POST"])
def start_stopper():
    global stopwatch_thread, stopwatch_stop_flag
    if stopwatch_thread != None and not stopwatch_thread.is_alive() or stopwatch_thread == None:

        stopwatch_stop_flag = False
        stopwatch_thread = Thread(target=stopwatch)
        stopwatch_thread.start()
        return "Stopper käib", 200
    return "Stopper juba käib", 200

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
    global timer_thread, timer_stop_flag
    if timer_thread != None and not timer_thread.is_alive() or timer_thread == None:

        data = request.json
        duration = data["duration"]
        timer_stop_flag = False
        timer_thread = Thread(target=timer, args=(duration,))
        timer_thread.start()
        return "Taimer käib", 200
    return "Taimer juba käib", 200

@app.route("/timer/stop", methods=["POST"])
def pause_timer():
    global timer_thread, timer_stop_flag

    timer_stop_flag = True
    timer_thread.join()
    return "Taimer seisab", 200

@app.route("/timer/reset", methods=["POST"])
def reset_timer():
    global timer_value, timer_stop_flag, timer_thread

    timer_stop_flag = True
    timer_thread.join()
    timer_value = 0
    return "timer reset", 200

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

@app.route("/player/remove/<name>", methods=["POST"])
def remove_player(name):
    players.pop(name)
    update_players_file()
    return jsonify(players), 200

@app.route("/voting/tasks", methods=["GET"])
def send_tasks():
    chosen_tasks = choose_tasks()
    return jsonify(chosen_tasks), 200

#id on see nr enne kõiki teisi asju, sama väärtusega, mis value
@app.route("/voting/tasks/addvote/<id>", methods=["POST"])
def add_task_vote(id):
    tasks["tasks"][0][id]["votes"] += 1
    update_tasks_file()
    return str(tasks["tasks"][0][id]["votes"]), 200
#remove pole vaja vist?

@app.route("/voting/tasks/results", methods=["GET"])
def get_voting_results():
    return ""

#TODO: mängijate hääletus, hääletuse tulemused,
#TODO: ühest seadmest ühe hääle lubamine, hääletuse start

if __name__ == "__main__":
    read_players()
    read_tasks()

    #see on täitsa oiž
    #print(tasks["tasks"][0]["1"]["votes"])
    #print(list(tasks["tasks"][0].values())[:2])


    app.run(host="0.0.0.0", port=5000, debug=False)

