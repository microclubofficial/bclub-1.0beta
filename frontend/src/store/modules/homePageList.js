const homePageList = {
  state: {
    backForNav: []
  },
  mutations: {
    set_backForNav (state, payload) {
      state.backForNav.unshift(state.backForNav)
    }
  },
  actions: {
    set_backForNav ({commit}, payload) {
      commit('set_backForNav', payload)
    }
  }
}

export default homePageList
