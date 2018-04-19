<template>
    <div class="box">
        <div class="container">
            <div class="page-header">
                <h4>找回密码</h4>
            </div>
            <form>
                <div class="form-group" style="width:30%">
                    <label for="exampleInputEmail1">请输入邮箱</label>
                    <input type="email" class="form-control" v-model="findForm.email" id="exampleInputEmail1" placeholder="Email" @blur='showRegisterMsg(findForm.email, 0)'>
                    <span class="prompt" style="margin-left: 0 !important; display:block;">{{emailPrompt}}</span>
                </div>
                <div class="form-group">
                    <div class=" col-md-1 btnm findforemai"   @click="setfindemail" >确认
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
import {post} from '../../utils/http'
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
          this.emailPrompt = '手机号码不能为空'
          return false
        } else if (!emailreg.test(input) && input !== undefined && input.length > 0) {
          this.emailPrompt = '邮箱格式不正确'
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
.findforemai{
    color: #fff !important;
    background-color: #337ab7 !important;
    border-color: #2e6da4 !important;
}
.prompt{
    margin-top: 10px;
    color: red;
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
