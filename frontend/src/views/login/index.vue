<style lang="scss" scoped>
.login-box {
  width: 40%;
  margin: 100px auto;
  border: none;
  .login-title {
    padding: 20px;
    background-color: #1e8fff;
    h3 {
      font-size: 24px;
      letter-spacing: 2px;
    }
  }
  .toggle-tab {
    display: flex;
    margin-top: 10px;
    .toggle-login {
      flex: 1;
      text-align: center;
      font-size: 18px;
      // font-weight:bold;
      padding:10px 0;
    }
  }
  .active-login {
    border-bottom: 4px solid #1e8fff;
    border-radius: 2px;
    display: inline-block;
    padding:0 5px 10px;
  }
  .panel-body {
    padding: 30px 0 0 0;
    .control-label {
      // text-align: left;
      font-size: 14px;
    }
  }
  .login-button {
    background-color: #1e8fff;
    border: none;
    height: 40px;
    line-height: 40px;
    font-size: 18px;
    margin: 10px 0;
    &:hover {
      color: #fff;
      background-color: #50a6fc;
    }
  }
}

.captcha-box {
  position: relative;
  .get-captcha {
    cursor: pointer;
    position: absolute;
    right: 15px;
    top: 0;
    background-color:rgba(255,255,255,0)!important;
    color: #1e8fff;
    width: 41%;
    height: 32px;
    line-height: 32px;
    text-align: right;
    span {
      color: #333;
    }
    i {
      color: #e8e8e8;
      font-size: 18px;
      padding: 0 10px;
    }
  }
  .text-gray {
    color: #ccc;
  }
}

.go-login {
  text-align: center;
  margin-bottom:30px;
  .login-hover {
    cursor: pointer;
    &:hover {
      color: #1e8fff;
    }
  }
}

.prompt {
  float: left;
  /*margin-left: 4%;*/
  margin-top: 10px;
  color: red;
}
</style>
<template>
  <div class="login-container">
    <div class="panel panel-primary login-box">
      <div class="panel-heading login-title">
        <h3 class="panel-title text-center">{{$t('login.title')}}</h3>
      </div>
      <ul id="myTab" class="toggle-tab">
        <li class="toggle-login" @click="changeTab(0)">
          <a href="#home" :class="{'active-login':showTab}" data-toggle="tab">{{$t('login.byUsername')}}</a>
        </li>
        <li @click="changeTab(1)" class="toggle-login">
          <a href="#ios" :class="{'active-login':!showTab}" data-toggle="tab">{{$t('login.byPhone')}}</a>
        </li>
      </ul>
      <div class="panel-body">
        <div id="myTabContent" class="tab-content" style="padding:0 120px 0 50px;">
          <form class="form-horizontal">
            <!-- 用户名登录 -->
            <div class="tab-pane fade active" id="home" v-show="showTab" :class="{in:showTab}">
              <div class="form-group">
                <label class="col-md-3 control-label">{{$t('login.username')}}</label>
                <div class="col-md-9">
                  <input class="form-control" name="username" type="text" :placeholder="$t('placeholder.username')" @change='showRegisterMsg(userForm.username, 0)' v-model="userForm.username">
                </div>
                <!--<label class="col-md-3 control-label"></label>-->
                <p class="prompt col-md-offset-3 col-md-9" style="margin-top:0px!important;margin-left:25%!important;">{{unamePrompt}}</p>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label">{{$t('login.password')}}</label>
                <div class="col-md-9">
                  <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.password')" @change='showRegisterMsg(userForm.password, 1)' v-model="userForm.password">
                </div>
                <!--<label class="col-sm-3 control-label"></label>-->
                <p class="prompt col-md-offset-3 col-md-9" style="margin-top:0px!important;margin-left:25%!important;">{{upwdPrompt}}</p>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label">{{$t('login.vcode')}}</label>
                <div class="col-md-9">
                  <div class="input-group">
                    <input class="form-control" name="captcha" @change='showRegisterMsg(userForm.captcha, 2)' :placeholder="$t('placeholder.vcode')" type="text" v-model="userForm.captcha" @keyup.enter="handleLogin">
                    <span class="input-group-addon" style="padding:0;border-left:none;">
                      <img ref="captcha" :src="controlImg" :alt="$t('placeholder.vcode')" width="120" height="30" @click="changeControl()">
                    </span>
                  </div>
                </div>
                <!--<label class="col-md-3 control-label"></label>-->
                <p class="prompt col-md-offset-3 col-md-9" style="margin-top:0px!important;margin-left:25%!important;">{{captchaPrompt}}</p>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <input id="remember" v-model="userForm.remember" type="checkbox" value="y">
                  <label for="remember">{{$t('login.rememberMe')}}</label>
                  <a class="pull-right" style="margin-top:7px;" @click="toForgetPwd">{{$t('login.forgetPwd')}}</a>
                </div>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <button type="button" class="btn btn-primary btn-block login-button" @click="handleLogin">{{$t('login.login')}}</button>
                </div>
              </div>
              <h5 class="go-login col-md-offset-3 col-md-9">{{$t('login.noAccount')}}
                <router-link class="login-hover" :to="{path:'/register'}">{{$t('login.goRegister')}}</router-link>
              </h5>
            </div>
            <!-- 手机登录 -->
            <div class="tab-pane fade  active" id="ios" v-show="!showTab" :class="{in:!showTab}">
              <div class="form-group">
                <label class="col-md-3 control-label">{{$t('login.phone')}}</label>
                <div class="col-md-9">
                  <input class="form-control" name="phone" type="text" :placeholder="$t('placeholder.phone')" v-model="phoneForm.phone" @change='showRegisterMsg(phoneForm.phone, 3)'>
                </div>
                <!--<label class="col-md-3 control-label"></label>-->
                <p class="prompt col-md-offset-3 col-md-6" style="margin-top:0px!important;margin-left:25%!important;">{{phonePrompt}}</p>
              </div>
              <div class="form-group">
                <label for="inputCaptcha3" class="col-md-3 control-label">{{$t('login.vcode')}}</label>
                <div class="col-md-9 captcha-box">
                  <input type="text" class="form-control" v-model="phoneForm.phonecaptcha" @change='showRegisterMsg(phoneForm.phonecaptcha, 4)' id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
                  <button type="button" class="col-md-3 get-captcha" v-bind:disabled="hasphone" :class="{'text-gray':hasphone}" @click="getPhoneControl">
                    <span v-show="hasControl">{{countdown}}</span>
                    <i> | </i>{{getcontroltxt}}</button>
                </div>
                <!--<label class="col-md-3 control-label"></label>-->
                <p class="prompt col-md-offset-3 col-md-6" style="margin-top:0px!important;margin-left:25%!important;">{{captchaPrompt}}</p>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <input id="rememberPhone" v-model="phoneForm.remember" type="checkbox" value="p">
                  <label for="rememberPhone">{{$t('login.rememberMe')}}</label>
                  <a class="pull-right" @click="toForgetPwd" style="margin-top:7px;">{{$t('login.forgetPwd')}}</a>
                </div>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <button type="button" class="btn btn-primary btn-block login-button" @click="handlePhoneLogin">{{$t('login.login')}}</button>
                </div>
              </div>
              <h5 class="go-login col-md-offset-3 col-md-9">{{$t('login.noAccount')}}
                <router-link class="login-hover" :to="{path:'/register'}">{{$t('login.goRegister')}}</router-link>
              </h5>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { post } from 'src/utils/http'
import { setToken } from '../../utils/auth'
export default {
  name: 'login',
  data () {
    return {
      userForm: {},
      phoneForm: {},
      formUrl: '/api/login',
      phoneUrl: '/api/phoneLogin',
      unamePrompt: '',
      upwdPrompt: '',
      captchaPrompt: '',
      phonePrompt: '',
      phoneControlPrompt: '',
      controlImg: '/api/captcha',
      hasphone: true,
      hasControl: false,
      countdown: 30,
      showTab: true,
      remember: '',
      getcontroltxt: this.$t('prompt.acquireVcode')
    }
  },
  mounted () {
    $('#myTab li:eq(0) a').tab('show')
    if ($('div').hasClass('modal-backdrop')) {
      document.body.removeChild(document.querySelector('.modal-backdrop'))
    }
    this.changeControl()
  },
  methods: {
    // 失去焦点验证
    showRegisterMsg (input, id) {
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.unamePrompt = this.$t('prompt.usernameRequired')
          return false
        } else {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
        if (input === undefined || input.length === 0) {
          this.upwdPrompt = this.$t('prompt.passwordRequired')
          return false
        } else {
          this.upwdPrompt = ''
        }
      } else if (id === 2) {
        if (input === undefined || input.length === 0) {
          this.captchaPrompt = this.$t('prompt.captchaRequired')
          return false
        } else {
          this.captchaPrompt = ''
        }
      } else if (id === 3) {
        var phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/        
        if (input === undefined || input.length === 0) {
          this.phonePrompt = this.$t('prompt.phoneRequired')
          this.hasphone = true
          return false
        } else if (!phonereg.test(input) && input !== undefined && input.length > 0) {
          this.phonePrompt = this.$t('prompt.phoneError')
          this.hasphone = true
          return false
        } else {
          this.phonePrompt = ''
          if (this.countdown === 30) {
            this.hasphone = false
          }
        }
      } else if (id === 4) {
        if (input === undefined || input.length === 0) {
          if (this.hasphone) {
            this.phoneControlPrompt = this.$t('prompt.captchaRequired')
          }
          return false
        } else {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 用户名登录
    handleLogin () {
      if (this.userForm.username === undefined) {
        alert(this.$t('prompt.usernmaeRequired'))
        return
      } else if (this.userForm.password === undefined) {
        alert(this.$t('prompt.passwordRequired'))
        return
      } else if (this.userForm.captcha === undefined) {
        alert(this.$t('prompt.captchaRequired'))
        return
      }
      post(this.formUrl, this.userForm).then(data => {
        // console.log(data.data)
        // console.log(this.userForm)
        // alert(data.message)
        this.controlPrompt = data.message
        if (data.message === '验证码错误' || data.message === 'Captcha error') {
          this.controlPrompt = data.message
          this.captchaPrompt = data.message
          this.changeControl()
          return
        } else {
          this.controlPrompt = ''
        }
        if (data.message === '用户名或密码错误' || data.message === 'Username or Password Error') {
          alert(data.message)
        }
        if (data.message === '你已登陆，不能重复登陆' || data.message === 'You have loggen in, no need to login again') {
          alert(data.message)
          this.changeControl()
          this.$router.push('/')
        }
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })

          if (this.userForm.remember) {
            setToken('b-Token', data.data, { expires: 7 })
          } else {
            setToken('b-Token', data.data)
          }
          this.changeControl()
          this.$router.push('/')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 手机登录
    handlePhoneLogin () {
      if (this.phoneForm.phone === undefined) {
        alert(this.$t('prompt.phoneRequired'))
        return
      } else if (this.phoneForm.phonecaptcha === undefined) {
        alert(this.$t('prompt.captchaRequired'))
        this.changeControl()
        return
      }
      post(this.phoneUrl, this.phoneForm).then(data => {
        if (data.resultcode === 0) {
          if (data.message === '你已登陆，不能重复登陆' || data.message === 'You have loggen in, no need to login again') {
            alert(data.message)
            this.$router.push('/')
            this.changeControl()
          } if (data.message === 'failed' ||　ata.message === '失败') {
            alert(this.$t('prompt.phoneNotRegistered'))
            return
          } else {
            this.controlPrompt = data.message
            this.changeControl()
            return
          }
        }
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          if (this.phoneForm.remember) {
            setToken('b-Token', data.data, { expires: 7 })
          } else {
            setToken('b-Token', data.data)
          }
          this.$router.push('/')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 切换验证码
    changeControl () {
      this.controlImg = this.controlImg + '?d=' + Date.now()
    },
    // 去忘记密码
    toForgetPwd () {
      this.$router.push('/forgetPwd')
    },
    // 获取手机验证码
    getPhoneControl () {
      let phone = parseFloat(this.phoneForm.phone)
      post('/api/phoneCaptcha/login', { 'phone': phone }).then((data) => {
        if (data.resultcode === 0) {
          alert(this.$t('prompt.phoneNotRegistered'))
          return
        }
        if (data.resultcode === 1) {
          this.hasphone = true
          let that = this
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
        } else if (data.resultcode === 0) {
          this.phonePrompt = this.$t('prompt.phoneNotRegistered')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 显示当前tab
    changeTab (now) {
      if (now === 0) {
        this.showTab = true
      } else {
        this.showTab = false
      }
    }
  }
}
</script>
