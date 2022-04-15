<template>
    <div>
        <b-container fluid>
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
                    <!--<input v-model="stopperDuration" placeholder="00:00:00">-->
                    <b-button class="m-1" @click="startStopper">Start</b-button>
                    <b-button class="m-1" @click="resumeStopper">Resume</b-button>
                    <b-button class="m-1" @click="stopStopper">Stop</b-button>
                </b-col>
                <b-col>
                    <input v-model="timerUserDuration" placeholder="Minutid">
                    <b-button class="m-1" @click="startTimer">Start</b-button>
                    <b-button class="m-1" @click="resumeTimer">Resume</b-button>
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
                            <th class="playerNames">Fails</th> 
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
                    <vue-poll v-bind="pollOptions" />
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
                ip: window.location.hostname + ":5000",
                protocol: "http://",
                players: {},
                stopperAlive: false,
                timerAlive: false,
                threadPollInterval: null,
                pollOptions: {
                question: "Järgmine ülesanne",
                answers: [
                ],
                showResults: true,
            },
                mostPopularTask: "",
                loading: true,

            }
        },
        methods: {
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
        startStopper: function () {
            /*let sendData = ''
            if (this.stopperDuration === '') {
                sendData = 0
            }
            else {
                sendData = this.stopperDuration
            }*/
            axios.post(this.protocol + this.ip + "/stopper/start").then((response) => {
                this.stopper = response.data.stopwatch_start
                this.stopperAlive = response.data.running
                this.stopperValueAtStop = response.data.value_at_stop
            });
        },
        resumeStopper: function () {
            axios.post(this.protocol + this.ip + "/stopper/resume").then((response) => {
                this.stopper = response.data.stopwatch_start
                this.stopperAlive = response.data.running
                this.stopperValueAtStop = response.data.value_at_stop
            });
        },
        stopStopper: function () {
            axios.post(this.protocol + this.ip + "/stopper/stop").then((response) => {
                this.stopper = response.data.stopwatch_start
                this.stopperAlive = response.data.running
                this.stopperValueAtStop = response.data.value_at_stop
            });
        },

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

        formatStopper: function() {
            this.loading = false
            if (this.stopperAlive) {
                let currentTime = Math.floor(Date.now() / 1000)
                let calcStopper = currentTime - this.stopper + this.stopperValueAtStop

                this.formattedStopper = this.formatTimeString(calcStopper)
            }
        },

        formatTimer: function() {
            if (this.timerAlive) {
                let currentTime = Math.floor(Date.now() / 1000)
                let calcTimer = this.timerDuration - (currentTime - this.timer)
                
                this.formattedTimer = this.formatTimeString(calcTimer)
            }
        },
        startTimer: function () {
            let timerMinutes = this.timerUserDuration * 60
            if (timerMinutes !== 0) {
                axios.post(this.protocol + this.ip + "/timer/start", {
                    "duration": timerMinutes
                }).then((response) => {
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
        getPlayers: function() {
            axios
                .get(this.protocol + this.ip + "/player/get")
                .then((res) => (this.players = res.data));     
        },
        addPlayer: function() {
            if (this.playerName != '') {
                axios.post(this.protocol + this.ip + "/player/add", {
                    "name": this.playerName
                }).then((response) => {
                    this.playerName = ''
                    this.players = response.data
                    //console.log(response)
                });
            }
        },
        removePlayer: function(name) {
            axios.post(this.protocol + this.ip + "/player/remove/" + name)
            .then((response) => {
                this.players = response.data
            });
        },

        addFail: function(name) {
            axios.post(this.protocol + this.ip + "/fail/add/" + name)
            .then((response) => {
                this.players = response.data
            });
        },
        removeFail: function(name) {
            axios.post(this.protocol + this.ip + "/fail/remove/" + name)
            .then((response) => {
                this.players = response.data
            });      
        },
        calcX: function(n) {
            return "X".repeat(n)
        },
        getTasks: function() {
            axios
                .get(this.protocol + this.ip + "/voting/tasks")
                .then((res) => {
                    this.pollOptions.answers = res.data
                });
            axios
                .get(this.protocol + this.ip + "/voting/winner_task")
                .then((res) => {
                    this.mostPopularTask = res.data
                });
        },
        endTasksPoll: function() {
            axios.post(this.protocol + this.ip + "/voting/end")
            .then((response) => {
                this.mostPopularTask = response.data
            });
            this.getTasks();    
        }
    },

    mounted() {
        this.getTimes();
        this.stopperInterval = setInterval(() => this.formatStopper(), 1000);
        this.timePollInterval = setInterval(() => this.getTimes(), 5000);
        this.timerInterval = setInterval(() => this.formatTimer(), 1000);
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