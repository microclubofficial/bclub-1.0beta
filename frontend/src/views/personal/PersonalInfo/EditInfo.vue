<template>
    <div>
        <div class="container">
            <form class="form-horizontal">
                <div class="form-group">
                    <label class="col-md-1 control-label">用户名:</label>
                    <div class="col-md-2">
                        <p class="form-control-static">{{userInfo.username}}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="btnm setFormconfirm" data-target="#myModal" data-toggle="modal" @click="setFormBtn(0)">修改</div>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-md-1 control-label">手机号:</label>
                    <div class="col-md-2">
                        <p class="form-control-static">{{personalUserInfo.phone}}</p>
                    </div>
                    <div class="col-md-2">
                        <div class="btnm setFormconfirm" data-target="#myModal" data-toggle="modal" @click="setFormBtn(1)">修改</div>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-md-1 control-label">注册时间:</label>
                    <div class="col-md-2">
                        <p class="form-control-static">{{personalUserInfo.register_time}}</p>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-md-1 control-label">上次登录:</label>
                    <div class="col-md-2">
                        <p class="form-control-static">{{personalUserInfo.last_login}}</p>
                    </div>
                </div>
            </form>
            <!-- 模态框填新密码 -->
            <div class="modal fade in" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" @click="closeModal" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                            <h4 class="modal-title" id="myModalLabel">请填写用户名</h4>
                        </div>
                        <div class="modal-body">
                            <!-- 找用户名 -->
                            <form class="form-horizontal" v-if="showModel">
                <div class="form-group">
            <label class="col-sm-2 control-label">用户名:</label>
            <div class="col-sm-4">
              <input class="form-control" name="username" type="text" placeholder="usernanme" @blur='showsetFormMsg(setForm.username, 0)' v-model="setForm.username">
            </div>
            <p class="prompt" style="height:34px;line-height: 34px;">{{unamePrompt}}</p>
          </div>
            </form>
            <!-- 找手机 -->
            <form class="form-horizontal" v-if="!showModel">
                <div class="form-group">
                    <label for="inputEmail3" class="col-md-2 control-label">手机号</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="inputEmail3"  @blur='showsetFormMsg(setForm.phone, 1)' v-model="setForm.phone" placeholder="请输入手机号">
                    </div>
                </div>
                <p class="prompt col-md-offset-2">{{phonePrompt}}</p>
                <div class="form-group">
                    <label for="inputCaptcha3" class="col-md-2 control-label">验证码</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" v-model="setForm.captcha" @blur='showsetFormMsg(setForm.captcha, 2)' id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <button type="button" class="col-md-2 btnm getcontrol" style="padding: 0 !important;height: 34px;line-height: 34px;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{disable:hasphone}"><span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}</button>
                </div>
                <p class="prompt col-md-offset-2">{{phoneControlPrompt}}</p>
            </form>
                        </div>
                    <div class="modal-footer">
                        <button type="button" class="btnm btn-default" @click="closeModal" data-dismiss="modal">关闭</button>
                        <button type="button" class="btnm btn-primary" @click="setusername">确定</button>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>
<script>
import {get, post} from '../../../utils/http'
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
      getcontroltxt: '获取验证码',
      phonePrompt: '',
      phoneControlPrompt: ''
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  created: function () {
    // 个人资料
    this.personalUser(this.userInfo.username)
  },
  mounted () {
  },
  methods: {
    //   验证
    showsetFormMsg (input, id) {
      if (id === 0) {
        var unamereg = /^[a-zA-Z0-9_\u4e00-\u9fa5]{3,16}$/
        if (!unamereg.test(input) && input !== undefined && input.length > 0) {
          this.unamePrompt = '用户名长度在3-16位之间'
          return false
        } else if (input === undefined || input.length === 0) {
          this.unamePrompt = '用户名不能为空'
          return false
        } else {
          this.unamePrompt = ''
        }
      } else if (id === 1) {
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
          this.setForm.phone = input
        }
      } else if (id === 2) {
        if (input === undefined || input.length === 0) {
          this.phoneControlPrompt = '验证码不能为空'
          return false
        } else {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 修改用户名和手机号
    setusername () {
      let instance
      if (this.showModel) {
        post(`/api/setting/username`, this.setForm).then(data => {
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
            this.personalUser(data.data.username)
            $('.modal').css({'display': 'none'})
            $('.modal').removeClass('in')
            document.body.removeChild(document.querySelector('.modal-backdrop'))
          }
        })
      } else {
        post(`/api/setting/phone`, this.setForm).then(data => {
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
            $('.modal').css({'display': 'none'})
            $('.modal').removeClass('in')
            $('#myModal').css({'display': 'none'})
            document.body.removeChild(document.querySelector('.modal-backdrop'))
          }
        })
      }
    },
    // 获取手机验证码
    getPhoneControl () {
      let phone = parseFloat(this.setForm.phone)
      this.hasphone = true
      let that = this
      post('/api/phoneCaptcha', {'phone': phone}).then((data) => {
        if (data.resultcode === 0) {
          if (data.message === 'failed') {
            alert('手机号已注册')
            this.hasphone = false
            return false
          }
        } else {
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
        }
      }).catch(error => {
        console.log(error)
      })
    },
    setFormBtn (id) {
      if (id === 0) {
        this.showModel = true
        $('.modal').css({'display': 'block'})
      } else {
        this.showModel = false
        $('.modal').css({'display': 'block'})
      }
    },
    closeModal () {
      $('.modal').css({'display': 'none'})
      $('.modal').removeClass('in')
      document.body.removeChild(document.querySelector('.modal-backdrop'))
    },
    // 个人资料
    personalUser (uname) {
      get(`/api/u/${uname}`).then(data => {
        this.personalUserInfo = data.data
      })
    }
  }
}
</script>
<style>
.prompt{
    color: red;
  }
.setFormconfirm{
    color: #fff;
    background-color: #337ab7;
    border-color: #2e6da4;
    border-radius: 3px !important;
    padding: 0px 8px !important;
}
.disable{
    background: #BCBCBC !important;
    color: #797979 !important;
    border:none !important;
}
.getcontrol{
    border-radius: 4px;
    color: #fff;
    background-color: #5cb85c;
    border-color: #4cae4c;
}
.modal-footer{
    border-top: none !important;
    padding-top: 0 !important;
}
.show{display: none;}
</style>
