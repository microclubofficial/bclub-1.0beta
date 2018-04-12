<template>
    <div>
        <div class="container">
            <form class="form-horizontal">
                <div class="form-group">
                    <label for="inputOriginPassword3" class="col-md-1 control-label">原密码</label>
                    <div class="col-md-4">
                        <input type="text" class="form-control" id="inputEmail3inputOriginPassword3" placeholder="请输入原密码">
                    </div>
                </div>
                <div class="form-group">
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
                </div>
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
export default {
  data () {
    return {
    }
  },
  mounted () {
  },
  methods: {
  }
}
</script>
