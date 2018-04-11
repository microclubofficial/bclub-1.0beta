const chartId = {
  state: {
    'chartId': ''
  },
  mutations: {
    CHART_ID (state, payload) {
      state.chartId = payload.chartId
    }
  }
}

export default chartId
