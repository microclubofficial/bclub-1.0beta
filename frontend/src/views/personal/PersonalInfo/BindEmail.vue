<template>
    <div>
        <div class="container">
            <form>
                <div class="form-group">
                    <label class="col-sm-12" for="exampleInputEmail1">请输入注册时的邮箱</label>
                    <input type="email" style="width:25%;margin-top:10px" class="form-control col-sm-3" v-model="bindForm.email" id="exampleInputEmail1" placeholder="Email" @blur='showBindEmailMsg(bindForm.email, 0)'>
                    <span class="prompt col-sm-9" style="margin-left: 0 !important;height:34px;margin-top:20px; display:block;">{{emailPrompt}}</span>
                </div>
                <button type="button" style="margin-top:10px;" @click="bindEmailFun" class="btn btn-primary">确认</button>
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
      bindForm: {},
      emailPrompt: ''
    }
  },
  mounted () {
  },
  methods: {
    // 验证
    showBindEmailMsg (input, id) {
      let emailreg = /^[A-Za-z0-9.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
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
    // 绑定邮箱
    bindEmailFun () {
      let instance
      console.log(this.setPwd)
      post(`/api/setting/email`, this.setPwd).then(data => {
        console.log(data)
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
        }
      })
    }
  }
}
</script>

<style>
 .prompt{
    float: left;
    margin-left: 4%;
    margin-top: 10px;
    color: red;
  }
</style>
