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
            <a class="btn" @click="toggleShow">设置头像</a>
            <my-upload field="img" @cropSuccess="cropSuccessFun" @cropUploadSuccess="cropUploadSuccessFun" @cropUploadFail="cropUploadFailFun" :width="50" :height="50" url="/api/avatar" :params="params" :headers="headers" img-format="png"></my-upload>
            <img :src="imgDataUrl">
        </div>
    </div>
</template>
<script>
import 'babel-polyfill'
import myUpload from '../uploadImg/upload.vue'
import { setToken, rememberToken } from '../../../utils/auth'
export default {
  data () {
    return {
      show: true,
      params: {
        token: '123456798',
        name: 'avatar'
      },
      headers: {
        smail: '*_~'
      },
      imgDataUrl: ''
    }
  },
  components: {
    myUpload
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted () {
  },
  methods: {
    toggleShow () {
      this.show = !this.show
    },
    cropSuccessFun (imgDataUrl, field) {
      this.imgDataUrl = imgDataUrl
      console.log(this.imgDataUrl)
    },
    cropUploadSuccessFun (data, field) {
      this.$store.commit('USER_INFO', {
        'username': data.data.username,
        'avatar': data.data.avatar,
        'isLogin': true
      })
      if (rememberToken('remember_token')) {
        setToken(data.data, { expires: 7 })
        // console.log(setToken(data.data, { expires: 7 }))
      } else {
        setToken(data.data)
        // console.log(setToken(data.data))
      }
      this.$router.push('/memberCenter')
    },
    cropUploadFailFun (status, field) {
      console.log(status)
    }
  }
}
</script>
