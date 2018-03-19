import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import articles from './modules/articles'
import user from './modules/user'
import errorLog from './modules/errorLog'
import getters from './getters'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    errorLog,
    app,
    user,
    articles
  },
  getters
})

export default store
