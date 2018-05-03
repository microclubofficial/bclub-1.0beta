const longId = {
  state: {
    'hideDilog': true,
    'bId': ''
  },
  mutations: {
    LONG_ID (state, payload) {
      state.hideDilog = payload.hideDilog
      state.bId = payload.bId
    }
  }
}

export default longId
