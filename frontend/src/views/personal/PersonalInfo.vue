<style lang="scss" scoped>
.member-center {
  margin-top: 40px;
}
.personal-info {
  background-color: #fefefe;
  border: 1px solid #eee;
  display: flex;
  display: -webkit-flex;
  align-items: center;
}
.breadcrumb {
  .hover:hover {
    color: #1e8fff;
  }
}
//加入样式
.nav-width {
  width: 27%;
  height: 600px;
  background: #fff;
  float: left;
  border-bottom: none;
  margin-right: 3%;
  .tx-box {
    width: 100%;
    height: 80px;
    margin-top: 30px;
  }
  .tx {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    overflow: hidden;
    margin: 0 auto;
    > img {
      width: 100%;
      height: 100%;
    }
  }
  .name {
    font-size: 16px;
    font-weight: bold;
    padding: 16px 0 16px 0;
  }
  .grade {
    padding: 0 0 32px 0;
    span {
      font-size: 14px;
      color: #fff;
      background: #ffce0a;
      padding: 4px 12px;
      border-radius: 10px;
    }
  }
  li {
    width: 100%;
    display: block;
    border: 0;
    margin: 0;
    text-align: center;
  }
  .nav-li {
    width: 100%;
    height: 48px;
    line-height: 48px;
    display: block;
    text-align: center;
    border: none;
    &.active {
      a {
        border: 0;
        height: 48px;
        line-height: 48px;
        background: #1e8fff;
        color: #fff;
      }
    }
    &:hover {
      width: 100%;
      border: 0;
      height: 48px;
      line-height: 48px;
    }
    a {
      margin: 0;
      padding: 0;
      height: 48px;
      font-size: 14px;
      border: 0;
      line-height: 48px;
      &:hover {
        border: 0;
      }
    }
  }
}
.info-border {
  border-bottom: solid 1px #dfdfdf;
}
.right-width {
  min-height: 600px;
  display: block;
  width: 70%;
  float: left;
}
.enul {
  .nav-li {
    text-align: left;
    text-indent: 36%;
  }
}
</style>

<template>
    <div>
        <MainHeader></MainHeader>
        <div class="member-center">
            <div class="container">
                <!-- <ol class="breadcrumb">
                    <li>
                        <router-link to='/'>
                            <i class="iconfont" style="margin-right:10px;">&#xe65a;</i>{{$t('editProfile.index')}}</router-link>
                    </li>
                    <li class="active">
                        <router-link class="hover" :to="{path:'/memberCenter'}">{{$t('personalCenter.personal')}}</router-link>
                    </li>
                </ol> -->
                <ul class="nav  nav-tabs nav-width" :class="{'enul':language == 'en'}">
                    <li class="tx-box">
                        <div class="tx">
                            <img  :src="user_token.avatar ? user_token.avatar : userInfo.avatar"/>
                        </div>
                    </li>
                    <li class="name">{{user_token.username ? user_token.username : userInfo.username}}</li>
                    <li class="grade">
                        <span>星级达人</span>
                    </li>
                    <li class="nav-li" v-for="(item,index) in infoList" :class="{active:item.name === $route.name}" @click="routerGo(index)" :key="index">
                        <a href="javascript:void(0)">{{item.cnName}}</a>
                    </li>
                </ul>
                <div class="personal-info right-width">
                    <router-view></router-view>
                </div>
                <section>
                    <div class="main-list">

                    </div>
                </section>
            </div>
        </div>
    </div>
</template>
<script>
import {getToken} from '../../utils/auth.js'
import MainHeader from '../common/header.vue'
export default {
  data () {
    return {
      infoList: [
        { 'name': 'editInfo', 'cnName': this.$t('editProfile.profile'), 'path': 'editInfo' },
        { 'name': 'editAvatar', 'cnName': this.$t('editProfile.avatar'), 'path': 'editAvatar' },
        { 'name': 'editPassword', 'cnName': this.$t('editProfile.password'), 'path': 'editPassword' },
        { 'name': 'bindEmail', 'cnName': this.$t('editProfile.email'), 'path': 'bindEmail' }
      ],
      nowIndex: 0,
      personalUser: [],
      user_token: ''
    }
  },
  computed: {
    language () {
      return this.$store.state.language.language
    },
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  components: {
    MainHeader
  },
  created () {
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
  },
  methods: {
    routerGo (index) {
      this.$router.push(`/personalInfo/${this.infoList[index].path}`)
    }
  }
}
</script>
<style>
    .breadcrumb{border-bottom: 1px solid #efefef;background: #F2F2F2;}
    .breadcrumb li:first-child a{color: #2DA2FF;}
</style>
