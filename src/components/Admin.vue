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
                <br>
                <b-button @click="addPlayer">Add player</b-button>
                </b-col>
            </b-row>
        </b-container>

    </div>
</template>

<script>
    import axios from "axios"
    export default {
        name: "Admin",
        data() {
            return {
                timer: '',
                stopper: '',
                timePollInterval: null,
                playerName: '',
                timerDuration: '',
                ip: window.location.hostname
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
            axios.post("http://" + this.ip + ":5000/stopper/start");
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
        addPlayer: function() {
            if (this.playerName != '') {
                axios.post("http://" + this.ip + ":5000/player/add", {
                    "name": this.player
                }).then((response) => {
                    this.player = ''
                    console.log(response)
                });
            }
        },
    },

    mounted() {
        this.timePollInterval = setInterval(() => this.getTimes(), 500);
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
</style>