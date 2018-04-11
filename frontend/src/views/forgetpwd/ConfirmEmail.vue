<template>
    <div class="box">
        <div class="container">
            <div class="page-header">
                <h4>找回密码</h4>
            </div>
            <form>
                <div class="form-group" style="width:30%">
                    <label for="exampleInputEmail1">请输入注册时的邮箱</label>
                    <input type="email" class="form-control" v-model="findForm.email" id="exampleInputEmail1" placeholder="Email" @blur='showRegisterMsg(findForm.email, 0)'>
                    <p class="prompt" style="margin-left: 0 !important;">{{emailPrompt}}</p>
                </div>
                <div class="form-group">
                    <div class=" col-md-1 btn findforemai"   @click="setfindemail" >确认
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
          this.emailPrompt = '用户名长度在3-16位之间'
          return false
        } else {
          this.emailPrompt = ''
        }
      }
    },
    // 填新密码
    setfindemail () {
      post('/api/forget', this.findForm).then(data => {
        console.log(data)
        if (data.resultcode === 1) {
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
    color: #fff;
    background-color: #337ab7;
    border-color: #2e6da4;
}
</style>
