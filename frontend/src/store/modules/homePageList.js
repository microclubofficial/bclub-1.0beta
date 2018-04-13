const homePageList = {
  state: {
    backForNav: []
  },
  mutations: {
    set_backForNav (state, payload) {
      // state.backForNav.unshift(state.backForNav)
      state.backForNav.unshift(payload)
    },
    clear_backForNav (state) {
      state.backForNav = []
    }
  },
  actions: {
    set_backForNav ({commit}, payload) {
      commit('set_backForNav', payload)
    },
    clear_backForNav ({commit}) {
      commit('clear_backForNav')
    }
  }
}

export default homePageList
