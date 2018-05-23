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
  }
}

.login-button {
  background-color: #1e8fff;
  border: none;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  margin: 40px 0 50px 30px;
  width: 380px;
  &:hover {
    color: #fff;
    background-color: #50a6fc;
  }
}

.prompt {
  margin-top: 10px;
  color: red;
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
          <h4>{{$t('forgetPassword.newPassword')}}</h4>
          <form class="form-horizontal">
            <div class="form-group">
              <label for="inputPassword3" class="col-md-3 control-label">{{$t('editProfile.newPassword')}}</label>
              <div class="col-md-9">
                <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.password')" @blur='showRegisterMsg(findForm.password, 0)' v-model="findForm.password">
              </div>
              <label class="col-md-3 control-label"></label>
              <p class="prompt col-md-9">{{upwdPrompt}}</p>
            </div>
            <div class="form-group">
              <label for="inputRepassword3" class="col-md-3 control-label">{{$t('editProfile.confirmPassword')}}</label>
              <div class="col-md-9">
                <input class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" @blur='showRegisterMsg(findForm.confirm_password, 1)' v-model="findForm.confirm_password">
              </div>
              <label class="col-md-3 control-label"></label>
              <p class="prompt col-md-9">{{confirm_upwdPrompt}}</p>
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt col-md-9" style="margin-top:0px !important;">{{emailPrompt}}</p>
            <button type="button" class="btn btn-primary btn-block login-button" @click="setnewpwd">{{$t('button.confirm')}}
            </button>
          </form>
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
      upwdPrompt: '',
      confirm_upwdPrompt: '',
      findForm: {
        'password': '',
        'confirm_password': ''
      },
      phonePrompt: ''
    }
  },
  mounted: function () {
  },
  methods: {
    //   失去焦点
    showRegisterMsg (input, id) {
      if (id === 0) {
        var upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
        if (!upwdreg.test(input) && input !== undefined && input.length > 0) {
          this.upwdPrompt = this.$t('prompt.passwordLength')
          return false
        } else if (input === undefined || input.length === 0) {
          this.upwdPrompt = this.$t('prompt.passwordRequired')
          return false
        } else {
          this.upwdPrompt = ''
        }
      } else if (id === 1) {
        if (input !== this.findForm.password && input !== undefined && input.length > 0) {
          this.confirm_upwdPrompt = this.$t('prompt.passwordDifferent')
          return false
        } else if (input === undefined || input.length === 0) {
          this.confirm_upwdPrompt = this.$t('prompt.passwordRequired')
          return false
        } else {
          this.confirm_upwdPrompt = ''
        }
      }
    },
    // 填新密码
    setnewpwd () {
      let token = this.$route.params.token
      post(`/api/setpassword/${token}`, this.findForm).then(data => {
        if (data.message === '修改成功') {
          if (data.resultcode === 1) {
            this.$store.commit('USER_INFO', {
              'username': data.data.username,
              'avatar': data.data.avatar,
              'isLogin': true
            })
            this.$router.push('/login')
          }
        }
      })
    }
  }
}
</script>

<style>
.prompt{
    margin-left: 0 !important;
    margin-top: 10px;
    color: red;
  }
  /*.disable{
    background: #BCBCBC !important;
    color: #797979 !important;
    border:none !important;
}*/
/* .disable:hover{
    background: #BCBCBC;
    color: #797979;
} */
.findpwd{
    color: #fff !important;
    background-color: #337ab7 !important;
    border-color: #2e6da4 !important;
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
