<template>
    <div class="box">
        <div class="container">
            <div class="page-header">
                <h4>请填写新密码</h4>
            </div>
            <form class="form-horizontal">
                <div class="form-group">
            <label class="col-sm-1 control-label">密码:</label>
            <div class="col-sm-4">
              <input class="form-control" name="password" type="password" placeholder="Password" @blur='showRegisterMsg(findForm.password, 0)' v-model="findForm.password">
            </div>
            <p class="prompt">{{upwdPrompt}}</p>
          </div>
          <div class="form-group">
            <label class="col-sm-1 control-label">确认密码:</label>
            <div class="col-sm-4">
              <input class="form-control" name="repassword" type="password" placeholder="Repassword" @blur='showRegisterMsg(findForm.confirm_password, 1)' v-model="findForm.confirm_password">
            </div>
            <p class="prompt">{{confirm_upwdPrompt}}</p>
          </div>
          <div class="form-group">
                    <div class="col-md-offset-2 col-md-1 btn findpwd"  @click="setnewpwd">确认
                    </div>
                </div>
            </form>
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
      } else if (id === 1) {
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
  .disable{
    background: #BCBCBC !important;
    color: #797979 !important;
    border:none !important;
}
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
