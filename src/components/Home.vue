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
        };
    },
    methods: {
        getTimes: function () {
            axios
                .get("http://192.168.1.156:5000/stopper/time")
                .then((res) => (this.stopper = res.data));
            axios
                .get("http://192.168.1.156:5000/timer/time")
                .then((res) => (this.timer = res.data));
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
