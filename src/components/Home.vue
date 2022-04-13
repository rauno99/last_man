<template>
    <div>
            <b-row class="text-center">
                <b-col>
                    <h2 class="timeTitle">Seistud aeg</h2>
                    <h1 class="time" v-if="stopper.stopwatch === 'NaN:NaN:NaN'">
                        00:00:00
                    </h1>
                    <h1 class="time" v-else>{{ formattedStopper }}</h1>
                </b-col>
                <b-col>
                    <h2 class="timeTitle">Järgmise ülesandeni</h2>
                    <h1 class="time" v-if="timer.timer === 'NaN:NaN:NaN'">
                        00:00:00
                    </h1>
                    <h1 v-else class="time">{{ timer.timer }}</h1>
                </b-col>
            </b-row>
            <hr>
            <b-row class="text-center">
                <b-col>
                <table>
                    <thead>
                        <tr>
                            <th class="playerNames">Mängija nimi</th>
                            <th class="playerNames">Fails</th> 
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(value, key) in players" :key="key">
                            <td class="playerNames">{{value.text}}</td>
                            <td class="playerX">{{calcX(value.fails)}}</td>
                        </tr>
                    </tbody>
                </table>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <vue-poll v-if="showTaskPoll" v-bind="taskPollOptions" @addvote="addTaskVote" />
                    <h1 class="timeTitle" v-else>"Hääletatud!"</h1>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <vue-poll v-if="showPlayerPoll" v-bind="playerPollOptions" @addvote="addPlayerVote" />
                    <h1 class="timeTitle" v-else>"Hääletatud!"</h1>
                </b-col>
            </b-row>
    </div>
</template>

<script>
import axios from "axios";
import VuePoll from "vue-poll";

export default {
    name: "Home",
    components: {
        VuePoll
    },
    data() {
        return {
            timer: "",
            stopper: "",
            stopperInterval: null,
            timePollInterval: null,
            formattedStopper: null,
            formattedTimer: null,
            stopperAlive: false,
            timerAlive: false,
            ip: window.location.hostname,
            protocol: "https://",
            players: {},
            taskPollOptions: {
                question: "Ülesande hääletus",
                answers: [
                ]
            },
            playerPollOptions: {
                question: "Mängija hääletus",
                answers: [
                ]
            },
            showPlayerPoll: true,
            showTaskPoll: true
        };
    },
    methods: {
        getTimes: function () {
            axios.get(this.protocol + this.ip + "/stopper/time").then((res) => {
                    this.stopper = res.data.stopwatch_start
                    this.stopperAlive = res.data.running
                });
            //axios.get(this.protocol + this.ip + "/timer/time").then((res) => (this.timer = res.data));
        },

        formatStopper: function() {
            if (this.stopperAlive) {
                let currentTime = Math.floor(Date.now() / 1000)
                let calcStopper = currentTime - this.stopper

                let sec = calcStopper
                let mins = Math.floor(sec / 60)
                sec = sec % 60
                let hours = Math.floor(mins / 60)
                mins = mins % 60

                if (sec < 10)
                    sec = "0" + sec.toString()
                if (mins < 10)
                    mins = "0" + mins.toString()
                if (hours < 10)
                    hours = "0" + hours.toString()
                this.formattedStopper = hours.toString() + ":" + mins.toString() + ":" + sec.toString()
            }
        },
        getPlayers: function() {
            axios
                .get(this.protocol + this.ip + "/player/get")
                .then((res) => {
                    this.players = res.data
                    this.playerPollOptions.answers = res.data
                });     
        },
        calcX: function(n) {
            return "X".repeat(n)
        },
        getTasks: function() {
            axios
                .get(this.protocol + this.ip + "/voting/tasks")
                .then((res) => {
                    this.taskPollOptions.answers = res.data
                });
        },
        addTaskVote: function(obj) {
            this.showTaskPoll = false
            axios.post(this.protocol + this.ip + "/voting/tasks/addvote/" + obj.value.toString())
        },

        addPlayerVote: function(obj) {
            this.showPlayerPoll = false
            //axios.post(this.protocol + this.ip + "/voting/tasks/addvote/" + obj.value.toString())
        }
    },

    mounted() {
        this.getTimes()
        this.timePollInterval = setInterval(() => this.getTimes(), 5000);
        this.stopperInterval = setInterval(() => this.formatStopper(), 1000);
        this.getPlayers();
        this.getTasks();
    },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap");
.time {
    font-family: "Roboto", sans-serif;
    color: gray;
    font-weight: 300;
    font-size: 600%;
}

.timeTitle {
    font-family: "Roboto", sans-serif;
    color: gray;
    font-weight: 300;
    font-size: 200%;
}

.playerNames {
    font-family: "Roboto", sans-serif;
    color: gray;
    font-weight: 300;
    font-size: 200%;
}

.playerX {
    font-family: "Roboto", sans-serif;
    color: darkred;
    font-weight: 300;
    font-size: 150%;
}


table th {
    padding: 20px;
    border-bottom: 1px solid gray;
}

table td {
  text-align: left;
  padding: 20px;
}


</style>
