<template>
  <div class="wrap">
    <div class="center-wrap">
      <div class="title">
        <span>
          <img src="../../../assets/img/i01.png" />
        </span>
        <span>{{$t('editProfile.profile')  }}</span>
        <span>
          <router-link class="hover" :to="{path:'/memberCenter'}">{{$t('personalCenter.returnMyHomepage')}} <i>></i></router-link>
        </span>
      </div>
      <form class="form-horizontal">
        <div class="form-group info-border">
          <div class="clearfix">
            <label class="left control-label personal-font">{{$t('register.username')}}</label>
            <div class="left" >
              <p class="form-control-static personal-font">{{personalUserInfo.username}}</p>
            </div>
            <div class="right">
              <div class="btnm  btn-edit" @click="setFormBtn(0)">{{isShow ? $t('button.fold') : $t('button.edit')}}</div>
            </div>
          </div>
          <!-- 修改用户名 -->
          <form class="form-horizontal form-space margin-top" v-if="isShow">
            <div class="clearfix edit-infor">
              <label for="inputEmail3" class="left control-label">{{$t('register.username')}}</label>
              <div class="left left-width">
                <input type="text" class="form-control" name="username" @change='showsetFormMsg(setForm.username, 0)' v-model="setForm.username" maxlength="16" id="inputEmail3" :placeholder="$t('placeholder.newUsername')">
                <div class="buttons-box clearfix">
                <label class="left control-label"></label>
                <p class="form-control-static prompt" style="margin-top:0px !important;">{{unamePrompt}}</p>
                  <div class="clearfix">
                    <button type="button" class="edit-user-btn" v-bind:disabled="!setForm.username" @click="setusername"  >{{$t('button.confirm')}}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
      
        <div class="form-group info-border">
          <div class="clearfix">
            <label class="left control-label personal-font">{{$t('register.phone')}}</label>
            <div class="left">
              <p class="form-control-static personal-font">{{personalUserInfo.phone}}</p>
            </div>
            <div class="right">
              <div class="btnm  btn-edit" @click="setFormBtn(1)">{{seShow ? $t('button.fold'): $t('button.edit')}}</div>
            </div>
          </div>
          <!-- 修改手机号 -->
          <form class="form-horizontal form-space margin-top" v-if="seShow">
            <div class="edit-infor clearfix">
              <label for="inputEmail3" class="left control-label">{{$t('register.phone')}}</label>
              <div class="left left-width">
                <input type="text" class="form-control" id="inputEmail3" @change='showsetFormMsg(setForm.phone, 1)' v-model="setForm.phone" :placeholder="$t('placeholder.newPhone')">
              <label class="left control-label"></label>
            <p class="prompt form-control-static" style="margin-left:4% !important;margin-top:0px !important;">{{phonePrompt}}</p>
              </div>
            </div>
            <div class="edit-infor clearfix yzm">
              <label for="inputCaptcha3" class="left control-label">{{$t('register.vcode')}}</label>
              <div class="left left-width">
                <div class="yzm-input">
                <input type="text" class="form-control" v-model="setForm.captcha" @change='showsetFormMsg(setForm.captcha, 2)' id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
                 </div>
                <button type="button" class="btn btn-default get-captcha yzm-button" style="height:34px;line-height:34px;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{'btn-success':!hasphone}">
                  <span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}
                </button>
                <div class="buttons-box clearfix">
                  <div class="left left-width">
                    <label class="left control-label"></label>
                    <p class="form-control-static prompt " style="margin-top:0px !important;">{{phoneControlPrompt}}</p>
                    <button type="button" class=" edit-user-btn" v-bind:disabled="!setForm.phone" @click="setusername"  >{{$t('button.confirm')}}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
        <div class="form-group info-border">
          <label class="left control-label personal-font">{{$t('editProfile.registerTime')}}</label>
          <div class="left">
            <p class="form-control-static personal-font">{{personalUserInfo.register_time}}</p>
          </div>
        </div>
        <div class="form-group info-border">
          <label class="left control-label personal-font">{{$t('editProfile.lastLogin')}}</label>
          <div class="left">
            <p class="form-control-static personal-font">{{personalUserInfo.last_login}}</p>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { get, post } from '../../../utils/http'
import { setToken, getToken, rememberToken } from '../../../utils/auth'
import { Toast } from 'mint-ui'
export default {
  data () {
    return {
      personalUserInfo: [],
      setForm: {},
      unamePrompt: '',
      showModel: true,
      hasphone: true,
      countdown: 30,
      hasControl: false,
      timer: null,
      getcontroltxt: this.$t('prompt.acquireVcode'),
      phonePrompt: '',
      phoneControlPrompt: '',
      canSetU: false,
      cansetP: false,
      user_token: '',
      // 展开收起
      isShow: false,
      seShow: false
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  created: function () {
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
    if (this.user_token === '') {
      this.$router.push('/')
    }
    // 个人资料
    this.personalUser(this.userInfo.username)
  },
  mounted () {
  },
  methods: {
    // 验证
    showsetFormMsg (input, id) {
      if (id === 0) {
        let unamereg = /^[a-zA-Z0-9_.\-\u4e00-\u9fa5]{3,16}$/
        if (unamereg.test(input) && input.length > 0 && input !== undefined && input.indexOf(' ') === -1) {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
        let phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/
        if (phonereg.test(input) && input !== undefined && input.length > 0) {
          this.phonePrompt = ''
          this.hasphone = false
          this.setForm.phone = input
        }
      } else if (id === 2) {
        if (input.length > 0) {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 修改用户名和手机号
    setusername () {
      let instance
      let unamereg = /^[a-zA-Z0-9_.\-\u4e00-\u9fa5]{3,16}$/
      if (this.isShow) {
        if (this.setForm.username === undefined || this.setForm.username.length === 0) {
          this.unamePrompt = this.$t('prompt.usernameRequired')
          return false
        } else if (this.setForm.username !== undefined && this.setForm.username.indexOf(' ') >= 0) {
          this.unamePrompt = this.$t('prompt.spaceForbidden')
          return false
        } else if (!unamereg.test(this.setForm.username) && this.setForm.username !== undefined && this.setForm.username.length > 0) {
          this.unamePrompt = this.$t('prompt.usernameLength')
          return false
        }
        post(`/api/setting/username`, this.setForm).then(data => {
          this.setForm.username = ''
          if (data.resultcode === 0) {
            alert(data.message)
            return false
          } else if (data.resultcode === 1) {
            instance = new Toast({
              message: data.message,
              iconClass: 'glyphicon glyphicon-ok',
              duration: 1000
            })
            setTimeout(() => {
              instance.close()
            }, 1000)
            this.$store.commit('USER_INFO', {
              'username': data.data.username,
              'avatar': data.data.avatar,
              'isLogin': true
            })
            if (rememberToken('remember_token')) {
              setToken('b-Token', data.data, {expires: 7})
            } else {
              setToken('b-Token', data.data)
            }
            this.personalUser(data.data.username)
            // $('.form-control').val('')
            // $('.setPhone').modal('hide')
            this.isShow = false
          }
        })
      } else if (this.seShow) {
        let phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/     
        if (this.setForm.phone === undefined || this.setForm.phone.length === 0) {
          this.phonePrompt = this.$t('prompt.phoneRequired')
          this.hasphone = true
          return false
        } else if (!phonereg.test(this.setForm.phone) && this.setForm.phone !== undefined && this.setForm.phone.length > 0) {
          this.phonePrompt = this.$t('prompt.phoneError')
          this.hasphone = true
          return false
        } else if (this.setForm.captcha === undefined || this.setForm.captcha.length === 0) {
          this.phoneControlPrompt = this.$t('prompt.captchaRequired')
          return false
        }
        post(`/api/setting/phone`, this.setForm).then(data => {
          this.setForm.phone = ''
          this.setForm.captcha = ''
          if (data.resultcode === 0) {
            instance = new Toast({
              message: data.message,
              duration: 1000
            })
            return false
          } else if (data.resultcode === 1) {
            instance = new Toast({
              message: data.message,
              iconClass: 'glyphicon glyphicon-ok',
              duration: 1000
            })
            this.personalUser(this.userInfo.username)
            $('.form-control').val('')
            $('.setPhone').modal('hide')
          }
        })
      }
    },
    // 获取手机验证码
    getPhoneControl () {
      let phone = parseFloat(this.setForm.phone)
      this.hasphone = true
      let that = this
      post('/api/phoneCaptcha', { 'phone': phone }).then((data) => {
        if (data.resultcode === 0) {
          if (data.message === 'failed' || data.message === '失败') {
            alert(this.$t('prompt.phoneRegistered'))
            this.hasphone = true
            return false
          }
        } else {
          this.timer = setInterval(function () {
            that.countdown--
            that.hasControl = true
            that.getcontroltxt = that.$t('prompt.reacquire')
            this.kaiguan = false
            if (that.countdown < 1) {
              that.getcontroltxt = that.$t('prompt.acquireVcode')
              that.hasphone = false
              that.countdown = 30
              that.hasControl = false
              clearInterval(that.timer)
            }
          }, 1000)
        }
      }).catch(error => {
        console.log(error)
      })
    },
    setFormBtn (id) {
      if (id === 0) {
        this.isShow = !this.isShow
        // this.showModel = true
        // $('.setPhone').modal('show')
        // document.body.removeChild(document.querySelector('.modal-backdrop'))
      } else if (id === 1) {
        this.showModel = false
        $('.setPhone').modal('show')
        this.seShow = !this.seShow
      }
    },
    closeModal () {
      $('.setPhone').hide('show')
    },
    // 个人资料
    personalUser (uname) {
      get(`/api/u/${uname}`).then(data => {
        if (data.resultcode === 0) {
          alert(this.$t('prompt.loginFirst'))
          this.$router.push({ path: '/login' })
        } else {
          this.personalUserInfo = data.data
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.prompt {
  color: red;
}
.setFormconfirm {
  color: #fff;
  background-color: #337ab7;
  border-color: #2e6da4;
  border-radius: 3px !important;
  padding: 0px 8px !important;
}
.disable {
  background: #bcbcbc !important;
  color: #797979 !important;
  border: none !important;
}
.getcontrol {
  border-radius: 4px;
  color: #fff;
  background-color: #5cb85c;
  border-color: #4cae4c;
}
.diy-title {
  text-align: center;
  font-size: 16px;
  color: #333;
}
.login-button {
  background-color: #1e8fff;
  border: none;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  margin: 40px 0 30px 48px;
  width: 362px;
  &:hover {
    color: #fff;
    background-color: #50a6fc;
  }
}
.modal-body {
  .form-space {
    padding: 40px 100px 0 50px;
  }
}
.show {
  display: none;
}
//加入样式
.info-border {
  border-bottom: solid 1px #dfdfdf;
}
.right {
  display: block;
  float: right;
  height: 80px;
}
.title {
  color: #666;
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 32px;
      height: 32px;
      display: block;
      float: left;
      margin-top: 6px;
      margin-right: 4px;
      > img {
        width: 100%;
        height: 100%;
        display: inline;
        vertical-align: text-bottom;
      }
    }
    &:nth-child(2) {
      font-size: 16px;
      font-weight: bold;
      padding-top: 4px;
    }
    &:nth-child(3) {
      font-size: 14px;
      float: right;
      color: #666;
      i {
        font-family: simsun;
        color: #666;
        padding: 0 10px;
      }
    }
  }
}
.form-group {
  color: #666;
  margin: 0 50px;
}
.form-group label {
  padding-right: 10px;
}
.personal-font {
  font-size: 14px;
  line-height: 64px;
}
.btn-edit {
  width: 60px;
  height: 32px;
  line-height: 32px;
  padding: 0;
  text-align: center;
  color: #fff;
  background: #1e8fff;
  border-radius: 4px;
  margin-top: 25px;
  float: right;
}
.edit-user-btn {
  width: 60px;
  height: 32px;
  text-align: center;
  background: #ff9612;
  border-radius: 5px;
  color: #fff;
}
.cancel-user-btn {
  width: 60px;
  height: 32px;
  text-align: center;
  background: #f0f0f0;
  border-radius: 5px;
  color: #666;
  margin-left: 15px;
  border: solid 1px #dfdfdf;
}
.margin-top {
  margin-top: 30px;
}
.center-wrap {
  width: 100%;
  min-height: 600px;
  margin: 0 auto;
}
.wrap {
  width: 100%;
  position: relative;
}
.wrap-width {
  width: 90%;
}
.left {
  float: left;
  display: block;
}
.left-width {
  width: 60%;
}
.buttons-box {
  margin: 0 0 30px 0;
}
.edit-infor label {
  font-size: 14px;
}
.yzm {
  // margin-top: 30px;
  .yzm-input {
    width: 72%;
    float: left;
    margin-right: 3%;
  }
  .yzm-button {
    width: 25%;
    float: left;
  }
}
.control-label {
  padding: 7px 0;
}
.clearfix:after {
  display: block;
  clear: both;
  content: "";
  visibility: hidden;
  height: 0;
}
.clearfix {
  zoom: 1;
}
</style>
