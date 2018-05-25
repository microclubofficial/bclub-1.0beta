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
    /*margin-left: 4%;*/
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
              <input  class="form-control" maxlength="16" name="username" type="text" :placeholder="$t('placeholder.username')" @change='showRegisterMsg(userForm.username,0)'  v-model="userForm.username">
            </div>
            <!--<label class="col-md-3 control-label"></label>-->
            <p class="prompt col-md-offset-3 col-md-9" style="margin-left:25%!important;">{{unamePrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.password')}}</label>
            <div class="col-md-9">
              <input @change='showRegisterMsg(userForm.password,1)' class="form-control" name="password" type="password" :placeholder="$t('placeholder.password')" v-model="userForm.password">
            </div>
            <!--<label class="col-md-3 control-label"></label>-->
            <p class="prompt col-md-offset-3 col-md-9" style="margin-left:25%!important;">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.repassword')}}</label>
            <div class="col-md-9">
              <input @change='showRegisterMsg(userForm.confirm_password,2)' class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" v-model="userForm.confirm_password">
            </div>
            <!--<label class="col-md-3 control-label"></label>-->
            <p class="prompt col-md-offset-3 col-md-9" style="margin-left:25%!important;">{{confirm_upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.phone')}}</label>
            <div class="col-md-9">
              <input @change='showRegisterMsg(userForm.phone,3)' class="form-control" name="phone" type="text" :placeholder="$t('placeholder.phone')" v-model="userForm.phone">
            </div>
            <!--<label class="col-md-3 control-label"></label>-->
             <p class="prompt col-md-offset-3 col-md-9" style="margin-left:25%!important;">{{phonePrompt}}</p>
          </div>
          <div class="form-group">
              <label for="inputCaptcha3" class="col-md-3 control-label"><span class="text-red">* </span>{{$t('register.vcode')}}</label>
              <div class="col-md-9 captcha-box">
                  <input type="text" class="form-control" @change='showRegisterMsg(userForm.captcha,4)' v-model="userForm.captcha" id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
                  <button type="button" class="col-md-3 get-captcha" v-bind:disabled="hasphone" :class="{'text-gray':hasphone}" @click="getPhoneControl"><span v-show="hasControl">{{countdown}}</span><i> | </i>{{getcontroltxt}}</button>
              </div>
            <!--<label class="col-md-3 control-label"></label>-->
            <p class="prompt col-md-offset-3 col-md-9" style="margin-left:25%!important;">{{captchaPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-md-3 control-label">&nbsp;&nbsp;&nbsp;{{$t('register.icode')}}</label>
            <div class="col-md-9">
              <input class="form-control" @change='showRegisterMsg(userForm.recommender_code,5)' name="recommender_code" type="text" :placeholder="$t('placeholder.icode')" v-model="userForm.recommender_code">
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
        var unamereg = /^[a-zA-Z0-9_.\-\u4e00-\u9fa5]{3,16}$/
        if (unamereg.test(input) && input !== undefined && input.length > 0) {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
        var upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
        if (upwdreg.test(input) && input !== undefined && input.length > 0) {
          this.upwdPrompt = ''
        }
      } else if (id === 2) {
        if (input !== this.userForm.password) {
          this.confirm_upwdPrompt = this.$t('prompt.passwordDifferent')
          return false
        } else if (input === this.userForm.password && input !== undefined && input.length > 0) {
          this.confirm_upwdPrompt = ''
        }
      } else if (id === 3) {
        var phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/
        if (phonereg.test(input) && input !== undefined && input.length > 0) {
          this.phonePrompt = ''
          this.hasphone = false
        }
      } else if (id === 4) {
        if (input !== undefined || input.length > 0) {
          this.captchaPrompt = ''
        }
      }
    },
    submitForm () {
      // 用户名验证
      let unamereg = /^[a-zA-Z0-9_.\-\u4e00-\u9fa5]{3,16}$/
      // 密码验证
      let upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
      // 手机号验证
      let phonereg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/
      if (this.userForm.username === undefined || this.userForm.username.length === 0) {
        this.unamePrompt = this.$t('prompt.usernameRequired')
        return false
      } else if (!unamereg.test(this.userForm.username) && this.userForm.username !== undefined && this.userForm.username.length > 0) {
        this.unamePrompt = this.$t('prompt.usernameLength')
        return false
        // 以下--- 密码
      } else if (this.userForm.password === undefined || this.userForm.password.length === 0) {
        this.upwdPrompt = this.$t('prompt.passwordRequired')
        return false
      } else if (!upwdreg.test(this.userForm.password) && this.userForm.password !== undefined && this.userForm.password.length > 0) {
        this.upwdPrompt = this.$t('prompt.passwordLength')
        return false
        // 以下 -- 确认密码
      } else if (this.userForm.confirm_password === undefined || this.userForm.confirm_password.length === 0) {
        this.confirm_upwdPrompt = this.$t('prompt.passwordRequired')
        return false
        // 以下 -- 手机号
      } else if (this.userForm.phone === undefined || this.userForm.phone.length === 0) {
        this.phonePrompt = this.$t('prompt.phoneRequired')
        this.hasphone = true
        return false
      } else if (!phonereg.test(this.userForm.phone) && this.userForm.phone !== undefined && this.userForm.phone.length > 0) {
        this.phonePrompt = this.$t('prompt.phoneError')
        this.hasphone = true
        return false
        // 以下 -- 验证码
      } else if (this.userForm.captcha === undefined || this.userForm.captcha.length === 0) {
        this.captchaPrompt = this.$t('prompt.captchaRequired')
        return false
      }
      post(this.formUrl, this.userForm).then(data => {
        // console.log(data)
        if (data.resultcode === 0) {
          this.unamePrompt = data.message
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
