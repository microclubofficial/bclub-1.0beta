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
.vicp-drop-area {
  width: 340px;
  height: 270px;
}
.title {
  color: #666;
  border-bottom: solid 1px #dfdfdf;
  height: 80px;
  line-height: 80px;
  margin: 0 50px;
  span {
    &:nth-child(1) {
      width: 32px;
      height: 32px;
      display: block;
      float: left;
      margin-top: 6px;
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
.center-wrap {
  width: 100%;
  margin: 0 auto;
}
.wrap {
  width: 100%;
  position: relative;
  color: #666;
}
.wrap-width {
  width: 90%;
}
.clearfix:after {
  display: block;
  clear: both;
  content: "";
  visibility: hidden;
  height: 0;
}
.clearfix {
  zoom: 1;
}
</style>

<template>
    <div class="wrap">
        <div class="center-wrap">
          <div class="title">
            <span>
              <img src="../../../assets/img/i02.png"/>
            </span>
            <span>{{$t('editProfile.avatar')}} </span>
            <span>
              <router-link class="hover" :to="{path:'/memberCenter'}">
              {{$t('personalCenter.returnMyHomepage')}}<i>></i>
              </router-link>
            </span>
         </div>
            <!--<a class="btn" @click="toggleShow">{{$t('editProfile.setAvatar')}}</a>-->
            <my-upload field="img" @cropSuccess="cropSuccessFun" @cropUploadSuccess="cropUploadSuccessFun" @cropUploadFail="cropUploadFailFun" :width="200" :height="200" url="/api/avatar" :params="params" :headers="headers" img-format="png"></my-upload>
            <img :src="imgDataUrl">
            <!-- <div class="right-box">
              <div class="sqaure">
                <img src="../../../assets/img/tp.jpg" alt="">
              </div>
              <div class="cicle">
                <img src="../../../assets/img/tp.jpg" alt="">
              </div>
            </div> -->
        </div>
    </div>
</template>
<script>
import 'babel-polyfill'
import myUpload from '../uploadImg/upload.vue'
import { setToken, rememberToken, getToken } from '../../../utils/auth'
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
      imgDataUrl: '',
      user_token: ''
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
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
    if (this.user_token === '') {
      this.$router.push('/')
    }
  },
  methods: {
    toggleShow () {
      this.show = !this.show
    },
    cropSuccessFun (imgDataUrl, field) {
      this.imgDataUrl = imgDataUrl
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
    }
  }
}
</script>
