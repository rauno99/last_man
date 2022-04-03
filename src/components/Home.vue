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
                            <td class="playerNames">{{value.text}}</td>
                            <td class="playerX">{{calcX(value.fails)}}</td>
                        </tr>
                    </tbody>
                </table>
                </b-col>
            </b-row>
            <b-row>
                <b-col>
                    <vue-poll v-if="showPoll" v-bind="pollOptions" @addvote="addVote" />
                    <h1 class="timeTitle" v-else>"Hääletatud!"</h1>
                </b-col>
            </b-row>
        </b-container>
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
            timePollInterval: null,
            ip: window.location.hostname,
            protocol: "http://",
            players: {},
            pollOptions: {
                question: "Järgmine ülesanne",
                answers: [
                ]
            },
            showPoll: true
        };
    },
    methods: {
        getTimes: function () {
            axios
                .get(this.protocol + this.ip + "/stopper/time")
                .then((res) => (this.stopper = res.data));
            axios
                .get(this.protocol + this.ip + "/timer/time")
                .then((res) => (this.timer = res.data));
        },

        getPlayers: function() {
            axios
                .get(this.protocol + this.ip + "/player/get")
                .then((res) => {
                    this.players = res.data
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
        },
        addVote: function(obj) {
            this.showPoll = false
            axios.post(this.protocol + this.ip + "/voting/tasks/addvote/" + obj.value.toString())
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
