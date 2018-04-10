<template>
    <div>
        <div class="container">
            <div class="page-header">
                <h4>找回密码</h4>
            </div>
            <form class="form-horizontal">
                <div class="form-group">
                    <label for="inputEmail3" class="col-md-1 control-label">手机号</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="inputEmail3"  @blur='showPhone(phoneObj.forgetphone)' v-model="phoneObj.forgetphone" placeholder="请输入手机号">
                    </div>
                    <p class="prompt">{{phonePrompt}}</p>
                </div>
                <div class="form-group">
                    <label for="inputCaptcha3" class="col-md-1 control-label">验证码</label>
                    <div class="col-md-3">
                        <input type="text" class="form-control" v-model="phoneObj.control" id="inputCaptcha3" placeholder="请输入验证码">
                    </div>
                    <div class="col-md-1"><button class="btn btn-success" v-bind:disabled="hasphone" :class="{disable:hasphone}">获取</button></div>
                </div>
                <!-- <div class="form-group">
                    <label for="inputPassword3" class="col-md-1 control-label">新密码</label>
                    <div class="col-md-4">
                        <input type="password" class="form-control" id="inputPassword3" placeholder="请输入新密码">
                    </div>
                </div>
                <div class="form-group">
                    <label for="inputRepassword3" class="col-md-1 control-label">确认密码</label>
                    <div class="col-md-4">
                        <input type="password" class="form-control" id="inputRepassword3" placeholder="请确认新密码">
                    </div>
                </div> -->
                <div class="form-group">
                    <div class="col-md-offset-1 col-md-4">
                        <button type="submit" class="btn btn-primary">确认</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
<script>
export default{
  data: function () {
    return {
      hasphone: true,
      phoneObj: {
        'forgetphone': '',
        'control': '',
        'phonePrompt': ''
      }
    }
  },
  mounted: function () {
  },
  methods: {
    showPhone (val) {
      var ponereg = /^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$/
      console.log(ponereg.test(val))
      if (!ponereg.test(val) && val !== undefined) {
        this.phonePrompt = '手机号码格式不正确'
        this.hasphone = true
      } else if (val === '' || val === undefined) {
        this.phonePrompt = '手机号码不能为空'
        this.hasphone = true
      } else {
        this.phonePrompt = ''
        this.hasphone = false
      }
    }
  }
}
</script>

<style>
.prompt{
    margin-top: 10px;
    color: red;
  }
.disable{
    background: #BCBCBC;
    color: #797979;
    border:none;
}
</style>
