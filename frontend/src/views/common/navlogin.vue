<template>
  <div>
    <div class="nav_login">
      <a href="javascript:void(0)" class="nav_login_regis" @click="toRegister">{{$t('nav.isRegister')}}</a>
      <div class="nav_login_btn" @click.stop="toLogin()">
        <img src="../../assets/img/login.png" alt="">
        <span>{{$t('nav.login')}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default{
  data: function () {
    return {
    }
  },
  methods: {
    toRegister () {
      this.$router.push('/register')
    },
    toLogin () {
      this.$router.push('/login')
    }
  }
}
</script>

<style>
.form-horizontal .control-label{padding: 7px 0 0 7px;}
.nav_login{
    display: table-cell;
    height: 60px;
    vertical-align: middle;
    font-size: 13px;
}
.nav_login_regis{
  vertical-align: middle;
  font-size:14px;
}
div[class*=_btn] {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: pointer;
}

.nav_login_btn {
    display: inline-block;
    line-height: 1;
    width: 90px;
    margin-left: 22px;
    padding: 6px 0;
    border: 1px solid #0095DA;
    text-align: center;
    font-size: 15px;
    border-radius: 32px;
    vertical-align: middle;
}
.nav_login_btn>img{width: 18px; height: 18px;}
.nav_login_btn span {
    vertical-align: middle;
    color: #0095DA;
}
</style>
