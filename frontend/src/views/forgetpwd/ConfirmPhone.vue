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
  .panel-body {
    padding: 40px 0 0 0;
    h4 {
      text-align: center;
      margin-bottom: 40px;
      padding-left: 50px;
    }
    .get-captcha{
      height:34px;
      line-height:34px;
    }
  }
}
.login-button {
  background-color: #1e8fff;
  border: none;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  margin: 40px 0 50px 48px;
  width:362px;
  &:hover {
    color: #fff;
    background-color: #50a6fc;
  }
}
.prompt {
  margin-top: 10px;
  color: red;
}
.diy-title{
  text-align: center;
  font-size:16px;
  color:#333;
}
.login-button {
  background-color: #1e8fff;
  border: none;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  margin: 40px 0 50px 48px;
  width: 362px;
  &:hover {
    color: #fff;
    background-color: #50a6fc;
  }
}

</style>
<template>
  <div>
    <div class="panel panel-primary login-box">
      <div class="panel-heading login-title">
        <h3 class="panel-title text-center">{{$t('forgetPassword.retrieve')}}</h3>
      </div>
      <div class="panel-body">
        <div class="confirm-box" style="padding:0 150px 0 100px;">
          <h4>{{$t('forgetPassword.byPhone')}}</h4>
          <form class="form-horizontal">
            <div class="form-group">
              <label for="inputEmail3" class="col-md-3 control-label">{{$t('register.phone')}}</label>
              <div class="col-md-9">
                <input type="text" class="form-control" id="inputEmail3" @blur='showRegisterMsg(phoneObj.phone, 0)' v-model="phoneObj.phone" :placeholder="$t('placeholder.phone')">
              </div>
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt col-md-9" style="margin-top:0px !important;">{{phonePrompt}}</p>
            <div class="form-group" style="margin-top: 37px;">
              <label for="inputCaptcha3" class="col-md-3 control-label">{{$t('register.vcode')}}</label>
              <div class="col-md-6">
                <input type="text" class="form-control" v-model="phoneObj.captcha" @blur='showRegisterMsg(phoneObj.captcha, 1)' id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
              </div>
              <button type="button" class="btn btn-default get-captcha" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{'btn-success':!hasphone}">
                {{getcontroltxt}}<span v-show="hasControl"> {{countdown}}</span></button>
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt col-md-9" style="margin-top:0px !important;">{{phoneControlPrompt}}</p>
            <button type="button" class="btn btn-primary btn-block login-button" @click='showModel' data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
            </button>
          </form>
        </div>
      </div>
    </div>
    <!-- 模态框填新密码 -->
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="margin-bottom:40px;">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
            <h4 class="modal-title diy-title" id="myModalLabel">{{$t('forgetPassword.newPassword')}}</h4>
          </div>
          <div class="modal-body">
            <form class="form-horizontal" style="padding:0 100px 10px 60px;">
              <div class="form-group">
                <label for="inputPassword3" class="col-md-3 control-label">{{$t('editProfile.newPassword')}}</label>
                <div class="col-md-9">
                  <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.password')" @blur='showRegisterMsg(findForm.password, 0)' v-model="findForm.password">
                </div>
                <p class="prompt">{{upwdPrompt}}</p>
              </div>
              <div class="form-group" style="margin-top:30px;">
                <label for="inputRepassword3" class="col-md-3 control-label">{{$t('editProfile.confirmPassword')}}</label>
                <div class="col-md-9">
                  <input class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" @blur='showRegisterMsg(findForm.confirm_password, 1)' v-model="findForm.confirm_password">
                </div>
                <p class="prompt">{{confirm_upwdPrompt}}</p>
              </div>
              <label class="col-md-3 control-label"></label>
              <p class="prompt col-md-9" style="margin-top:0px !important;">{{phonePrompt}}</p>
              <button type="button" class="btn btn-primary btn-block login-button" style="width:380px;margin: 30px 0 30px 30px;" @click="setnewpwd">{{$t('button.confirm')}}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { post } from '../../utils/http'
export default {
  data: function() {
    return {
      hasphone: true,
      countdown: 30,
      hasControl: false,
      timer: null,
      getcontroltxt: this.$t('prompt.acquireVcode'),
      phoneObj: {
        'phone': '',
        'captcha': ''
      },
      phonePrompt: '',
      phoneControlPrompt: '',
      upwdPrompt: '',
      confirm_upwdPrompt: '',
      findForm: {
        'password': '',
        'confirm_password': '',
        'phone': ''
      }
    }
  },
  mounted: function() {
  },
  methods: {
    // 失去焦点验证
    showRegisterMsg(input, id) {
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.phonePrompt = '手机号码不能为空'
          this.hasphone = true
          return false
        } else {
          this.phonePrompt = ''
          this.hasphone = false
          this.findForm.phone = input
        }
      } else if (id === 1) {
        if (input === undefined || input.length === 0) {
          this.phoneControlPrompt = '验证码不能为空'
          return false
        } else {
          this.phoneControlPrompt = ''
        }
      } else if (id === 2) {
        var upwdreg = /^[a-zA-Z0-9_]{6,}$/
        if (!upwdreg.test(input) && input !== undefined && input.length > 0) {
          this.upwdPrompt = '密码长度不能小于6位'
          return false
        } else if (input === undefined || input.length === 0) {
          this.upwdPrompt = '密码不能为空'
          return false
        } else {
          this.upwdPrompt = ''
        }
      } else if (id === 3) {
        if (input !== this.findForm.password && input !== undefined && input.length > 0) {
          this.confirm_upwdPrompt = '两次输入密码不一致'
          return false
        } else if (input === undefined || input.length === 0) {
          this.confirm_upwdPrompt = '确认密码不能为空'
          return false
        } else {
          this.confirm_upwdPrompt = ''
        }
      }
    },
    // 获取手机验证码
    getPhoneControl() {
      let phone = parseFloat(this.phoneObj.phone)
      post('/api/phoneCaptcha/login', { 'phone': phone }).then((data) => {
        if (data.resultcode === 1) {
          this.hasphone = true
          let that = this
          this.timer = setInterval(function() {
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
          this.phonePrompt = '手机号码未注册'
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 填新密码
    setnewpwd() {
      this.findForm.phone = parseInt(this.phoneObj.phone)
      post('/api/setpassword', this.findForm).then(data => {
        if (data.resultcode === 1) {
          $('#myModal').removeClass('in')
          $('body').removeClass('modal-open')
          document.body.removeChild(document.querySelector('.modal-backdrop'))
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          this.$router.push('/login')
        }
      })
    },
    // 显示模态框
    showModel() {
      if (this.phoneObj.phone === '') {
        this.phonePrompt = '手机号码不能为空'
        return false
      } else if (this.phoneObj.captcha === '') {
        this.phoneControlPrompt = '验证码不能为空'
        return false
      } else {
        post('/api/phoneForget', this.phoneObj).then(data => {
          if (data.message === '验证码错误') {
            this.phoneControlPrompt = '验证码错误，请重新获取'
            this.phoneObj.captcha = ''
          } else if (data.message === '手机号不存在') {
            this.phonePrompt = data.message
          } else if (data.resultcode === 1) {
            $('#myModal').modal({
              keyboard: true
            })
          }
        })
      }
    }
  }
}
</script>
