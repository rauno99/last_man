<template>
    <div>
        <b-container fluid>
            <b-row class=text-center>
                <b-col>
                    <h2 class="timeTitle">Seistud aeg</h2>
                    <h1 class="time" v-if="stopper.stopwatch==='NaN:NaN:NaN'">00:00:00</h1>
                    <h1 class="time" v-else>{{ stopper.stopwatch }}</h1>
                </b-col>
                <b-col>
                    <h2 class="timeTitle">Järgmise ülesandeni</h2>
                    <h1 class="time" v-if="timer.timer==='NaN:NaN:NaN'">00:00:00</h1>
                    <h1 v-else class="time">{{ timer.timer }}</h1>
                </b-col>
            </b-row>
            <b-row class=text-center>
                <b-col>
                    <b-button class="m-1" @click="startStopper">Start</b-button>
                    <b-button class="m-1" @click="resetStopper">Reset</b-button>
                    <b-button class="m-1" @click="stopStopper">Stop</b-button>
                </b-col>
                <b-col>
                    <input v-model="timerDuration" placeholder="Minutes">
                    <b-button class="m-1" @click="startTimer">Start</b-button>
                    <b-button class="m-1" @click="resumeTimer">Resume</b-button>
                    <b-button class="m-1" @click="stopTimer">Stop</b-button>
                </b-col>
            </b-row>
            <hr>
            <b-row>
                <b-col>
                <input v-model="playerName" placeholder="Name">
                <b-button class="m-3" @click="addPlayer">Add player</b-button>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                <table>
                    <thead>
                        <tr>
                            <th class="playerNames">Mangija nimi</th>
                            <th class="playerNames">Fails</th> 
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(value, key) in players" :key="key">
                            <td class="playerNames">{{key}}</td>
                            <td class="playerX">{{calcX(value)}}</td>
                            <td><b-button @click="addFail(key)">+</b-button></td>
                            <td><b-button @click="removeFail(key)">-</b-button></td>
                            <td><b-button @click="removePlayer(key)">Remove</b-button></td>
                        </tr>
                    </tbody>
                </table>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <vue-poll v-bind="pollOptions" />
                </b-col>
                <b-col>
                    <h1>Eelmise hääletuse võitja {{mostPopularTask}}</h1>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <b-button @click="endTasksPoll">Lõpeta hääletus</b-button>
                </b-col>
            </b-row>
        </b-container>

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
                timePollInterval: null,
                playerName: '',
                timerDuration: '',
                ip: window.location.hostname,
                players: {},
                stopperAlive: false,
                timerAlive: false,
                threadPollInterval: null,
                pollOptions: {
                question: "Järgmine ülesanne",
                answers: [
                    { value: 1, text: 'yl1', votes: 0 },
                    { value: 2, text: 'yl2', votes: 0 },
                    { value: 3, text: 'yl3', votes: 0 },
                    { value: 4, text: 'yl4', votes: 0 } 
                ],
                showResults: true,
            },
                mostPopularTask: ""
            }
        },
        methods: {
        getTimes: function () {
            axios
                .get("http://" + this.ip + ":5000/stopper/time")
                .then((res) => (this.stopper = res.data));
            axios
                .get("http://" + this.ip + ":5000/timer/time")
                .then((res) => (this.timer = res.data));
        },
        startStopper: function () {
            axios.post("http://" + this.ip + ":5000/stopper/start").then((response) => {console.log(response)});
        },
        resetStopper: function () {
            axios.post("http://" + this.ip + ":5000/stopper/reset");
        },
        stopStopper: function () {
            axios.post("http://" + this.ip + ":5000/stopper/stop");
        },
        startTimer: function () {
            this.timerDuration = this.timerDuration * 60
            axios.post("http://" + this.ip + ":5000/timer/start", {
                "duration": this.timerDuration
            }).then((response) => {
                this.timerDuration = ''
                console.log(response)
            });
        },
        resumeTimer: function () {
            axios.post("http://" + this.ip + ":5000/timer/resume");
        },
        resetTimer: function () {
            axios.post("http://" + this.ip + ":5000/timer/reset");
        },
        stopTimer: function () {
            axios.post("http://" + this.ip + ":5000/timer/stop");
        },
        getPlayers: function() {
            axios
                .get("http://" + this.ip + ":5000/player/get")
                .then((res) => (this.players = res.data));     
        },
        addPlayer: function() {
            if (this.playerName != '') {
                axios.post("http://" + this.ip + ":5000/player/add", {
                    "name": this.playerName
                }).then((response) => {
                    this.playerName = ''
                    this.players = response.data
                    console.log(response)
                });
            }
        },
        removePlayer: function(name) {
            axios.post("http://" + this.ip + ":5000/player/remove/" + name)
            .then((response) => {
                this.players = response.data
            });
        },

        addFail: function(name) {
            axios.post("http://" + this.ip + ":5000/fail/add/" + name)
            .then((response) => {
                this.players = response.data
            });
        },
        removeFail: function(name) {
            axios.post("http://" + this.ip + ":5000/fail/remove/" + name)
            .then((response) => {
                this.players = response.data
            });      
        },
        calcX: function(n) {
            return "X".repeat(n)
        },
        getTasks: function() {
            axios
                .get("http://" + this.ip + ":5000/voting/tasks")
                .then((res) => {
                    this.pollOptions.answers = res.data
                });
            axios
                .get("http://" + this.ip + ":5000/voting/winner_task")
                .then((res) => {
                    this.mostPopularTask = res.data
                });
        },
        endTasksPoll: function() {
            axios.post("http://" + this.ip + ":5000/voting/end")
            .then((response) => {
                this.mostPopularTask = response.data
            });
            this.getTasks();    
        }
    },

    mounted() {
        this.timePollInterval = setInterval(() => this.getTimes(), 900);
        this.getPlayers();
        this.getTasks()
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