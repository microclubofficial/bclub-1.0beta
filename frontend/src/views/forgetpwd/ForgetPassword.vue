<template>
    <div>
        <div class="container">
            <div class="page-header">
                <h4>忘记密码</h4>
            </div>
            <button type="button" class="btn btn-success" @click="confirmPhone">通过手机找回</button>
            <button type="button" class="btn btn-primary" @click="confirmEmail">通过邮箱找回</button>
        </div>
    </div>
</template>
<script>
export default{
  data: function () {
    return {

    }
  },
  mounted: function () {

  },
  methods: {
    confirmPhone () {
      this.$router.push('/confirmPhone')
    },
    confirmEmail () {
      this.$router.push('/confirmEmail')
    }
  }
}
</script>
