<style lang="scss" scoped>
  .login-box{
    width:40%;
    margin:100px auto;
    border:none;
    .login-title{
      padding:20px;
      background-color: #1e8fff;
      h3{
        font-size:24px;
        letter-spacing: 2px;
      }
    }
    .panel-body{
      padding:30px 0 0 0;
      .control-label{
        text-align: left;
        font-size:14px;
      }
    }
    #register{
      background-color: #1e8fff;
      border:none;
      height:40px;
      line-height: 40px;
      font-size:18px;
      margin:25px 0;
      &:hover{
        color:#fff;
        background-color: #50a6fc;
      }
    }
  }
  .captcha-box{
    position: relative;
    .get-captcha{
      cursor: pointer;
      position: absolute;
      right:15px;
      top:0;
      background-color:rgba(255,255,255,0)!important;
      color: #1e8fff;
      width:41%;
      height:32px;
      line-height: 32px;
      text-align: right;
      span{
        color:#333;
      }
      i{
        color:#e8e8e8;
        font-size:18px;
        padding:0 10px;
      }
    }
    .text-gray{
      color:#ccc;
    }
  }
  .go-login{
    text-align: center;
    margin-bottom: 30px;
    .login-hover{
      cursor: pointer;
      &:hover{
        color:#1e8fff;
      }
    }
  }
  .prompt{
    float: left;
    margin-left: 4%;
    margin-top: 10px;
    color: red;
    padding-left:20px;
  }
</style>
<template>
  <div class="login-container">
    <div class="panel panel-primary login-box">
      <div class="panel-heading login-title">
        <h3 class="panel-title text-center">{{$t('register.title')}}</h3>
      </div>
      <div class="panel-body">
        <form action="" class="form-horizontal" style="max-width:420px;margin:auto" name="vForm" method="post">
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.username')}}</label>
            <div class="col-md-9">
              <input  class="form-control" maxlength="16" name="username" type="text" :placeholder="$t('placeholder.username')" @blur='showRegisterMsg(userForm.username, 0)'  v-model="userForm.username">
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt">{{unamePrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.password')}}</label>
            <div class="col-md-9">
              <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.password')" @blur='showRegisterMsg(userForm.password, 1)' v-model="userForm.password">
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.repassword')}}</label>
            <div class="col-md-9">
              <input class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" @blur='showRegisterMsg(userForm.confirm_password, 2)' v-model="userForm.confirm_password">
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.phone')}}</label>
            <div class="col-md-9">
              <input class="form-control" name="phone" type="text" :placeholder="$t('placeholder.phone')" v-model="userForm.phone" @blur='showRegisterMsg(userForm.phone, 3)'>
            </div>
            <label class="col-md-3 control-label"></label>
             <p class="prompt">{{phonePrompt}}</p>
          </div>
          <div class="form-group">
              <label for="inputCaptcha3" class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.vcode')}}</label>
              <div class="col-md-9 captcha-box">
                  <input type="text" class="form-control" v-model="userForm.captcha" @blur='showRegisterMsg(userForm.phone, 5)' id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
                  <button type="button" class="col-md-3 get-captcha" v-bind:disabled="hasphone" :class="{'text-gray':hasphone}" @click="getPhoneControl"><span v-show="hasControl">{{countdown}}</span><i> | </i>{{getcontroltxt}}</button>
              </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt">{{captchaPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label">&nbsp;&nbsp;&nbsp;{{$t('register.icode')}}</label>
            <div class="col-md-9">
              <input class="form-control" name="recommender_code" type="text" :placeholder="$t('placeholder.icode')" v-model="userForm.recommender_code">
            </div>
          </div>
          <button class="btn btn-primary btn-block" type="button" id="register" @click="submitForm">{{$t('register.register')}}</button>
          <h5 class="go-login">{{$t('register.hasAccount')}}<router-link class="login-hover" :to="{path:'/login'}">{{$t('register.goLogin')}}</router-link></h5>
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
      getcontroltxt: this.$t('prompt.acquireVcode'),
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
        // console.log(data)
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
          setToken('b-Token', data.data)
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
          this.phonePrompt = '手机号已注册'
        }
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>
