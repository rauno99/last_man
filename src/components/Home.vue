<template>
    <div>
        <b-container fluid>
            <b-row class="text-center">
                <b-col>
                    <h2 class="timeTitle">Seistud aeg</h2>
                    <h1 class="time" v-if="stopper.stopwatch === 'NaN:NaN:NaN'">
                        00:00:00
                    </h1>
                    <h1 class="time" v-else>{{ stopper.stopwatch }}</h1>
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
                            <td class="playerNames">{{key}}</td>
                            <td class="playerX">{{calcX(value)}}</td>
                        </tr>
                    </tbody>
                </table>
                </b-col>
            </b-row>

        </b-container>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Home",
    data() {
        return {
            timer: "",
            stopper: "",
            timePollInterval: null,
            ip: window.location.hostname,
            players: {}
        };
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

        getPlayers: function() {
            axios
                .get("http://" + this.ip + ":5000/player/get")
                .then((res) => (this.players = res.data));     
        },
        calcX: function(n) {
            return "X".repeat(n)
        }
    },

    mounted() {
        this.timePollInterval = setInterval(() => this.getTimes(), 900);
        this.getPlayers();
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
