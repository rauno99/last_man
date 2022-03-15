import Vue from 'vue'
import VueRouter from 'vue-router'
import Voting from '../components/Voting.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Voting
  },
]

const router = new VueRouter({
  routes
})

export default router
