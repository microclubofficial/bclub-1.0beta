const language = {
  state: {
    'language': 'zh'
  },
  mutations: {
    LANGUAGE (state, payload) {
      // console.log(payload)
      state.language = payload.language
    }
  }
}

export default language
