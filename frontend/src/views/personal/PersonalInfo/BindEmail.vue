<template>
    <div>
        <div class="container bindEmail">
            <form v-if='!successbind'>
                <div class="form-group">
                    <label class="col-sm-12" for="exampleInputEmail1">{{$t('editProfile.bindEmail')}}</label>
                    <input type="email" style="width:25%;margin-top:10px" class="form-control col-sm-3" v-model="bindForm.email" id="exampleInputEmail1" :placeholder="$t('placeholder.email')" @blur='showBindEmailMsg(bindForm.email, 0)'>
                    <span class="prompt col-sm-9" style="margin-left: 0 !important;height:34px;margin-top:20px; display:block;">{{emailPrompt}}</span>
                </div>
                <button type="button" style="margin-top:10px;" v-bind:disabled="!bindForm.email" @click="bindEmailFun" class="btn findEmail btn-primary">{{$t('button.confirm')}}</button>
            </form>
            <!--完成验证后样式-->
            <div class="successBind" style="margin:50px 0;" v-if='successbind'>
              <p>
                已绑定邮箱<span style="font-weight: bold;margin: 0 20px 0 10px;">{{bindForm.email}}</span>
                <button type="button" @click='SbindEmail' class="btn btn-primary">修改邮箱</button>
              </p>
            </div>
            <!--发邮件模态框-->
                <div class="modal fade emaiModal" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      </div>
                      <div class="modal-body">
                        一封邮件已发送，请注意查收
                      </div>
                      <div class="modal-footer">
                        <button type="button" @click="resendFun" class="btn btn-primary">重新发送
                        </button>
                        <button type="button" @click="successBind" class="btn btn-default">
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
import { Toast } from 'mint-ui'
export default {
  data () {
    return {
      bindForm: {},
      emailPrompt: '',
      canFind: false,
      showModal: false,
      successbind: false
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
      let instance
      if (this.canFind) {
        post(`/api/setting/email`, this.bindForm).then(data => {
          if (data.resultcode === 0) {
            instance = new Toast({
              message: data.message,
              duration: 1000
            })
            setTimeout(() => {
              instance.close()
            }, 1000)
            $('.emaiModal').modal('hide')
            return false
          } else if (data.resultcode === 1) {
            $('.emaiModal').modal('show')
          }
        })
      }
    },
    // 重新发送
    resendFun () {
      post(`/api/setting/email`, this.bindForm).then(data => {
      })
    },
    // 完成验证状态
    successBind () {
      $('.emaiModal').modal('hide')
      this.successbind = true
    },
    // 完成后修改邮箱
    SbindEmail () {
      this.successbind = false
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
 .bindEmail>.emaiModal>.modal-dialog{
    width: 30%;
  }
 .emaiModal>.modal-dialog>.modal-content>.modal-body{
   font-size: 16px;
   text-align: center;
 }
 .emaiModal>.modal-dialog>.modal-content>.modal-footer{
   border:none;
   text-align: center;
 }
 .emaiModal>.modal-dialog>.modal-content>.modal-footer>.btn-primary{
   margin-left: 20px;
 }
</style>
