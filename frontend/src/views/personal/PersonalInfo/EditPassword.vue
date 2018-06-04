<style lang="scss" scoped>
.title {
  color: #666;
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 32px;
      height: 32px;
      display: block;
      float: left;
      margin-top: 6px;
      margin-right: 4px;
      > img {
        width: 100%;
        height: 100%;
        display: inline;
        vertical-align: text-bottom;
      }
    }
    &:nth-child(2) {
      font-size: 16px;
      font-weight: bold;
      padding-top: 4px;
    }
    &:nth-child(3) {
      font-size: 14px;
      float: right;
      color: #666;
      i {
        font-family: simsun;
        color: #666;
        padding: 0 10px;
      }
    }
  }
}
.password-form {
  width: 60%;
  margin: 30px auto;
  label {
    float: left;
  }
}
.btn-confirm {
  text-align: center;
  width: 60px;
  height: 32px;
  padding: 0;
  line-height: 32px;
  background: #1e8fff;
  color: #fff;
  margin-right: 20px;
  border-radius: 5px;
}
.btn-cacel {
  text-align: center;
  width: 60px;
  height: 32px;
  padding: 0;
  line-height: 32px;
  background: #f0f0f0;
  color: #666;
  border-radius: 5px;
  border: solid 1px #dfdfdf;
}
.mark {
  background: #f7f8fd;
  font-size: 14px;
  color: #666;
  padding: 4px 20px;
  margin: 20px 50px;
  span {
    float: right;
    color: #1e8fff;
  }
}
.center-wrap {
  width: 100%;
  margin: 0 auto;
  color: #666;
  font-size: 14px;
}
.wrap {
  width: 100%;
  position: relative;
}
.wrap-width {
  width: 90%;
}
.left {
  float: left;
}
.left-width {
  width: 60%;
}
.margin-top label {
  width: 22%;
  padding-right: 10px;
  text-align: left;
}
.button-box {
  padding-left: 22%;
}
.margin-top {
  margin-top: 30px;
}
.clearfix:after {
  display: block;
  clear: both;
  content: "";
  visibility: hidden;
  height: 0;
}
.clearfix {
  zoom: 1;
}
</style>
<template>
  <div class="wrap">
    <div class="center-wrap">
      <div class="title">
        <span>
          <img src="../../../assets/img/i03.png" />
        </span>
        <span>{{$t('editProfile.password')}}</span>
        <span>
          <router-link class="hover" :to="{path:'/memberCenter'}">{{$t('personalCenter.returnMyHomepage')}} <i>></i></router-link>
        </span>
      </div>
      <form class="form-horizontal password-form">
        <div class="clearfix margin-top">
          <label class="left control-label">{{$t('editProfile.originalPassword')}}</label>
          <div class="left left-width">
            <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.originalPassword')" @change='showFindPwdMsg(setPwd.OldPassword, 0)' v-model="setPwd.OldPassword">
            <p class="prompt">{{oldpwdPrompt}}</p>
          </div>
        </div>
        <div class="clearfix margin-top">
          <label class="left control-label">{{$t('editProfile.newPassword')}}</label>
          <div class="left left-width">
            <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.newPassword')" @change='showFindPwdMsg(setPwd.NewPassword, 1)' v-model="setPwd.NewPassword">
            <p class="prompt">{{newpwdPrompt}}</p>
          </div>        
        </div>
        <div class="clearfix margin-top">
          <label class="left control-label">{{$t('editProfile.confirmPassword')}}</label>
          <div class="left left-width">
            <input class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" @change='showFindPwdMsg(setPwd.confirm_password, 2)' v-model="setPwd.confirm_password">
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
        </div>
        <div class="clearfix button-box margin-top">

          <button class=" forphone btnm  btn-confirm" v-bind:disabled="!setPwd.OldPassword" @click='setPwdFun' data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
          </button>

          <button class="forphone btnm  btn-cacel">
            {{$t('button.cancel')}}
          </button>

        </div>
      </form>
    </div>
  </div>
</template>
<script>
import {post} from '../../../utils/http'
// import { Toast } from 'mint-ui'
import {getToken} from '../../../utils/auth.js'
export default {
  data () {
    return {
      setPwd: {},
      oldpwdPrompt: '',
      newpwdPrompt: '',
      confirm_upwdPrompt: '',
      user_token: ''
    }
  },
  mounted () {
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
    if (this.user_token === '') {
      this.$router.push('/')
    }
  },
  methods: {
    //   验证
    showFindPwdMsg (input, id) {
      if (id === 0) {
        if (input.length > 0) {
          post(`/api/confirmed/password`, this.setPwd).then(data => {
            if (data.resultcode === 0) {
              this.oldpwdPrompt = this.$t('prompt.orgpwdError')
              return false
            } else {
              this.oldpwdPrompt = ''
            }
          })
        }
      } else if (id === 0 || id === 1) {
        let upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
        if (upwdreg.test(input) && input !== undefined && input.length > 0) {
          if (id === 0) {
            this.oldpwdPrompt = ''
          } else if (id === 1) {
            if (input === this.setPwd.OldPassword) {
              this.newpwdPrompt = this.$t('prompt.oldpasswordDifferent')
              return false
            } else {
              this.newpwdPrompt = ''
            }
          }
        }
      } else if (id === 2) {
        if (input === this.setPwd.NewPassword && input !== undefined && input.length > 0) {
          this.confirm_upwdPrompt = ''
        } else if (input !== this.setPwd.NewPassword) {
          this.confirm_upwdPrompt = this.$t('prompt.passwordDifferent')
          return false
        }
      }
    },
    // 修改密码
    setPwdFun () {
      let upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
      if (this.setPwd.OldPassword === undefined || this.setPwd.OldPassword.length === 0) {
        this.oldpwdPrompt = this.$t('prompt.passwordRequired')
        return false
      } else if (this.oldpwdPrompt !== '') {
        this.oldpwdPrompt = this.$t('prompt.orgpwdError')
        return false
      }
      if (this.setPwd.NewPassword === undefined || this.setPwd.NewPassword === 0) {
        this.newpwdPrompt = this.$t('prompt.passwordRequired')
        return false
      } if (!upwdreg.test(this.setPwd.NewPassword) && this.setPwd.NewPassword !== undefined && this.setPwd.NewPassword.length > 0) {
        this.newpwdPrompt = this.$t('prompt.passwordLength')
        return false
      } else if (this.setPwd.confirm_password === undefined || this.setPwd.confirm_password === 0) {
        this.confirm_upwdPrompt = this.$t('prompt.passwordRequired')
        return false
      }
      post(`/api/setting/password`, this.setPwd).then(data => {
        if (data.resultcode === 1) {
          this.$router.push('/login')
        }
      })
    }
  }
}
</script>

<style>
.confirm {
  color: #fff !important;
  background-color: #337ab7 !important;
  border-color: #2e6da4 !important;
}
.prompt {
  float: left;
  margin-left: 4%;
  margin-top: 10px;
  color: red;
}
</style>
