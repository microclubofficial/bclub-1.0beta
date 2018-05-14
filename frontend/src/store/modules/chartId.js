const chartId = {
  state: {
    'chartId': '',
    'chartCh': ''
  },
  mutations: {
    CHART_ID (state, payload) {
      state.chartId = payload.chartId
      state.chartCh = payload.chartCh
    }
  }
}

export default chartId
