<template>
    <div>
        <div class="container">
            <form>
                <div class="form-group">
                    <label class="col-sm-12" for="exampleInputEmail1">请输入要绑定的邮箱</label>
                    <input type="email" style="width:25%;margin-top:10px" class="form-control col-sm-3" v-model="bindForm.email" id="exampleInputEmail1" placeholder="Email" @blur='showBindEmailMsg(bindForm.email, 0)'>
                    <span class="prompt col-sm-9" style="margin-left: 0 !important;height:34px;margin-top:20px; display:block;">{{emailPrompt}}</span>
                </div>
                <button type="button" style="margin-top:10px;" v-bind:disabled="!bindForm.email" @click="bindEmailFun" class="btn findEmail btn-primary">确认</button>
            </form>
            <!--发邮件模态框-->
                <div class="modal fade emaiModal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-body">
                        一封邮件已发送，请注意查收
                      </div>
                      <div class="modal-footer">
                        <button type="button" @click="bindEmailFun"  class="btn btn-default">重新发送
                        </button>
                        <button type="button" class="btn btn-primary">
                          完成验证
                        </button>
                      </div>
                    </div><!-- /.modal-content -->
                  </div><!-- /.modal-dialog -->
</div>
        </div>
    </div>
</template>
<script>
import {post} from '../../../utils/http'
// import { Toast } from 'mint-ui'
export default {
  data () {
    return {
      bindForm: {},
      emailPrompt: '',
      canFind: false,
      showModal: false
    }
  },
  mounted () {
    $('.emaiModal').modal('show')
  },
  methods: {
    // 验证
    showBindEmailMsg (input, id) {
      let emailreg = /^[A-Za-z0-9.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.emailPrompt = '邮箱不能为空'
          this.canFind = false
          return false
        } else if (!emailreg.test(input) && input !== undefined && input.length > 0) {
          this.emailPrompt = '邮箱格式不正确'
          this.canFind = false
          return false
        } else {
          this.emailPrompt = ''
          this.canFind = true
        }
      }
    },
    // 绑定邮箱
    bindEmailFun () {
      // let instance
      if (this.canFind) {
        post(`/api/setting/email`, this.bindForm).then(data => {
          if (data.resultcode === 0) {
            alert(data.message)
            $('.emaiModal').modal('hide')
            return false
          } else if (data.resultcode === 1) {
            $('.emaiModal').modal('show')
          }
        })
      }
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
  .findEmail{
    transition: opacity .5s
  }
</style>
