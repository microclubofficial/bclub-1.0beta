<template>
  <div class="login-container">
    <div class="panel panel-primary" style="width:30%;margin:100px auto">
      <div class="panel-heading">
        <a href="/login" style="color:#fff">Register</a>
      </div>
      <div class="panel-body">
        <form action="" class="form-horizontal" style="max-width:420px;margin:auto" name="vForm" method="post">
          <div class="form-group">
            <label class="col-sm-2 control-label">用户名:</label>
            <div class="col-sm-9">
              <input  class="form-control" name="username" type="text" placeholder="Username" @blur='showRegisterMsg(userForm.username, 0)'  v-model="userForm.username">
            </div>
            <label class="col-sm-2 control-label"></label>
            <p class="prompt">{{unamePrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">密码:</label>
            <div class="col-sm-9">
              <input class="form-control" name="password" type="password" placeholder="Password" @blur='showRegisterMsg(userForm.password, 1)' v-model="userForm.password">
            </div>
            <label class="col-sm-2 control-label"></label>
            <p class="prompt">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">确认密码:</label>
            <div class="col-sm-9">
              <input class="form-control" name="repassword" type="password" placeholder="Repassword" @blur='showRegisterMsg(userForm.confirm_password, 2)' v-model="userForm.confirm_password">
            </div>
            <label class="col-sm-2 control-label"></label>
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
          <!-- <div class="form-group">
            <label class="col-sm-2 control-label">邮箱:</label>
            <div class="col-sm-9">
              <input class="form-control" name="emai" type="mail" placeholder="emai" v-model="userForm.email" @blur='showRegisterMsg(userForm.email, 4)'>
            </div>
            <p class="prompt">{{emailPrompt}}</p>
          </div> -->

          <!-- <div class="form-group">
            <label class="col-sm-2 control-label">验证码:</label>
            <div class="col-sm-9">
              <div class="input-group">
                <span class="input-group-addon" style="padding:0;border-right:none;">
                  <img ref="captcha" :src="controlImg" alt="验证码" width="90" height="20" @click="changeControl()">
                </span>
                <input class="form-control" name="captcha" placeholder="Captcha" type="text" style="border-left:none;" v-model="userForm.captcha" @blur='showRegisterMsg(userForm.captcha, 5)'>
              </div>
              <p class="prompt">{{captchaPrompt}}</p>
            </div>
          </div> -->
          <div class="form-group">
            <label class="col-sm-2 control-label">手机号:</label>
            <div class="col-sm-9">
              <input class="form-control" name="phone" type="text" placeholder="phone" v-model="userForm.phone" @blur='showRegisterMsg(userForm.phone, 3)'>
            </div>
            <label class="col-sm-2 control-label"></label>
             <p class="prompt">{{phonePrompt}}</p>
          </div>
                <div class="form-group">
                    <label for="inputCaptcha3" class="col-md-2 control-label">验证码</label>
                    <div class="col-md-6">
                        <input type="text" class="form-control" v-model="userForm.captcha" @blur='showRegisterMsg(userForm.phone, 5)' id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <button class="col-md-3 btnm getcontrol" type="button" style="padding: 0 !important;height: 34px;line-height: 34px;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{disable:hasphone}"><span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}</button>
                  <label class="col-sm-2 control-label"></label>
                  <p class="prompt">{{captchaPrompt}}</p>
                </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">邀请码:</label>
            <div class="col-sm-9">
              <input class="form-control" name="username" type="text" placeholder="邀请码" v-model="userForm.recommender_code">
            </div>
          </div>

          <div class="form-group">
            <div class="col-sm-offset-2 col-sm-9 btnm submitForm" id="register" @click="submitForm">注册
            </div>
          </div>
           <h5 style='text-align:center;cursor: pointer'>已注册？<router-link :to="{path:'/login'}">登录</router-link></h5>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import {post} from 'src/utils/http'
import { setToken } from '../../utils/auth'
export default {
  name: 'login',
  data () {
    return {
      userForm: {},
      formUrl: '/api/register',
      unamePrompt: '',
      upwdPrompt: '',
      confirm_upwdPrompt: '',
      phonePrompt: '',
      emailPrompt: '',
      controlImg: '/api/captcha',
      captchaPrompt: '',
      hasphone: true,
      countdown: 30,
      hasControl: false,
      getcontroltxt: '获取验证码',
      timer: null,
      kaiguan: true
    }
  },
  methods: {
    changVcode () {
      // console.log(this.$refs.captcha);
    },
    // 失去焦点验证
    showRegisterMsg (input, id) {
      if (id === 0) {
        var unamereg = /^[a-zA-Z0-9_\u4e00-\u9fa5]{3,16}$/
        if (!unamereg.test(input) && input !== undefined && input.length > 0) {
          this.unamePrompt = '用户名在3-16位之间(数字、大小写字母、下划线、中文)'
          // console.log(input.length)
          return false
        } else if (input === undefined || input.length === 0) {
          this.unamePrompt = '用户名不能为空'
          return false
        } else {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
        var upwdreg = /^[a-zA-Z0-9_]{6,}$/
        if (!upwdreg.test(input) && input !== undefined && input.length > 0) {
          this.upwdPrompt = '密码长度不能小于6位(大小写字母、数字)'
          return false
        } else if (input === undefined || input.length === 0) {
          this.upwdPrompt = '密码不能为空'
          return false
        } else {
          this.upwdPrompt = ''
        }
      } else if (id === 2) {
        if (input !== this.userForm.password && input !== undefined && input.length > 0) {
          this.confirm_upwdPrompt = '两次输入密码不一致'
          return false
        } else if (input === undefined || input.length === 0) {
          this.confirm_upwdPrompt = '确认密码不能为空'
          return false
        } else {
          this.confirm_upwdPrompt = ''
        }
      } else if (id === 3) {
        var ponereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/
        if (!ponereg.test(input) && input !== undefined && input.length > 0) {
          this.phonePrompt = '手机号码格式不正确'
          this.hasphone = true
          return false
        } else if (input === undefined || input.length === 0) {
          this.phonePrompt = '手机号码不能为空'
          this.hasphone = true
          return false
        } else {
          this.phonePrompt = ''
          this.hasphone = false
        }
      } else if (id === 5) {
        if (input === undefined || input.length === 0) {
          this.captchaPrompt = '验证码不能为空'
          return false
        } else {
          this.captchaPrompt = ''
        }
      }
    },
    submitForm () {
      post(this.formUrl, this.userForm).then(data => {
        if (data.resultcode === 0) {
          alert(data.message)
          return
        }
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          setToken(data.data)
          this.$router.push('/')
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 验证码切换
    changeControl () {
      this.controlImg = this.controlImg + '?d=' + Date.now()
    },
    // 获取手机验证码
    getPhoneControl () {
      let phone = parseFloat(this.userForm.phone)     
      post('/api/phoneCaptcha', {'phone': phone}).then((data) => {
        if (data.resultcode === 1) {
          this.hasphone = true
          let that = this
          this.timer = setInterval(function () {
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
          this.phonePrompt = '手机号已注册'
        }
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
  .prompt{
    float: left;
    margin-left: 4%;
    margin-top: 10px;
    color: red;
  }
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
.submitForm{
    color: #fff;
    background-color: #337ab7;
    border-color: #2e6da4;
}
</style>
