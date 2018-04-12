<style lang="scss" scoped>
.img-preview {
    padding:20px;
    display: flex;
    display: -webkit-flex;
    align-items: center;
    .rectangle {
        width: 200px;
        height: 200px;
        img {
            width: 100%;
        }
    }
    .round {
        margin-left:100px;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        overflow: hidden;
        img {
            width: 100%;
        }
    }
}
</style>

<template>
    <div>
        <div class="container">
            <form class="form-horizontal">
                <div class="form-group">
                    <label for="inputOriginPassword3" class="col-md-1 control-label">上传头像</label>
                    <div class="col-md-4">
                        <input type="file" class="form-control" id="inputEmail3inputOriginPassword3" placeholder="请输入原密码">
                    </div>
                </div>
                <div class="img-preview">
                    <div class="rectangle">
                        <img :src="userInfo.avatar" alt="">
                    </div>
                    <div class="round">
                        <img :src="userInfo.avatar" alt="">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-md-offset-1 col-md-4">
                        <button type="reset" class="btn btn-default">取消</button>
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
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted () {
  },
  methods: {
  }
}
</script>
