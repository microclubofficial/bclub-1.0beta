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
    .get-captcha {
      height: 34px;
      line-height: 34px;
    }
  }
}

.login-button {
  background-color: #1e8fff;
  border: none;
  height: 40px;
  line-height: 40px;
  font-size: 18px;
  margin-top: 20px;
  margin-bottom: 40px;
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
          <h4>{{$t('forgetPassword.byEmail')}}</h4>
          <form class="form-horizontal clearfloat">
            <div class="form-group">
              <label for="inputEmail3" class="col-md-3 control-label">{{$t('forgetPassword.email')}}</label>
              <div class="col-md-9">
                <input type="text" class="form-control" id="inputEmail3" @blur='showRegisterMsg(findForm.email, 0)' v-model="findForm.email" :placeholder="$t('placeholder.email')">
              </div>
            </div>
            <label class="col-md-3 control-label"></label>
            <p class="prompt col-md-9" style="margin-top:0px !important;">{{emailPrompt}}</p>
            <button type="button" class="btn col-md-offset-2 col-md-10 btn-primary login-button" @click="setfindemail">{{$t('button.confirm')}}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { post } from '../../utils/http'
export default {
  data: function () {
    return {
      findForm: {
        'email': ''
      },
      emailPrompt: ''
    }
  },
  mounted: function () {

  },
  methods: {
    // 失去焦点验证
    showRegisterMsg (input, id) {
      var emailreg = /^[A-Za-z0-9.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.emailPrompt = this.$t('prompt.emailRequired')
          return false
        } else if (!emailreg.test(input) && input !== undefined && input.length > 0) {
          this.emailPrompt = this.$t('prompt.emailError')
          return false
        } else {
          this.emailPrompt = ''
        }
      }
    },
    // 填新密码
    setfindemail () {
      post('/api/forget', this.findForm).then(data => {
        if (data.resultcode === 0) {
          alert(data.message)
        }
        if (data.resultcode === 1) {
          alert(data.message)
          console.log(data)
          this.$store.commit('USER_INFO', {
            'username': data.data.username,
            'avatar': data.data.avatar,
            'isLogin': true
          })
          this.$router.push('/login')
        }
      })
    }
  }
}
</script>

<style>
.findforemai {
  color: #fff !important;
  background-color: #337ab7 !important;
  border-color: #2e6da4 !important;
}

.prompt {
  margin-top: 10px;
  color: red;
}

.btnm {
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
