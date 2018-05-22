<template>
  <div>
    <div class="container">
      <form class="form-horizontal">
        <div class="form-group">
          <label class="col-md-2 control-label">{{$t('register.username')}}</label>
          <div class="col-md-2">
            <p class="form-control-static">{{personalUserInfo.username}}</p>
          </div>
          <div class="col-md-2">
            <div class="btnm setFormconfirm" data-target="#myModal" data-toggle="modal" @click="setFormBtn(0)">{{$t('button.edit')}}</div>
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-2 control-label">{{$t('register.phone')}}</label>
          <div class="col-md-2">
            <p class="form-control-static">{{personalUserInfo.phone}}</p>
          </div>
          <div class="col-md-2">
            <div class="btnm setFormconfirm" @click="setFormBtn(1)">{{$t('button.edit')}}</div>
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-2 control-label">{{$t('editProfile.registerTime')}}</label>
          <div class="col-md-2">
            <p class="form-control-static">{{personalUserInfo.register_time}}</p>
          </div>
        </div>
        <div class="form-group">
          <label class="col-md-2 control-label">{{$t('editProfile.lastLogin')}}</label>
          <div class="col-md-2">
            <p class="form-control-static">{{personalUserInfo.last_login}}</p>
          </div>
        </div>
      </form>
      <!-- 模态框填新密码 -->
      <div class="modal fade in setPhone" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" @click="closeModal" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h4 class="modal-title diy-title" id="myModalLabel">{{showModel ? $t('editProfile.username') : $t('editProfile.phone')}}</h4>
            </div>
            <div class="modal-body">
              <!-- 修改用户名 -->
              <form class="form-horizontal form-space" v-if="showModel">
                <div class="form-group">
                  <label for="inputEmail3" class="col-md-3 control-label">{{$t('register.username')}}</label>
                  <div class="col-md-9">
                    <input type="text" class="form-control" name="username" @blur='showsetFormMsg(setForm.username, 0)' v-model="setForm.username" maxlength="16" id="inputEmail3" :placeholder="$t('placeholder.username')">
                  </div>
                </div>
                <label class="col-md-3 control-label"></label>
                <p class="prompt col-md-9" style="margin-top:0px !important;">{{unamePrompt}}</p>
                <button type="button" class="btn btn-primary btn-block login-button"  v-bind:disabled="!setForm.username" @click="setusername" data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
                </button>
              </form>
              <!-- 修改手机号 -->
              <form class="form-horizontal form-space" v-if="!showModel">
                <div class="form-group">
                  <label for="inputEmail3" class="col-md-3 control-label">{{$t('register.phone')}}</label>
                  <div class="col-md-9">
                    <input type="text" class="form-control" id="inputEmail3" @blur='showsetFormMsg(setForm.phone, 1)' v-model="setForm.phone" :placeholder="$t('placeholder.phone')">
                  </div>
                </div>
                <p class="prompt col-md-offset-3 col-md-9" style="margin-top:0px !important;">{{phonePrompt}}</p>
                <div class="form-group" style="margin-top: 37px;">
                  <label for="inputCaptcha3" class="col-md-3 control-label">{{$t('register.vcode')}}</label>
                  <div class="col-md-6">
                    <input type="text" class="form-control" v-model="setForm.captcha" @blur='showsetFormMsg(setForm.captcha, 2)' id="inputCaptcha3" :placeholder="$t('placeholder.vcode')">
                  </div>
                  <button type="button" class="btn btn-default get-captcha" style="height:34px;line-height:34px;" @click="getPhoneControl" v-bind:disabled="hasphone" :class="{'btn-success':!hasphone}">
                    <span v-show="hasControl">{{countdown}}</span>{{getcontroltxt}}</button>
                </div>
                <p class="prompt col-md-offset-3 col-md-9" style="margin-top:0px !important;">{{phoneControlPrompt}}</p>
                <button type="button" class="btn btn-primary btn-block login-button"  v-bind:disabled="!setForm.phone" @click="setusername" data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
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
      cansetP: false
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
        if (input.indexOf(' ') >= 0) {
          this.unamePrompt = '不能输入空格'
          this.canSetU = false
          return false
        } else {
          var unamereg = /^[a-zA-Z0-9_\.\u4e00-\u9fa5]{3,16}$/
          if (!unamereg.test(input) && input !== undefined && input.length > 0) {
            this.unamePrompt = '用户名长度在3-16位之间'
            this.canSetU = false
            return false
          } else if (input === undefined || input.length === 0) {
            this.unamePrompt = '用户名不能为空'
            this.canSetU = false
            return false
          } else {
            this.unamePrompt = ''
            this.canSetU = true
          }
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
        if (input.length > 0) {
          this.phoneControlPrompt = ''
        }
      }
    },
    // 修改用户名和手机号
    setusername () {
      let instance
      if (this.showModel) {
        if (this.canSetU) {
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
              if (rememberToken('remember_token')) {
                setToken('b-Token', data.data, {expires: 7})
              } else {
                setToken('b-Token', data.data)
              }
              this.personalUser(data.data.username)
              $('.form-control').val('')
              $('.setPhone').modal('hide')
            }
          })
        }
      } else {
        if (this.setForm.captcha === undefined || this.setForm.captcha.length === 0) {
          this.phoneControlPrompt = '验证码不能为空'
          return false
        }
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
          if (data.message === 'failed') {
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
        this.showModel = true
        // $('.setPhone').modal('show')
        // document.body.removeChild(document.querySelector('.modal-backdrop'))
      } else if (id === 1) {
        this.showModel = false
        $('.setPhone').modal('show')
      }
    },
    closeModal () {
      $('.setPhone').hide('show')
    },
    // 个人资料
    personalUser (uname) {
      get(`/api/u/${uname}`).then(data => {
        if (data.message === '未登录') {
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
  background: #BCBCBC !important;
  color: #797979 !important;
  border: none !important;
}

.getcontrol {
  border-radius: 4px;
  color: #fff;
  background-color: #5cb85c;
  border-color: #4cae4c;
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
  margin: 40px 0 30px 48px;
  width: 362px;
  &:hover {
    color: #fff;
    background-color: #50a6fc;
  }
}

.modal-body{
  .form-space{
    padding:40px 100px 0 50px;
  }
}
.show {
  display: none;
}
</style>
