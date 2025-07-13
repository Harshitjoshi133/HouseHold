import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import services from './modules/services'
import requests from './modules/requests'

Vue.use(Vuex) // ✅ Required in Vue 2

export default new Vuex.Store({
  modules: {
    auth,
    services,
    requests
  }
})
