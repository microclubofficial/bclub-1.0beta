<style lang="scss" scoped>
.login-box {
  width: 40%;
  margin: 100px auto;
  border: none;
  .login-title {
    padding: 20px;
    background-color: #1e8fff;
    h3 {
      font-size: 24px;
      letter-spacing: 2px;
    }
  }
  .flex-box {
    padding: 50px 0 0 0;
    display: flex;
    .flex-item {
      flex: 1;
      text-align: center;
      cursor: pointer;
      p {
        margin: 20px 0 60px 0;
        font-size: 14px;
        &:hover {
          color: #1e8fff;
        }
      }
      .gray-circle {
        width: 120px;
        height: 120px; 
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        &:hover{
          opacity: 0.7;
        }
      } 
    }
    .byphone .gray-circle{
      background: #b9dbfe url('../../assets/img/shouji.png') no-repeat center;
    }
    .byemail .gray-circle{
      background: #b9dbfe url('../../assets/img/youxiang.png') no-repeat center;
    }
  }
}
</style>

<template>
  <div>
    <div class="panel panel-primary login-box">
      <div class="panel-heading login-title">
        <h3 class="panel-title text-center">找回密码</h3>
      </div>
      <div class="panel-body flex-box">
        <div class="byphone flex-item">
          <div class="gray-circle" @click="confirmPhone"></div>
          <p @click="confirmPhone">通过手机找回</p>
        </div>
        <div class="byemail flex-item">
          <div class="gray-circle" @click="confirmEmail"></div>
          <p @click="confirmEmail">通过邮箱找回</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data: function() {
    return {

    }
  },
  mounted: function() {

  },
  methods: {
    confirmPhone() {
      this.$router.push('/confirmPhone')
    },
    confirmEmail() {
      this.$router.push('/confirmEmail')
    }
  }
}
</script>
