#!/usr/bin/python

###################################################### -----> VIIMANE JÕLDAK PÜSTI <----- ######################################################

#MVP-d: Markus, Markus, Samsungi monitor, huge ass chonky Samsungi monitor, Robert

import time, json, random
from math import floor
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, static_folder="dist/", static_url_path="/")
CORS(app)

#Local development URL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/last_man_db'

# Heroku database URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://eupjeijraobnwo:19ee1d4919796a724bd693ee2803d20edbbf02dca5abe14fb27402b0949362ad@ec2-52-212-228-71.eu-west-1.compute.amazonaws.com:5432/dbpsjih91uudnl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

###################################################### DB MODELS ######################################################

class Times(db.Model):
    __tablename__ = "times"
    name = db.Column('name', db.String(15), primary_key = True)
    start_time = db.Column('start_time', db.Integer()) #seconds since the epoch
    running = db.Column('running', db.Boolean())
    timer_value = db.Column('timer_value', db.Integer()) #start value of timer in seconds
    value_at_stop = db.Column('value_at_stop', db.Integer()) #amount of seconds passed before stop


class Tasks(db.Model):
    __tablename__ = "tasks"
    value = db.Column('value', db.Integer(), primary_key = True)
    text = db.Column('text', db.String(300))
    votes = db.Column('votes', db.Integer())
    include = db.Column('include', db.Boolean())
    in_voting = db.Column('in_voting', db.Boolean())
    last_winner = db.Column('last_winner', db.Boolean())


class Players(db.Model):
    __tablename__ = "players"
    value = db.Column('value', db.Integer(), primary_key = True)
    name = db.Column('name', db.String(100))
    fails = db.Column('fails', db.Integer())
    votes = db.Column('votes', db.Integer())
    include = db.Column('include', db.Boolean())
    last_winner = db.Column('last_winner', db.Boolean())

###################################################### FUNCTIONS ######################################################

def make_tasks(input="Sõlme tegemine, Rippumine, Peast arvutamine, Ühel jalal seismine, Teksti dešifreerimine, Kavalalt räpane nali, Märki viskamine, Silmad kinni seismine, Raskuse käes hoidmine, Palli hoidmine, Arvude loendamine, Tagurpidi tähestiku lugemine, Pii lugemine, Nööriga pastakas pudelisse, Koostöö ülesanne, Piltmõistatus, Kükitamine, Käed selja taga, Arvamismäng, Ämbri viskamine, Jooksuvõistlus"):
    names = input.split(", ")
    
 
    for i in range(len(names)):
        new_task = Tasks(text=names[i], votes=0, include=True, in_voting=False, last_winner=False)
        db.session.add(new_task)
        db.session.commit()


def choose_tasks():
    reset_in_voting_tasks()
    tasks = Tasks.query.filter_by(include = True).all() 
    choice = random.sample(tasks, k=4)

    results = []

    for task in choice:
        task_object =  {
            "value": task.value,
            "text": task.text,
            "votes": task.votes
        } 

        results.append(task_object)
        queried_task = Tasks.query.get(task.value)
        queried_task.in_voting = True
        db.session.add(queried_task)
        db.session.commit()

    return results


def get_in_voting_tasks():
    tasks = Tasks.query.filter_by(in_voting = True).all()      
    results = [
        {
            "value": task.value,
            "text": task.text,
            "votes": task.votes
        } for task in tasks
    ]
    return results


def reset_in_voting_tasks():
    tasks = Tasks.query.filter_by(in_voting = True).all() 
    for task in tasks:
        task.in_voting = False
        db.session.add(task)
        db.session.commit()    


def reset_tasks_values():
    tasks = Tasks.query.all()
    for task in tasks:
        task.votes = 0
        task.in_voting = False
        task.include = True
        task.last_winner = False
        db.session.add(task)
        db.session.commit()

#TODO:filter
def reset_tasks_votes():
    tasks = Tasks.query.all()
    for task in tasks:
        task.votes = 0
        db.session.add(task)
        db.session.commit()


def reset_tasks_last_winner():
    tasks = Tasks.query.filter_by(last_winner = True).all()
    for task in tasks:
        task.last_winner = False
        db.session.add(task)
        db.session.commit()


def reset_player_values():
    players = Players.query.all()
    for player in players:
        player.fails = 0
        player.votes = 0
        player.include = True
        player.last_winner = False
        db.session.add(player)
        db.session.commit


def reset_player_include():
    players = Players.query.filter_by(include = False).all()
    for player in players:
        player.include = True
        db.session.add(player)
        db.session.commit


#TODO:filter
def reset_player_votes():
    players = Players.query.all()
    for player in players:
        player.votes = 0
        db.session.add(player)
        db.session.commit()


def reset_players_last_winner():
    players = Players.query.filter_by(last_winner = True).all()
    for player in players:
        player.last_winner = False
        db.session.add(player)
        db.session.commit()


def get_all_players():
    players = Players.query.order_by(Players.value).all()

    results = [
        {
            "value": player.value,
            "text": player.name,
            "votes": player.votes,
            "fails": player.fails,
            "last_winner": player.last_winner

        } for player in players
    ]
    return results

def get_players_for_voting():
    players = Players.query.filter_by(include = True).order_by(Players.value).all()

    results = [
        {
            "value": player.value,
            "text": player.name,
            "votes": player.votes,
            "fails": player.fails,

        } for player in players
    ]
    return results

###################################################### ROUTES ######################################################

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

###################################################### Stopwatch ######################################################

@app.route("/stopper/time", methods=["GET"])
def get_stopper_time():
    stopwatch = Times.query.get("stopwatch")

    if stopwatch == None:
        return jsonify({"running": False})

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running, "value_at_stop": stopwatch.value_at_stop}), 200


@app.route("/stopper/start", methods=["POST"])
def start_stopper():
    stopwatch = Times.query.get("stopwatch")
    if stopwatch == None:
        stopwatch = Times(name="stopwatch", start_time = floor(time.time()), running = True, value_at_stop = 0)
        db.session.add(stopwatch)
        db.session.commit()
    elif stopwatch.running == False:
        stopwatch.start_time = floor(time.time())
        stopwatch.running = True
        stopwatch.value_at_stop = 0
        db.session.add(stopwatch)
        db.session.commit()

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running, "value_at_stop": stopwatch.value_at_stop}), 200


@app.route("/stopper/resume", methods=["POST"])
def resume_stopper():
    stopwatch = Times.query.get("stopwatch")

    if stopwatch != None and stopwatch.running == False:
        stopwatch.running = True
        stopwatch.start_time = floor(time.time())
        db.session.add(stopwatch)
        db.session.commit()

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running, "value_at_stop": stopwatch.value_at_stop}), 200


@app.route("/stopper/stop", methods=["POST"])
def stop_stopper():
    stopwatch = Times.query.get("stopwatch")

    if stopwatch != None and stopwatch.running == True:
        stopwatch.running = False
        stopwatch.value_at_stop = floor(time.time()) - stopwatch.start_time + stopwatch.value_at_stop
        db.session.add(stopwatch)
        db.session.commit()

    return jsonify({"stopwatch_start": stopwatch.start_time, "running": stopwatch.running, "value_at_stop": stopwatch.value_at_stop}), 200

###################################################### Timer ######################################################

@app.route("/timer/time", methods=["GET"])
def get_timer_time():
    timer = Times.query.get("timer")

    if timer == None:
        return jsonify({"running": False})

    return jsonify({"timer_start": timer.start_time, "running": timer.running, "timer_value": timer.timer_value}), 200


@app.route("/timer/start", methods=["POST"])
def start_timer():
    data = request.json
    timer = Times.query.get("timer")
    if timer == None:
        timer = Times(name="timer", start_time = time.time(), running = True, timer_value = data["duration"])
        db.session.add(timer)
        db.session.commit()
    elif timer.running == False:
        timer.start_time = time.time()
        timer.running = True
        timer.timer_value = data["duration"]
        db.session.add(timer)
        db.session.commit()
    return jsonify({"timer_start": timer.start_time, "running": timer.running, "timer_value": timer.timer_value}), 200


@app.route("/timer/stop", methods=["POST"])
def stop_timer():
    timer = Times.query.get("timer")

    if timer != None and timer.running == True:
        timer.running = False
        db.session.add(timer)
        db.session.commit()

    return jsonify({"timer_start": timer.start_time, "running": timer.running, "timer_value": timer.timer_value}), 200

###################################################### Tasks ######################################################

@app.route("/voting/tasks", methods=["GET"])
def send_tasks():
    return jsonify(get_in_voting_tasks()), 200


@app.route("/voting/tasks/addvote/<value>", methods=["POST"])
def add_task_vote(value):
    task = Tasks.query.get(value)
    task.votes += 1
    db.session.add(task)
    db.session.commit()

    return jsonify(get_in_voting_tasks()), 200
    

@app.route("/voting/tasks/end", methods=["POST"])
def end_voting():
    reset_tasks_last_winner()
    winner_task = Tasks.query.order_by(Tasks.votes.desc()).first()
    winner_task.include = False
    winner_task.last_winner = True
    db.session.add(winner_task)
    db.session.commit()
    reset_tasks_votes()
    choose_tasks()
    return jsonify({"winner": winner_task.text, "tasks": get_in_voting_tasks()}), 200


@app.route("/voting/winner_task", methods=["GET"])
def get_winner_task():
    winner_task = Tasks.query.filter_by(last_winner = True).all()
    if len(winner_task) != 0:
        winner_task = winner_task[0]
        return jsonify(winner_task.text), 200
    return "", 200

###################################################### Players ######################################################

@app.route("/player/get", methods=["GET"])
def get_players():
    return jsonify(get_all_players()), 200


@app.route("/player/add", methods=["POST"])
def add_player():
    data = request.json
    new_player = Players(name=data["name"], fails=0, votes=0, include=True, last_winner=False)
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


@app.route("/voting/players/addvote/<value>", methods=["POST"])
def add_player_vote(value):
    player = Players.query.get(value)
    player.votes += 1
    db.session.add(player)
    db.session.commit()

    return jsonify(get_players_for_voting()), 200


@app.route("/voting/players/get", methods=["GET"])
def get_for_voting():
    return jsonify(get_players_for_voting()), 200


#TODO: fix
@app.route("/voting/players/end", methods=["POST"])
def end_playervotes():
    reset_players_last_winner()
    reset_player_include()
    winner_player = Players.query.order_by(Players.votes.desc()).first()
    winner_player.include = False
    winner_player.last_winner = True
    db.session.add(winner_player)
    db.session.commit()
    reset_player_votes()

    return jsonify({"winner": winner_player.name, "players": get_players_for_voting()}), 200


@app.route("/voting/winner_player", methods=["GET"])
def get_winner_player():
    winner_player = Players.query.filter_by(last_winner = True).all()
    if len(winner_player) != 0:
        winner_player = winner_player[0]
        return jsonify(winner_player.name), 200
    return "", 200

###################################################### MAIN ######################################################

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)
    #reset_tasks_values()
    #reset_player_values()
    #make_tasks()
    #choose_tasks()