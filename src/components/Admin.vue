<template>
    <div>
        <b-row class=text-center>
            <b-col>
                <h2 class="timeTitle">Seistud aeg</h2>
                <h1 class="time">{{ formattedStopper }}</h1>
            </b-col>
            <b-col>
                <h2 class="timeTitle">Järgmise ülesandeni</h2>
                <h1 class="time">{{ formattedTimer }}</h1>
            </b-col>
        </b-row>
        <b-row class=text-center>
            <b-col>
                <b-button class="m-1" @click="startStopper">Start/Nulli</b-button>
                <b-button class="m-1" @click="resumeStopper">Resume</b-button>
                <b-button class="m-1" @click="stopStopper">Stop</b-button>
            </b-col>
            <b-col>
                <input v-model="timerUserDuration" placeholder="Minutid">
                <b-button class="m-1" @click="startTimer">Start</b-button>
                <!--<b-button class="m-1" @click="resumeTimer">Resume</b-button>-->
                <b-button class="m-1" @click="stopTimer">Stop</b-button>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
            <input v-model="playerName" placeholder="Nimi">
            <b-button class="m-3" @click="addPlayer">Lisa mängija</b-button>
            </b-col>
        </b-row>
        <b-row>
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
                        <td><b-button @click="addFail(value.value)">+</b-button></td>
                        <td><b-button @click="removeFail(value.value)">-</b-button></td>
                        <td><b-button @click="removePlayer(value.value)">Remove</b-button></td>
                    </tr>
                </tbody>
            </table>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h1 class="timeTitle">Eelmise hääletuse võitja: {{mostPopularTask}}</h1>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <vue-poll v-bind="taskPollOptions" />
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-button @click="endTasksPoll">Lõpeta hääletus</b-button>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h1 class="timeTitle">Eelmise mängija hääletuse võitja: {{mostPopularPlayer}}</h1>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <vue-poll v-bind="playerPollOptions" />
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-button @click="endPlayerPoll">Lõpeta hääletus</b-button>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import axios from "axios"
    import VuePoll from "vue-poll";

    export default {
        name: "Admin",
        components: {
            VuePoll
        },
        data() {
            return {
                timer: '',
                stopper: '',
                stopperInterval: null,
                stopperValueAtStop: null,
                timerInterval: null,
                formattedStopper: null,
                formattedTimer: null,
                timePollInterval: null,
                timerUserDuration: null,
                playerName: '',
                timerDuration: '',
                stopperDuration: '',
                ip: window.location.hostname,
                protocol: "https://",
                players: {},
                stopperAlive: false,
                timerAlive: false,
                threadPollInterval: null,

                taskPollOptions: {
                question: "Järgmine ülesanne",
                answers: [],
                showResults: true,
                },

                playerPollOptions: {
                question: "Mängija hääletus",
                answers: [],
                showResults: true,
                },

                mostPopularTask: "",
                mostPopularPlayer: "",
                loading: true,

            }
        },
        methods: {
            ///////////////////////METHODS///////////////////////////////////

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

            //////////////////POLL FROM SERVER METHODS///////////////////////

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
                axios.get(this.protocol + this.ip + "/voting/winner_player").then((res) => {
                        this.mostPopularPlayer = res.data
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
                axios.get(this.protocol + this.ip + "/voting/winner_task").then((res) => {
                        this.mostPopularTask = res.data
                });
            },

            ///////////////////STOPPER METHODS//////////////////////

            startStopper: function () {
                axios.post(this.protocol + this.ip + "/stopper/start").then((res) => {
                    this.stopper = res.data.stopwatch_start
                    this.stopperAlive = res.data.running
                    this.stopperValueAtStop = res.data.value_at_stop
                });
            },
            resumeStopper: function () {
                axios.post(this.protocol + this.ip + "/stopper/resume").then((res) => {
                    this.stopper = res.data.stopwatch_start
                    this.stopperAlive = res.data.running
                    this.stopperValueAtStop = res.data.value_at_stop
                });
            },
            stopStopper: function () {
                axios.post(this.protocol + this.ip + "/stopper/stop").then((res) => {
                    this.stopper = res.data.stopwatch_start
                    this.stopperAlive = res.data.running
                    this.stopperValueAtStop = res.data.value_at_stop
                });
            },

            formatStopper: function() {
                this.loading = false
                if (this.stopperAlive) {
                    let currentTime = Math.floor(Date.now() / 1000)
                    let calcStopper = currentTime - this.stopper + this.stopperValueAtStop
                    this.formattedStopper = this.formatTimeString(calcStopper)
                }
            },
            ////////////////////////TIMER/////////////////////////////

            startTimer: function () {
                let timerMinutes = this.timerUserDuration * 60
                if (timerMinutes !== 0) {
                    axios.post(this.protocol + this.ip + "/timer/start", {
                        "duration": timerMinutes
                    }).then((res) => {
                        this.timerUserDuration = ''
                    });
                }
            },

            resumeTimer: function () {
                axios.post(this.protocol + this.ip + "/timer/resume");
            },

            resetTimer: function () {
                axios.post(this.protocol + this.ip + "/timer/reset");
            },

            stopTimer: function () {
                axios.post(this.protocol + this.ip + "/timer/stop");
            },

            formatTimer: function() {
                if (this.timerAlive) {
                    let currentTime = Math.floor(Date.now() / 1000)
                    let calcTimer = this.timerDuration - (currentTime - this.timer)
                    this.formattedTimer = this.formatTimeString(calcTimer)
                }
            },

            //////////////////////////PLAYER//////////////////////////////

            addPlayer: function() {
                if (this.playerName != '') {
                    axios.post(this.protocol + this.ip + "/player/add", {
                        "name": this.playerName
                    }).then((res) => {
                        this.playerName = ''
                        this.players = res.data
                    });
                }
            },

            removePlayer: function(name) {
                axios.post(this.protocol + this.ip + "/player/remove/" + name)
                .then((res) => {
                    this.players = res.data
                });
            },

            addFail: function(name) {
                axios.post(this.protocol + this.ip + "/fail/add/" + name)
                .then((res) => {
                    this.players = res.data
                });
            },
            removeFail: function(name) {
                axios.post(this.protocol + this.ip + "/fail/remove/" + name)
                .then((res) => {
                    this.players = res.data
                });      
            },

            endPlayerPoll: function() {
                axios.post(this.protocol + this.ip + "/voting/players/end").then((res) => {
                    this.mostPopularPlayer = res.data.winner
                    this.playerPollOptions.answers = res.data.players
                });
            },

            /////////////////////TASKS/////////////////////////////////

            endTasksPoll: function() {
                axios.post(this.protocol + this.ip + "/voting/tasks/end").then((res) => {
                    this.mostPopularTask = res.data.winner
                    this.taskPollOptions.answers = res.data.tasks
                });
                this.getTasks();    
            }
    },

    mounted() {
        this.getTimes();
        this.getPlayers();
        this.getTasks();
        this.getPlayersforVote()
        this.stopperInterval = setInterval(() => this.formatStopper(), 1000);
        this.timePollInterval = setInterval(() => this.getTimes(), 5000);
        this.timerInterval = setInterval(() => this.formatTimer(), 1000);
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