#!/usr/bin/python

#MVP-d:
#Markus, Markus, Samsungi monitor, huge ass chonky Samsungi monitor, Robert
from math import floor
import ssl
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
import time
import json

app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

# stopwatch_thread = None
# timer_thread = None

# stopwatch_stop_flag = False
# timer_stop_flag = False

# stopwatch_value = 0
# timer_value = 0

# players = {}
# tasks = {}
# last_used_taskset = 0

# winner_task = ""

def make_tasks(subset_size, input):
    names = input.split(", ")
    outer_dict = {}
    dict = {}
    taskset_no = 1
    for i in range(len(names)):
        text = names[i]
        task_object = {}
        task_object["value"] = i
        task_object["text"] = text
        task_object["votes"] = 0
        dict[i] = task_object
        if (i+1) % subset_size == 0 or i == len(names) - 1:

            list = []
            list.append(dict)
            outer_key = "tasks" + str(taskset_no)
            outer_dict[outer_key] = list
            dict = {}
            taskset_no += 1

    outer_dict["last_used"] = 0

    with open("tasks_database.json", "w", encoding="utf8") as tasks_file:
        json.dump(outer_dict, tasks_file)

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

def update_times_file():

    with open("times_database.json", "w") as times_file:
        json.dump({"stopwatch": stopwatch_value}, times_file)
        #no mdea mees

def timer(duration):
    global timer_value
    start = time.time()

    while True:
        if timer_stop_flag or timer_value < 0:
            timer_value = 0
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
    global tasks, last_used_taskset
    with open("tasks_database.json", encoding="utf8") as tasks_database:
        tasks = json.load(tasks_database)
    last_used_taskset = tasks["last_used"]

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

def update_last_used():
    global last_used_taskset

    last_used_taskset += 1
    tasks["last_used"] += 1
    update_tasks_file()

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

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
    return jsonify(list(players["players"][0].values())), 200

@app.route("/fail/add/<value>", methods=["POST"])
#nüüd tuleb value saata
def add_fail(value):
    players["players"][0][str(value)]["fails"] += 1
    update_players_file()
    return jsonify(players), 200

@app.route("/fail/remove/<value>", methods=["POST"])
def remove_fail(value):
    if players["players"][0][str(value)]["fails"] > 0:
        players["players"][0][str(value)]["fails"] -= 1
        update_players_file()
    return jsonify(players), 200

@app.route("/voting/players/resetvotes", methods=["POST"])
def reset_playervotes():
    for i in range(len(players["players"][0])):
        players["players"][0][str(i)]["votes"] = 0
    update_players_file()
    return "Votes cleared", 200

@app.route("/player/add", methods=["POST"])
def add_player():
    data = request.json
    print(data)
    player_object = {}
    player_object["value"] = len(players["players"][0]) + 1
    player_object["text"] = data["name"]
    player_object["votes"] = 0
    player_object["fails"] = 0
    key = str(player_object["value"])
    players["players"][0][key] = player_object
    update_players_file()
    return jsonify(players), 200

@app.route("/player/remove/<value>", methods=["POST"])
#kas value tuleb int või str?
def remove_player(value):
    players["players"][0].pop(value)
    update_players_file()
    return jsonify(players), 200

@app.route("/voting/tasks", methods=["GET"])
def send_tasks():
    taskset = "tasks" + str(last_used_taskset + 1)
    chosen_tasks = list(tasks[taskset][0].values())
    print(chosen_tasks)
    return jsonify(chosen_tasks), 200

#id on see nr enne kõiki teisi asju, sama väärtusega, mis value
@app.route("/voting/tasks/addvote/<id>", methods=["POST"])
def add_task_vote(id):
    tasks["tasks"+str(last_used_taskset+1)][0][id]["votes"] += 1
    update_tasks_file()
    return str(tasks["tasks"+str(last_used_taskset+1)][0][id]["votes"]), 200
#remove pole vaja vist?

@app.route("/voting/end", methods=["POST"])
def end_voting():
    global last_used_taskset, winner_task
    print("key: " + str(last_used_taskset+1))
    current_taskset = tasks["tasks" + str(last_used_taskset+1)][0]
    max_votes = 0
    max_votes_key = None

    for key in current_taskset.keys():
        if current_taskset[key]["votes"] > max_votes:
            max_votes_key = key

    winner_task = current_taskset[max_votes_key]["text"]
    print(winner_task)
    update_last_used()

    return winner_task, 200

@app.route("/voting/winner_task", methods=["GET"])
def get_winner_task():
    global winner_task
    return winner_task, 200

#TODO: mängijate hääletus, hääletuse tulemused,
#TODO: ühest seadmest ühe hääle lubamine, hääletuse start, taimer miinusesse
app.route("/voting/players/addvote/<name>", methods=["POST"])
def add_player_vote():
    pass

@app.before_first_request
def execute_before():
    global stopwatch_thread, timer_thread, stopwatch_stop_flag, timer_stop_flag, stopwatch_value, timer_value, players, tasks, last_used_taskset, winner_task
    stopwatch_thread = None
    timer_thread = None

    stopwatch_stop_flag = False
    timer_stop_flag = False

    stopwatch_value = 0
    timer_value = 0

    players = {}
    tasks = {}
    last_used_taskset = 0

    winner_task = ""

    read_players()
    read_tasks()

#TODO: mängijate hääletus, stopperi value faili, ülesanded faili

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

