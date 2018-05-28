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
.title {
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 32px;
      height: 24px;
      display: inline-block;

      >img {
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
.center-wrap {
  width: 840px;
  margin: 0 auto;
}
</style>

<template>
    <div>
        <div class="center-wrap">
          <div class="title">
            <span>
              <img src="../../../assets/img/personal.png"/>
            </span>
            <span>修改头像 </span>
            <span>
              <router-link class="hover" :to="{path:'/memberCenter'}">
              返回我的主页<i>></i>
              </router-link>
            </span>
        
         </div>
            <!--<a class="btn" @click="toggleShow">{{$t('editProfile.setAvatar')}}</a>-->
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
        setToken('b-Token', data.data, { expires: 7 })
        // console.log(setToken(data.data, { expires: 7 }))
      } else {
        setToken('b-Token', data.data)
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
