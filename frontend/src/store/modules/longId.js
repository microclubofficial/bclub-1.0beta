const longId = {
  state: {
    'hideDilog': true,
    'bId': '',
    'bName': ''
  },
  mutations: {
    LONG_ID (state, payload) {
      state.hideDilog = payload.hideDilog
      state.bId = payload.bId
      state.bName = payload.bName
    }
  }
}

export default longId
