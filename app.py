#!/usr/bin/python

#MVP-d:
#Markus, Markus, Samsungi monitor, huge ass chonky Samsungi monitor, Robert
from math import floor
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from threading import Thread
import time
import json
import random

app = Flask(__name__, static_folder="dist/", static_url_path="/")


#Local development URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/last_man_db'

## Heroku database URL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://eupjeijraobnwo:19ee1d4919796a724bd693ee2803d20edbbf02dca5abe14fb27402b0949362ad@ec2-52-212-228-71.eu-west-1.compute.amazonaws.com:5432/dbpsjih91uudnl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

def read_tasks():
    global tasks, last_used_taskset
    with open("tasks_database.json", encoding="utf8") as tasks_database:
        tasks = json.load(tasks_database)
    last_used_taskset = tasks["last_used"]

def read_players():
    global players
    with open("players_database.json", encoding="utf8") as players_database:
        players = json.load(players_database)

read_players()
read_tasks()

class Players(db.Model):
    __tablename__ = "players"
    value = db.Column('value', db.Integer(), primary_key = True)
    name = db.Column('name', db.String(100))
    fails = db.Column('fails', db.Integer())
    votes = db.Column('votes', db.Integer())
    include = db.Column('include', db.Boolean())

class Tasks(db.Model):
    __tablename__ = "tasks"
    value = db.Column('value', db.Integer(), primary_key = True)
    text = db.Column('text', db.String(300))
    votes = db.Column('votes', db.Integer())
    include = db.Column('include', db.Boolean())

class Times(db.Model):
    __tablename__ = "times"
    name = db.Column('name', db.String(15), primary_key = True)
    start_time = db.Column('start_time', db.Integer()) #seconds since the epoch
    running = db.Column('running', db.Boolean())
    timer_value = db.Column('timer_value', db.Integer()) #start value of timer in seconds

def make_tasks(input):
    names = input.split(", ")
 
    for i in range(len(names)):
        new_task = Tasks(text=names[i], votes=0, include=True)
        db.session.add(new_task)
        db.session.commit()
    
def timer(duration):
    global timer_value
    start = time.time()

    while True:
        if timer_stop_flag or timer_value < 0:
            timer_value = 0
            break
        timer_value = duration - (time.time() - start)

def choose_tasks():

    tasks = Tasks.query.filter_by(include = True).all()
    choice = random.choices(tasks, k=4)

    results = [
        {
            "value": task.value,
            "text": task.text,
            "votes": task.votes
        } for task in choice
    ]
    return results

def get_all_players():
    players = Players.query.all()
    results = [
        {
            "value": player.value,
            "text": player.name,
            "votes": player.votes,
            "fails": player.fails

        } for player in players
    ]
    return results

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/stopper/time", methods=["GET"])
def get_stopper_time():
    stopwatch = Times.query.get("stopwatch")
    if stopwatch == None:
        return jsonify({"running": False})
    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running}), 200

#TODO: kas juba käib
@app.route("/stopper/start", methods=["POST"])
def start_stopper():
    stopwatch = Times.query.get("stopwatch")
    if stopwatch == None:
        stopwatch = Times(name="stopwatch", start_time = time.time(), running = True)
        db.session.add(stopwatch)
        db.session.commit()
    elif stopwatch.running == False:
        stopwatch.start_time = time.time()
        stopwatch.running = True
        db.session.add(stopwatch)
        db.session.commit()
    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running}), 200

@app.route("/stopper/resume", methods=["POST"])
def resume_stopper():
    stopwatch = Times.query.get("stopwatch")

    if stopwatch != None and stopwatch.running == False:
        stopwatch.running = True
        db.session.add(stopwatch)
        db.session.commit()

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running}), 200

@app.route("/stopper/stop", methods=["POST"])
def stop_stopper():

    stopwatch = Times.query.get("stopwatch")

    if stopwatch != None and stopwatch.running == True:
        stopwatch.running = False
        db.session.add(stopwatch)
        db.session.commit()

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running}), 200

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

@app.route("/player/get", methods=["GET"])
def get_players():
    return jsonify(get_all_players()), 200

@app.route("/fail/add/<value>", methods=["POST"])
def add_fail(value):
    player = Players.query.get(value)
    player.fails += 1
    db.session.add(player)
    db.session.commit()
    return jsonify(get_all_players()), 200

@app.route("/fail/remove/<value>", methods=["POST"])
def remove_fail(value):
    player = Players.query.get(value)
    if player.fails > 0:
        player.fails -= 1
    db.session.add(player)
    db.session.commit()
    return jsonify(get_all_players()), 200


#TODO: fix
@app.route("/voting/players/resetvotes", methods=["POST"])
def reset_playervotes():
    players = Players.query.all()
    
    for player in players:
        player.votes = 0
        db.session.add(player)
        db.session.commit()
    return jsonify(get_all_players()), 200

    """for i in range(len(players["players"][0])):
        players["players"][0][str(i)]["votes"] = 0
    update_players_file()
    return "Votes cleared", 200"""

@app.route("/player/add", methods=["POST"])
def add_player():
    data = request.json
    new_player = Players(name=data["name"], fails=0, votes=0, include=True)
    db.session.add(new_player)
    db.session.commit()
    
    results = get_all_players()
    
    return jsonify(results), 200

@app.route("/player/remove/<value>", methods=["POST"])
def remove_player(value):
    player = Players.query.get(value)
    db.session.delete(player)
    db.session.commit()

    return jsonify(get_all_players()), 200

@app.route("/voting/tasks", methods=["GET"])
def send_tasks():
    return jsonify(choose_tasks()), 200

@app.route("/voting/tasks/addvote/<id>", methods=["POST"])
def add_task_vote(id):

    task = Tasks.query.get(id)
    task.votes += 1
    db.session.add(task)
    db.session.commit()

    return 
    
    """tasks["tasks"+str(last_used_taskset+1)][0][id]["votes"] += 1
    update_tasks_file()
    return str(tasks["tasks"+str(last_used_taskset+1)][0][id]["votes"]), 200"""

@app.route("/voting/end", methods=["POST"])
def end_voting():
    global last_used_taskset, winner_task
    current_taskset = tasks["tasks" + str(last_used_taskset+1)][0]
    max_votes = 0
    max_votes_key = None

    for key in current_taskset.keys():
        if current_taskset[key]["votes"] > max_votes:
            max_votes_key = key

    winner_task = current_taskset[max_votes_key]["text"]

    return winner_task, 200

@app.route("/voting/winner_task", methods=["GET"])
def get_winner_task():
    global winner_task
    return winner_task, 200

#TODO: mängijate hääletus, hääletuse tulemused, stopper faili, hääletuse start

app.route("/voting/players/addvote/<value>", methods=["POST"])
def add_player_vote(value):
    players["players"][0][str(value)]["votes"] += 1
    return jsonify(list(players["players"][0].values())), 200

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)
    #make_tasks("Sõlme tegemine väikse krutskiga, peast arvutamine, ühel jalal seismine, teksti dešifreerimine, mõistatuse lahendamine, märki viskamine, vee tassimine ühest anumast teise, silmad kinni seismine, muna hoidmine lusika peal, fraasi kordamine, tagurpidi tähestiku lugemine, numbrite lugemine, nööriga pastakas pudelisse, jäätunud särgi lahti harutamine, torni ehitamine")
    #choose_tasks()
    #stopwatch()