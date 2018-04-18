<template>
    <div>
        <div class="container">
            <form class="form-horizontal">
                <div class="form-group">
            <label class="col-sm-1 control-label">原密码:</label>
            <div class="col-sm-3">
              <input class="form-control" name="password" type="password" placeholder="Password" @blur='showFindPwdMsg(setPwd.OldPassword, 0)' v-model="setPwd.OldPassword">
            </div>
            <p class="prompt">{{oldpwdPrompt}}</p>
          </div>
                <div class="form-group">
            <label class="col-sm-1 control-label">新密码:</label>
            <div class="col-sm-3">
              <input class="form-control" name="password" type="password" placeholder="Password" @blur='showFindPwdMsg(setPwd.NewPassword, 1)' v-model="setPwd.NewPassword">
            </div>
            <p class="prompt">{{newpwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-1 control-label">确认密码:</label>
            <div class="col-sm-3">
              <input class="form-control" name="repassword" type="password" placeholder="Repassword" @blur='showFindPwdMsg(setPwd.confirm_password, 2)' v-model="setPwd.confirm_password">
            </div>
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
          <div class="form-group"  style="margin-top: 37px;">
                    <div class="col-md-offset-2 col-md-1 forphone btnm confirm" @click='setPwdFun' data-target="#myModal" data-toggle="">确认
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
      if (id === 0 || id === 1) {
        var upwdreg = /^[a-zA-Z0-9_]{6,}$/
        if (!upwdreg.test(input) && input !== undefined && input.length > 0) {
          if (id === 0) {
            this.oldpwdPrompt = '原密码长度不能小于6位'
          } else if (id === 1) {
            this.newpwdPrompt = '新密码长度不能小于6位'
          }
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
