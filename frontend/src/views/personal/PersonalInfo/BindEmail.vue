<style lang="scss" scoped>
.title {
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 28px;
      height: 28px;
      display: block;
      float: left;
      margin-top: 4px;
      margin-right: 4px;

      > img {
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
    float: left;
  }
}

.btn-confirm {
  text-align: center;
  width: 60px;
  height: 32px;
  padding: 0;
  line-height: 32px;
  background: #1e8fff;
  color: #fff;
  border-radius: 5px;
}

.btn-cacel {
  text-align: center;
  width: 60px;
  height: 32px;
  padding: 0;
  line-height: 32px;
  background: #f0f0f0;
  color: #666;
  border-radius: 5px;
  border: solid 1px #dfdfdf;
}

.email-box {
  clear: both;
  overflow: hidden;
  display: block;
  width: 50%;
  margin: 0 auto;
  position: relative;
  padding: 30px 0;
  label {
    width: 40%;
    line-height: 52px;
    display: block;
    float: left;
  }
  input {
    width: 60%;
    float: left;
  }
  button {
    &:nth-child(1) {
      margin-right: 20px;
    }
  }
}

.email-btn {
  padding: 0 0 40px 0;
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
          <img src="../../../assets/img/i04.png" />
        </span>
        <span>{{$t('editProfile.email')}}</span>
        <span>
          <router-link class="hover" :to="{path:'/memberCenter'}">{{$t('personalCenter.returnMyHomepage')}}
            <i>></i>
          </router-link>
        </span>
      </div>
    </div>

    <div class="center-wrap bindEmail">
      <form v-if='!successbind'>
        <div class="form-group email-box">
          <label for="exampleInputEmail1">{{$t('editProfile.bindEmail')}}</label>
          <input type="email" style="margin-top:10px" class="form-control" v-model="bindForm.email" id="exampleInputEmail1" :placeholder="$t('placeholder.email')" @change='showBindEmailMsg(bindForm.email, 0)'>
          <span class="prompt" style="margin-left: 0 !important;height:34px;margin-top:20px; display:block;">{{emailPrompt}}</span>
        </div>
        <div class="email-box email-btn">
          <button type="button" v-bind:disabled="!bindForm.email" @click="bindEmailFun" class="findEmail btnm btn-confirm">{{$t('button.confirm')}}</button>
          <button class="findEmail btnm btn-cacel ">{{$t('button.cancel')}}</button>
        </div>
      </form>
      <!--完成验证后样式-->
      <div class="successBind" style="margin:50px 0;" v-if='successbind'>
        <p>
          已绑定邮箱
          <span style="font-weight: bold;margin: 0 20px 0 10px;">{{bindForm.email}}</span>
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
          </div>
          <!-- /.modal-content -->
        </div>
        <!-- /.modal-dialog -->
      </div>
    </div>
  </div>
</template>
<script>
import { post, get } from "../../../utils/http";
import { Toast } from "mint-ui";
export default {
  data() {
    return {
      bindForm: {},
      emailPrompt: "",
      canFind: false,
      showModal: false,
      successbind: false
    };
  },
  mounted() {},
  methods: {
    // 验证
    showBindEmailMsg(input, id) {
      let emailreg = /^[A-Za-z0-9.\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
      if (id === 0) {
        if (input === undefined || input.length === 0) {
          this.emailPrompt = "邮箱不能为空";
          this.canFind = false;
          return false;
        } else if (
          !emailreg.test(input) &&
          input !== undefined &&
          input.length > 0
        ) {
          this.emailPrompt = "邮箱格式不正确";
          this.canFind = false;
          return false;
        } else {
          this.emailPrompt = "";
          this.canFind = true;
        }
      }
    },
    // 绑定邮箱
    bindEmailFun() {
      let instance;
      if (this.canFind) {
        post(`/api/setting/email`, this.bindForm).then(data => {
          if (data.resultcode === 0) {
            instance = new Toast({
              message: data.message,
              duration: 1000
            });
            setTimeout(() => {
              instance.close();
            }, 1000);
            $(".emaiModal").modal("hide");
            return false;
          } else if (data.resultcode === 1) {
            $(".emaiModal").modal("show");
          }
        });
      }
    },
    // 重新发送
    resendFun() {
      post(`/api/confirmed/password`, this.bindForm).then(data => {});
    },
    // 完成验证状态
    successBind() {
      get(`/api/confirmed/email`).then(data => {
        if (data.resultcode === 0) {
          $(".emaiModal").modal("hide");
          this.successbind = false;
        } else {
          $(".emaiModal").modal("hide");
          this.successbind = true;
        }
      });
    },
    // 完成后修改邮箱
    SbindEmail() {
      this.successbind = false;
    }
  }
};
</script>

<style>
.prompt {
  float: left;
  margin-left: 4%;
  margin-top: 10px;
  color: red;
}

.findEmail {
  transition: opacity 0.5s;
}

.bindEmail > .emaiModal > .modal-dialog {
  width: 30%;
}

.emaiModal > .modal-dialog > .modal-content > .modal-body {
  font-size: 16px;
  text-align: center;
}

.emaiModal > .modal-dialog > .modal-content > .modal-footer {
  border: none;
  text-align: center;
}

.emaiModal > .modal-dialog > .modal-content > .modal-footer > .btn-primary {
  margin-left: 20px;
}
</style>
