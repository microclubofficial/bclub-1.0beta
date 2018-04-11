<template>
  <div class="login-container">
    <div class="panel panel-primary" style="width:30%;margin:100px auto">
      <ul id="myTab" class="nav nav-tabs">
        <li class="active"><a href="#home" data-toggle="tab">用户名登录</a></li>
        <li><a href="#ios" data-toggle="tab">手机登录</a></li>
      </ul>
      <div class="panel-body">
        <div id="myTabContent" class="tab-content">
          <form class="form-horizontal" style="max-width:420px;margin:auto">
            <!-- 用户名登录 -->
            <div class="tab-pane fade in active" id="home">
            <div class="form-group">
            <label class="col-sm-2 control-label">用户名:</label>
            <div class="col-sm-9">
              <input class="form-control" @blur='showRegisterMsg(userForm.username, 0)' name="username" type="text" placeholder="Username" v-model="userForm.username">
            </div>
            <p class="prompt">{{unamePrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">密码:</label>
            <div class="col-sm-9">
              <input class="form-control" @blur='showRegisterMsg(userForm.password, 1)' name="password" type="password" placeholder="Password" v-model="userForm.password">
            </div>
            <p class="prompt">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">验证码:</label>
            <div class="col-sm-9">
              <div class="input-group">
                <span class="input-group-addon" style="padding:0;border-right:none;">
                  <img ref="captcha" :src="controlImg" alt="验证码" width="90" height="20" @click="changeControl()">
                </span>
                <input class="form-control" name="captcha"  @blur='showRegisterMsg(userForm.captcha, 2)' placeholder="Captcha" type="text" style="border-left:none;" v-model="userForm.captcha"  @keyup.enter="handleLogin">
              </div>
            </div>
            <p class="prompt">{{captchaPrompt}}</p>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-9">
              <input id="remember" name="remember" type="checkbox" value="y">
              <label for="remember">记住我</label>
              <a class="pull-right" @click="toForgetPwd">忘记密码?</a>
            </div>
          </div>
          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-9">
              <button type="button" class="btn btn-primary btn-block" @click="handleLogin">登陆</button>
            </div>
          </div>
          </div>
          <!-- 手机登录 -->
          <div class="tab-pane fade" id="ios">
            <div class="form-group">
            <label class="col-sm-2 control-label">手机号:</label>
            <div class="col-sm-9">
              <input class="form-control" name="phone" type="text" placeholder="phone" v-model="phoneForm.phone" @blur='showRegisterMsg(phoneForm.phone, 3)'>
            </div>
             <p class="prompt">{{phonePrompt}}</p>
          </div>
                <div class="form-group">
                    <label for="inputCaptcha3" class="col-md-2 control-label">验证码</label>
                    <div class="col-md-7">
                        <input type="text" @blur='showRegisterMsg(phoneForm.phonecaptcha, 4)' class="form-control" v-model="phoneForm.phonecaptcha" id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <div class="col-md-2 btn getcontrol" style=" padding: 6px 12px !important;height: 100%;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{disable:hasphone}"><span v-show="hasControl">{{countdown}}</span>获取</div>
                    <p class="prompt">{{phoneControlPrompt}}</p>
                </div>
                <div class="form-group">
            <div class="col-sm-offset-2 col-sm-9">
              <button type="button" class="btn btn-primary btn-block" @click="handlePhoneLogin">登陆</button>
            </div>
          </div>
          </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import {post} from 'src/utils/http'
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
      showTab: true
    }
  },
  mounted () {
    $('#myTab li:eq(0) a').tab('show')
  },
  methods: {
    // 失去焦点验证
    showRegisterMsg (input, id) {
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
          this.hasphone = false
        }
      } else if (id === 4) {
        if (input === undefined || input.length === 0) {
          this.phoneControlPrompt = '验证码不能为空'
          return false
        } else {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 用户名登录
    handleLogin () {
      post(this.formUrl, this.userForm).then(data => {
        console.log(data)
        alert(data.message)
        if (data.message === '验证码错误') {
          this.controlPrompt = data.message
          this.phoneControlPrompt = data.message
          return
        } else {
          this.controlPrompt = ''
        }
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          // this.$store.state.isLogin = true
          this.$router.push('/')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 手机登录
    handlePhoneLogin () {
      post(this.phoneUrl, this.phoneForm).then(data => {
        alert(data.message)
        if (data.message === '验证码错误') {
          this.controlPrompt = data.message
          this.changeControl()
          return
        } else if (data.message === '用户名或密码错误') {
          this.changeControl()
          return
        } else {
          this.controlPrompt = ''
        }
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          // this.$store.state.isLogin = true
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
      post('/api/phoneCaptcha', {'phone': phone}).then((data) => {
        console.log(data)
        console.log(phone)
        if (data.message === '短信发送成功') {
          let that = this
          if (that.countdown === 0) {
            this.timer = setInterval(function () {
              that.countdown--
              that.hasControl = true
              if (that.countdown <= 1) {
                that.getcontroltxt = '获取验证码'
                that.hasphone = false
                that.countdown = 30
                that.hasControl = false
                clearInterval(that.timer)
              }
            }, 1000)
          } else {
            this.timer = setInterval(function () {
              that.countdown--
              that.hasControl = true
              that.getcontroltxt = '重新获取'
              that.hasphone = true
              if (that.countdown < 1) {
                that.getcontroltxt = '获取验证码'
                that.countdown = 30
                that.hasphone = false
                that.hasControl = false
                clearInterval(that.timer)
              }
            }, 1000)
          }
        }
      }).catch(error => {
        alert(error)
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.prompt{
    float: left;
    margin-left: 20%;
    margin-top: 10px;
    color: red;
}
.nav-tabs>li>a{border-radius: 0 !important;}
  .form-group>label{padding: 0 10px;}
  .disable{
    background: #BCBCBC !important;
    color: #797979 !important;
    border:none !important;
}
// .disable:hover{
//     background: #BCBCBC;
//     color: #797979;
// }
.getcontrol{
    border-radius: 4px;
    color: #fff;
    background-color: #5cb85c;
    border-color: #4cae4c;
}
.btn{
    display: inline-block;
    padding: 6px 12px;
    margin-bottom: 0;
    font-size: 14px;
    font-weight: 400;
    line-height: 1.42857143;
    text-align: center;
    white-space: nowrap;
    vertical-align: middle;
    -ms-touch-action: manipulation;
    touch-action: manipulation;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    background-image: none;
    border: 1px solid transparent;
}
</style>
