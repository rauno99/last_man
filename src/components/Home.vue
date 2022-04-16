<template>
    <div>
        <b-row class="text-center">
            <b-col>
                <h2 class="timeTitle">Seistud aeg</h2>
                <h1 class="time">{{ formattedStopper }}</h1>
            </b-col>
            <b-col>
                <h2 class="timeTitle">Järgmise ülesandeni</h2>
                <h1 class="time">{{ formattedTimer }}</h1>
            </b-col>
        </b-row>
        <hr>
        <b-row class="text-center">
            <b-col>
            <table>
                <thead>
                    <tr>
                        <th class="playerNames">Mängija nimi</th>
                        <th class="playerNames">Kaotused</th> 
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
                <h1 class="timeTitle" v-else>Hääletatud!</h1>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <vue-poll v-if="showPlayerPoll" v-bind="playerPollOptions" @addvote="addPlayerVote" />
                <h1 class="timeTitle" v-else>Hääletatud!</h1>
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
            stopperValueAtStop: null,
            timerInterval: null,
            timePollInterval: null,
            formattedStopper: null,
            formattedTimer: null,
            stopperAlive: false,
            timerAlive: false,
            timerDuration: null,
            ip: window.location.hostname,
            protocol: "https://",
            players: {},

            taskPollOptions: {
                question: "Ülesande hääletus",
                answers: []
            },

            playerPollOptions: {
                question: "Mängija hääletus",
                answers: []
            },

            showPlayerPoll: true,
            showTaskPoll: true,
            loading: true
        };
    },
    methods: {
        /////////////////////////METHODS//////////////////////////////////////7
        formatTimeString: function(sec) {
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

            return hours.toString() + ":" + mins.toString() + ":" + sec.toString()
        },
        calcX: function(n) {
            return "X".repeat(n)
        },

        ////////////////////////POLL FROM SERVER////////////////////////////////
        getTimes: function () {
            axios.get(this.protocol + this.ip + "/stopper/time").then((res) => {
                    this.stopper = res.data.stopwatch_start
                    this.stopperAlive = res.data.running
                    this.stopperValueAtStop = res.data.value_at_stop
                    if (this.stopperAlive === false && this.loading === true) {
                        this.formattedStopper = this.formatTimeString(this.stopperValueAtStop)
                    }
                });
            axios.get(this.protocol + this.ip + "/timer/time").then((res) => {
                this.timer = res.data.timer_start
                this.timerAlive = res.data.running
                this.timerDuration = res.data.timer_value
            });
        },

        getPlayers: function() {
            axios.get(this.protocol + this.ip + "/player/get").then((res) => {
                this.players = res.data
            });     
        },

        getPlayersforVote: function() {
            axios.get(this.protocol + this.ip + "/voting/players/get").then((res) => {
                this.playerPollOptions.answers = res.data
            }); 
        },

        getTasks: function() {
            axios.get(this.protocol + this.ip + "/voting/tasks").then((res) => {
                this.taskPollOptions.answers = res.data
            });
        },

        getAllData: function() {
            this.getTasks();
            this.getPlayers();
            this.getPlayersforVote();
        },
        /////////////////////////STOPPER////////////////////////////////////
        formatStopper: function() {
            this.loading = false
            if (this.stopperAlive) {
                let currentTime = Math.floor(Date.now() / 1000)
                let calcStopper = currentTime - this.stopper + this.stopperValueAtStop
                this.formattedStopper = this.formatTimeString(calcStopper)
            }
        },

        ////////////////////////////TIMER/////////////////////////////////
        formatTimer: function() {
            if (this.timerAlive) {
                let currentTime = Math.floor(Date.now() / 1000)
                let calcTimer = this.timerDuration - (currentTime - this.timer)
                this.formattedTimer = this.formatTimeString(calcTimer)
            }
        },

        ///////////////////////////PLAYERS//////////////////////////////7
        addPlayerVote: function(obj) {
            this.showPlayerPoll = false
            axios.post(this.protocol + this.ip + "/voting/players/addvote/" + obj.value.toString())
        },

        ////////////////////////////TASKS////////////////////////////////
        addTaskVote: function(obj) {
            this.showTaskPoll = false
            axios.post(this.protocol + this.ip + "/voting/tasks/addvote/" + obj.value.toString())
        },
    },

    mounted() {
        this.getTimes()
        this.getPlayers();
        this.getTasks();
        this.getPlayersforVote()
        this.timePollInterval = setInterval(() => this.getTimes(), 3000);
        this.stopperInterval = setInterval(() => this.formatStopper(), 1000);
        this.timerInterval = setInterval(() => this.formatTimer(), 1000);
        this.dataInterval = setInterval(() => this.getAllData(), 1000)
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
