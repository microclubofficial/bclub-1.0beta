<template>
    <div>
        <div class="container">
            <form class="form-horizontal">
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
                    <div class="col-md-offset-3 col-md-1 forphone btnm confirm" @click='setPwdFun' data-target="#myModal" data-toggle="">{{$t('button.confirm')}}
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import {post} from '../../../utils/http'
import { Toast } from 'mint-ui'
export default {
  data () {
    return {
      setPwd: {},
      oldpwdPrompt: '',
      newpwdPrompt: '',
      confirm_upwdPrompt: ''
    }
  },
  mounted () {
  },
  methods: {
    //   验证
    showFindPwdMsg (input, id) {
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
        var upwdreg = /^[a-zA-Z0-9~!@#$%^&*()_+`\-={}:";'<>?,./]{6,18}$/
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
    setPwdFun () {
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
.confirm{
    color: #fff !important;
    background-color: #337ab7 !important;
    border-color: #2e6da4 !important;
}
 .prompt{
    float: left;
    margin-left: 4%;
    margin-top: 10px;
    color: red;
  }
</style>
