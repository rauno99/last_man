<template>
  <div>
    <h2>Seistud aeg</h2>
    <h1>{{ times.stopwatch }} </h1>
    <div>
    <h2>Järgmise ülesandeni</h2>
    <h1>{{ times.timer }} </h1>
  </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Voting',
  data() {
    return {
      times: '',
      timePollInterval: null,
    }
  },
  methods: {
    getTimes: function() {
      axios.get('http://192.168.1.156:5000/getTimes')
      .then(res => (this.times = res.data));
    },
  },

  created() {
    this.timePollInterval = setInterval(() => this.getTimes(), 990);
  },
}
</script>

<style scoped>
</style>
