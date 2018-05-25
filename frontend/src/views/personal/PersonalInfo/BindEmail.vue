<template>
    <div>
        <div class="container bindEmail">
            <form v-if='!successbind'>
                <div class="form-group">
                    <label class="col-sm-12" for="exampleInputEmail1">{{$t('editProfile.bindEmail')}}</label>
                    <input type="email" style="width:25%;margin-top:10px" class="form-control col-sm-3" v-model="bindForm.email" id="exampleInputEmail1" :placeholder="$t('placeholder.email')" @change='showBindEmailMsg(bindForm.email, 0)'>
                    <span class="prompt col-sm-9" style="margin-left: 0 !important;height:34px;margin-top:20px; display:block;">{{emailPrompt}}</span>
                </div>
                <button type="button" style="margin-top:10px;" v-bind:disabled="!bindForm.email" @click="bindEmailFun" class="btn findEmail btn-primary">{{$t('button.confirm')}}</button>
            </form>
            <!--完成验证后样式-->
            <div class="successBind" style="margin:50px 0;" v-if='successbind'>
              <p>{{$t('editProfile.bindedEmail')}}<span style="font-weight: bold;margin: 0 20px 0 10px;">{{bindForm.email}}</span>
                <button type="button" @click='SbindEmail' class="btn btn-primary">{{$t('button.edit')}}</button>
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
                        <p >{{$t('prompt.emailSent')}}</p>
                      </div>
                      <div class="modal-footer">
                        <button type="button" @click="resendFun" class="btn btn-primary">{{$t('button.resend')}}
                        </button>
                        <button type="button" @click="successBind" class="btn btn-default">
                          {{$t('button.verify')}}
                        </button>
                      </div>
                    </div><!-- /.modal-content -->
                  </div><!-- /.modal-dialog -->
</div>
        </div>
    </div>
</template>
<script>
import {post, get} from '../../../utils/http'
// import { Toast } from 'mint-ui'
import {getToken} from '../../../utils/auth.js'
export default {
  data () {
    return {
      bindForm: {},
      emailPrompt: '',
      canFind: false,
      showModal: false,
      successbind: false,
      user_token: ''
    }
  },
  mounted () {
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
    if (this.user_token === '') {
      this.$router.push('/')
    }
    get(`/api/u/email`).then(data => {
      if (data.resultcode === 1) {
        this.successbind = true
      }
    })
  },
  methods: {
    // 验证
    showBindEmailMsg (input, id) {
      let emailreg = /^[A-Za-z0-9.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.emailPrompt = this.$t('prompt.emailRequired')
          this.canFind = false
          return false
        } else if (!emailreg.test(input) && input !== undefined && input.length > 0) {
          this.emailPrompt = this.$t('prompt.emailError')
          // get('/api/setting/email', {'email': input}).then(data=>{
          //   console.log(data)
          // })
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
    },
    // 重新发送
    resendFun () {
      this.bindEmailFun()
    },
    // 完成验证状态
    successBind () {
      get(`/api/confirmed/email`, {email: this.bindForm.email}).then(data => {
        if (data.resultcode === 0) {
          alert(data.message)
          $('.emaiModal').modal('show')
          this.successbind = false
        } else {
          $('.emaiModal').modal('hide')
          this.successbind = true
        }
      })
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
