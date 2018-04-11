<template>
    <div class="box">
        <div class="container">
            <div class="page-header">
                <h4>找回密码</h4>
            </div>
            <form class="form-horizontal">
                <div class="form-group">
                    <label for="inputEmail3" class="col-md-1 control-label">手机号</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="inputEmail3"  @blur='showRegisterMsg(phoneObj.phone, 0)' v-model="phoneObj.phone" placeholder="请输入手机号">
                    </div>
                </div>
                <p class="prompt col-md-offset-1">{{phonePrompt}}</p>
                <br>
                <div class="form-group">
                    <label for="inputCaptcha3" class="col-md-1 control-label">验证码</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" v-model="phoneObj.captcha" @blur='showRegisterMsg(phoneObj.captcha, 1)' id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <div class="col-md-1 btnm getcontrol" style=" padding: 6px 12px !important;height: 100%;width: 10%;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{disable:hasphone}"><span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}</div>
                </div>
                <p class="prompt col-md-offset-1">{{phoneControlPrompt}}</p>
                <div class="form-group">
                    <div class="col-md-offset-2 col-md-1 btnm confirm"  data-target="#myModal" data-toggle="modal">确认
                    </div>
                </div>
            </form>
            <!-- 模态框填新密码 -->
            <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 class="modal-title" id="myModalLabel">请填写新密码</h4>
                        </div>
                        <div class="modal-body">
                            <form class="form-horizontal">
                <div class="form-group">
            <label class="col-sm-2 control-label">密码:</label>
            <div class="col-sm-4">
              <input class="form-control" name="password" type="password" placeholder="Password" @blur='showRegisterMsg(findForm.password, 2)' v-model="findForm.password">
            </div>
            <p class="prompt">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-2 control-label">确认密码:</label>
            <div class="col-sm-4">
              <input class="form-control" name="repassword" type="password" placeholder="Repassword" @blur='showRegisterMsg(findForm.confirm_password, 3)' v-model="findForm.confirm_password">
            </div>
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
            </form>
                        </div>
                    <div class="modal-footer">
                        <button type="button" class="btnm btnm-default" data-dismiss="modal">关闭</button>
                        <button type="button" class="btnm btnm-primary" @click="setnewpwd">确定</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
</template>
<script>
import {post} from '../../utils/http'
export default{
  data: function () {
    return {
      hasphone: true,
      countdown: 30,
      hasControl: false,
      timer: null,
      getcontroltxt: '获取验证码',
      phoneObj: {
        'forgetphone': '',
        'control': ''
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
  mounted: function () {
  },
  methods: {
    // 失去焦点验证
    showRegisterMsg (input, id) {
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
    getPhoneControl () {
      let phone = parseFloat(this.phoneObj.phone)
      post('/api/phoneCaptcha', {'phone': phone}).then((data) => {
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
    },
    // 填新密码
    setnewpwd () {
      post('/api/setpassword', this.findForm).then(data => {
        console.log(data)
        if (data.message === '修改成功') {
          $('.modal-backdrop').removeClass('in')
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          this.$router.push('/')
        }
      })
    }
  }
}
</script>

<style>
.prompt{
    margin-top: 10px;
    color: red;
  }
  .disable{
    background: #BCBCBC !important;
    color: #797979 !important;
    border:none !important;
}
/* .disable:hover{
    background: #BCBCBC;
    color: #797979;
} */
.confirm{
    color: #fff !important;
    background-color: #337ab7 !important;
    border-color: #2e6da4 !important;
}
.getcontrol{
    border-radius: 4px;
    color: #fff;
    background-color: #5cb85c;
    border-color: #4cae4c;
}
.btnm{
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
    border-radius: 5px;
}
</style>
