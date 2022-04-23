import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import Admin from '../components/Admin.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },

  {
    path: '/maeiteamissiiapannagjhlwsiiw285ks5594dks4993k',
    name: 'Admin',
    component: Admin
  },
]

const router = new VueRouter({
  routes
})

export default router
