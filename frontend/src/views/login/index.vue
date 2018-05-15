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
  margin-left: 4%;
  margin-top: 10px;
  color: red;
}
</style>
<template>
  <div class="login-container">
    <div class="panel panel-primary login-box">
      <div class="panel-heading login-title">
        <h3 class="panel-title text-center">用户登录</h3>
      </div>
      <ul id="myTab" class="toggle-tab">
        <li class="toggle-login" @click="changeTab(0)">
          <a href="#home" :class="{'active-login':showTab}" data-toggle="tab">用户名登录</a>
        </li>
        <li @click="changeTab(1)" class="toggle-login">
          <a href="#ios" :class="{'active-login':!showTab}" data-toggle="tab">手机登录</a>
        </li>
      </ul>
      <div class="panel-body">
        <div id="myTabContent" class="tab-content" style="padding:0 120px 0 50px;">
          <form class="form-horizontal">
            <!-- 用户名登录 -->
            <div class="tab-pane fade active" id="home" v-show="showTab" :class="{in:showTab}">
              <div class="form-group">
                <label class="col-md-3 control-label">用户名:</label>
                <div class="col-md-9">
                  <input class="form-control" name="username" type="text" placeholder="请输入用户名" @blur='showRegisterMsg(userForm.username, 0)' v-model="userForm.username">
                </div>
                <label class="col-md-3 control-label"></label>
                <p class="prompt">{{unamePrompt}}</p>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label">密　码:</label>
                <div class="col-md-9">
                  <input class="form-control" name="password" type="password" placeholder="请输入密码" @blur='showRegisterMsg(userForm.password, 1)' v-model="userForm.password">
                </div>
                <label class="col-sm-3 control-label"></label>
                <p class="prompt">{{upwdPrompt}}</p>
              </div>
              <div class="form-group">
                <label class="col-md-3 control-label">验证码:</label>
                <div class="col-md-9">
                  <div class="input-group">
                    <input class="form-control" name="captcha" @blur='showRegisterMsg(userForm.captcha, 2)' placeholder="请输入验证码" type="text" v-model="userForm.captcha" @keyup.enter="handleLogin">
                    <span class="input-group-addon" style="padding:0;border-left:none;">
                      <img ref="captcha" :src="controlImg" alt="验证码" width="120" height="30" @click="changeControl()">
                    </span>
                  </div>
                </div>
                <label class="col-md-3 control-label"></label>
                <p class="prompt">{{captchaPrompt}}</p>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <input id="remember" v-model="userForm.remember" type="checkbox" value="y">
                  <label for="remember">记住我</label>
                  <a class="pull-right" style="margin-top:7px;" @click="toForgetPwd">忘记密码?</a>
                </div>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <button type="button" class="btn btn-primary btn-block login-button" @click="handleLogin">登陆</button>
                </div>
              </div>
              <h5 class="go-login col-md-offset-3 col-md-9">没有账号？
                <router-link class="login-hover" :to="{path:'/register'}">去注册</router-link>
              </h5>
            </div>
            <!-- 手机登录 -->
            <div class="tab-pane fade  active" id="ios" v-show="!showTab" :class="{in:!showTab}">
              <div class="form-group">
                <label class="col-md-3 control-label">手机号：</label>
                <div class="col-md-9">
                  <input class="form-control" name="phone" type="text" placeholder="请输入手机号" v-model="phoneForm.phone" @blur='showRegisterMsg(phoneForm.phone, 3)'>
                </div>
                <label class="col-md-3 control-label"></label>
                <p class="prompt col-md-9">{{phonePrompt}}</p>
              </div>
              <div class="form-group">
                <label for="inputCaptcha3" class="col-md-3 control-label">验证码：</label>
                <div class="col-md-9 captcha-box">
                  <input type="text" class="form-control" v-model="phoneForm.phonecaptcha" @blur='showRegisterMsg(phoneForm.phonecaptcha, 4)' id="inputCaptcha3" placeholder="请输入验证码">
                  <button type="button" class="col-md-3 get-captcha" v-bind:disabled="hasphone" :class="{'text-gray':hasphone}" @click="getPhoneControl">
                    <span v-show="hasControl">{{countdown}}</span>
                    <i> | </i>{{getcontroltxt}}</button>
                </div>
                <label class="col-md-3 control-label"></label>
                <p class="prompt">{{captchaPrompt}}</p>
              </div>
              <!--<div class="form-group">
                    <label for="inputCaptcha3" class="col-md-3 control-label">验证码</label>
                    <div class="col-md-5">
                      <input type="text" @blur='showRegisterMsg(phoneForm.phonecaptcha, 4)' class="form-control" v-model="phoneForm.phonecaptcha" id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <button type="button" class="col-md-3 btnm getcontrol" style=" padding: 0 !important;height: 34px;line-height: 34px;
                " @click="getPhoneControl" v-bind:disabled="hasphone" :class="{disable:hasphone}">
                      <span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}</button>
                    <p class="prompt col-md-9">
                      <label class="col-md-3 control-label"></label>{{phoneControlPrompt}}</p>
                  </div>-->
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <input id="rememberPhone" v-model="phoneForm.remember" type="checkbox" value="p">
                  <label for="rememberPhone">记住我</label>
                  <a class="pull-right" @click="toForgetPwd" style="margin-top:7px;">忘记密码?</a>
                </div>
              </div>
              <div class="form-group">
                <div class="col-md-offset-3 col-md-9">
                  <button type="button" class="btn btn-primary btn-block login-button" @click="handlePhoneLogin">登陆</button>
                </div>
              </div>
              <h5 class="go-login col-md-offset-3 col-md-9">没有账号？
                <router-link class="login-hover" :to="{path:'/register'}">去注册</router-link>
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
  data() {
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
      getcontroltxt: '获取验证码'
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
    showRegisterMsg(input, id) {
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.unamePrompt = '用户名不能为空'
          return false
        } else {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
        if (input === undefined || input.length === 0) {
          this.upwdPrompt = '密码不能为空'
          return false
        } else {
          this.upwdPrompt = ''
        }
      } else if (id === 2) {
        if (input === undefined || input.length === 0) {
          this.captchaPrompt = '验证码不能为空'
          return false
        } else {
          this.captchaPrompt = ''
        }
      } else if (id === 3) {
        if (input === undefined || input.length === 0) {
          this.phonePrompt = '手机号码不能为空'
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
            this.phoneControlPrompt = '验证码不能为空'
          }
          return false
        } else {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 用户名登录
    handleLogin() {
      if (this.userForm.username === undefined) {
        alert('用户名不能为空')
        return
      } else if (this.userForm.password === undefined) {
        alert('密码不能为空')
        return
      } else if (this.userForm.captcha === undefined) {
        alert('验证码不能为空')
        return
      }
      post(this.formUrl, this.userForm).then(data => {
        // console.log(data.data)
        // console.log(this.userForm)
        // alert(data.message)
        this.controlPrompt = data.message
        if (data.message === '验证码错误') {
          this.controlPrompt = data.message
          this.captchaPrompt = data.message
          this.changeControl()
          return
        } else {
          this.controlPrompt = ''
        }
        if (data.message === '用户名或密码错误') {
          alert(data.message)
        }
        if (data.message === '你已经登陆，不能重复登陆') {
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
            setToken(data.data, { expires: 7 })
          } else {
            setToken(data.data)
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
        alert('手机号码不能为空')
        return
      } else if (this.phoneForm.phonecaptcha === undefined) {
        alert('验证码不能为空')
        this.changeControl()
        return
      }
      post(this.phoneUrl, this.phoneForm).then(data => {
        if (data.resultcode === 0) {
          if (data.message === '你已经登陆，不能重复登陆') {
            alert(data.message)
            this.$router.push('/')
            this.changeControl()
          } if (data.message === 'failed') {
            alert('手机号未注册')
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
            setToken(data.data, { expires: 7 })
          } else {
            setToken(data.data)
          }
          this.$router.push('/')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 切换验证码
    changeControl() {
      this.controlImg = this.controlImg + '?d=' + Date.now()
    },
    // 去忘记密码
    toForgetPwd() {
      this.$router.push('/forgetPwd')
    },
    // 获取手机验证码
    getPhoneControl() {
      let phone = parseFloat(this.phoneForm.phone)
      post('/api/phoneCaptcha/login', { 'phone': phone }).then((data) => {
        if (data.resultcode === 0) {
          alert('手机号未注册')
          return
        }
        if (data.resultcode === 1) {
          this.hasphone = true
          let that = this
          this.timer = setInterval(function() {
            that.countdown--
            that.hasControl = true
            that.getcontroltxt = '重新获取'
            this.kaiguan = false
            if (that.countdown < 1) {
              that.getcontroltxt = '获取验证码'
              that.hasphone = false
              that.countdown = 30
              that.hasControl = false
              clearInterval(that.timer)
            }
          }, 1000)
        } else if (data.resultcode === 0) {
          this.phonePrompt = '手机号未注册'
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 显示当前tab
    changeTab(now) {
      if (now === 0) {
        this.showTab = true
      } else {
        this.showTab = false
      }
    }
  }
}
</script>
