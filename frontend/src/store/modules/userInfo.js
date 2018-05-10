// import {post} from '../../utils/http'
const userInfo = {
  state: {
    userInfo: {
      'username': '',
      'avatar': '',
      'isLogin': false
    }
  },
  mutations: {
    USER_INFO (state, payload) {
      // console.log(payload)
      state.userInfo = payload
    }
  }
}

export default userInfo
