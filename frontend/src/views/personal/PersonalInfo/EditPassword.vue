<style lang="scss" scoped>
.title {
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 32px;
      height: 24px;
      display: inline-block;

      >img {
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
  width: 320px;
  margin: 30px auto;
  label {
    width: 90px;
    float: left;
  }
  input {
    width: 220px;
  }
}

.btn-confirm {
  width: 60px;
  padding: 4px 8px;
  background: #1e8fff;
  color: #fff;
}

.btn-cacel {
  width: 60px;
  padding: 4px 8px;
  background: #f0f0f0;
  color: #666;
  border-radius: 5px;
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
}
.wrap {
  width: 100%;
  position: relative;

}

.wrap-width {
  width: 90%;
}
</style>
<template>
  <div class="wrap">
    <div class="center-wrap">
      <div class="title">
        <span>
          <img src="../../../assets/img/personal.png" />
        </span>
        <span>修改密码</span>
        <span>
          <router-link class="hover" :to="{path:'/memberCenter'}">返回我的主页 <i>></i></router-link>
        </span>
      </div>
      <p class="mark">
        为了您的账号安全，修改密码前请填写原密码<span>帮助</span>
      </p>
      <form class="form-horizontal password-form">
        <div class="form-group">
          <label class="col-sm-2 control-label">{{$t('editProfile.originalPassword')}}</label>
          <div class="col-sm-3">
            <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.originalPassword')" @change='showFindPwdMsg(setPwd.OldPassword, 0)' v-model="setPwd.OldPassword">
          </div>
          <p class="prompt">{{oldpwdPrompt}}</p>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label">{{$t('editProfile.newPassword')}}</label>
          <div class="col-sm-3">
            <input class="form-control" name="password" type="password" :placeholder="$t('placeholder.newPassword')" @change='showFindPwdMsg(setPwd.NewPassword, 1)' v-model="setPwd.NewPassword">
          </div>
          <p class="prompt">{{newpwdPrompt}}</p>
        </div>
        <div class="form-group">
          <label class="col-sm-2 control-label">{{$t('editProfile.confirmPassword')}}</label>
          <div class="col-sm-3">
            <input class="form-control" name="repassword" type="password" :placeholder="$t('placeholder.repassword')" @change='showFindPwdMsg(setPwd.confirm_password, 2)' v-model="setPwd.confirm_password">
          </div>
          <p class="prompt">{{confirm_upwdPrompt}}</p>
        </div>
        <div class="form-group">

          <button class="col-md-offset-3 col-md-1 forphone btnm  btn-confirm" v-bind:disabled="!setPwd.OldPassword" @click='setPwdFun' data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
          </button>

          <button class="col-md-offset-1 col-md-1 forphone btnm  btn-cacel">
            取消
          </button>

        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { post } from '../../../utils/http'
import { Toast } from 'mint-ui'
export default {
  data() {
    return {
      setPwd: {},
      oldpwdPrompt: '',
      newpwdPrompt: '',
      confirm_upwdPrompt: ''
    }
  },
  mounted() {
  },
  methods: {
    //   验证
    showFindPwdMsg(input, id) {
      if (id === 0) {
        if (input.length > 0) {
          post(`/api/confirmed/password`, this.setPwd).then(data => {
            if (data.resultcode === 0) {
              this.oldpwdPrompt = '原密码错误'
              return false
            } else {
              this.oldpwdPrompt = ''
            }
          })
        }
      } else if (id === 0 || id === 1) {
        var upwdreg = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[~!@#$%^&*()_+`\-={}:";'<>?,.\/]).{6,18}$/
        if (!upwdreg.test(input) && input !== undefined && input.length > 0) {
          if (id === 0) {
            this.oldpwdPrompt = '密码长度在6-18位'
          } else if (id === 1) {
            this.newpwdPrompt = '密码长度在6-18位'
          }
          return false
        } else if (id === 1 && (input === this.setPwd.OldPassword)) {
          this.newpwdPrompt = '新密码不能和原密码一致'
          return false
        } else if (input === undefined || input.length === 0) {
          if (id === 0) {
            this.oldpwdPrompt = '原密码不能为空'
          } else if (id === 1) {
            this.newpwdPrompt = '新密码不能为空'
          }
          return false
        } else {
          this.oldpwdPrompt = ''
          this.newpwdPrompt = ''
        }
      } else if (id === 2) {
        if (input !== this.setPwd.NewPassword && input !== undefined && input.length > 0) {
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
    // 修改密码
    setPwdFun() {
      let instance
      post(`/api/setting/password`, this.setPwd).then(data => {
        if (data.resultcode === 1) {
          instance = new Toast({
            message: data.message,
            iconClass: 'glyphicon glyphicon-ok',
            duration: 1000
          })
          setTimeout(() => {
            instance.close()
          }, 1000)
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
