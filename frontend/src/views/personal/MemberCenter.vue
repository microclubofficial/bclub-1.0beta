<style lang="scss" scoped>
/*.member-center{margin-top: 40px;}*/
.personal-info {
    background-color: #fefefe;
    border: 1px solid #eee;
    box-shadow: 1px 1px 1px #ccc;
    padding: 20px;
    display: flex;
    display: -webkit-flex;
    align-items: center;
    .avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        overflow: hidden;
        margin-right: 20px;
        img {
            width: 100%;
        }
    }
    .right-main {
        flex: 9;
        .nav-pills {
            margin-top: 20px;
        }
    }
    .right-btn {
        flex: 1;
    }
}

.main-list {
    background-color: #fafafa;
    box-shadow: 1px 1px 1px #ccc;
    margin-top: 10px;
    min-height: 300px;
}
</style>

<template>
<div>
 <MainHeader></MainHeader>
    <div class="member-center">
        <div class="container">
            <h3 style="margin:20px 0;">{{$t('personalCenter.personal')}}</h3>
            <div class="personal-info">
                <div class="avatar">
                    <img :src="personalUser.avatar" alt="">
                </div>
                <div class="right-main">
                    <h3>{{personalUser.username}}</h3>
                    <!--<p>
                        关注：<a href="">1652</a>&nbsp;&nbsp;&nbsp;&nbsp;
                        主题：<a href="">152</a>&nbsp;&nbsp;&nbsp;&nbsp;
                        热度：<a href="">16515642</a>
                    </p>-->
                    <ul class="nav nav-pills">
                        <li v-for="(item,index) in navList" :class="{active:item.name === $route.name}" @click="routerGo(index)" :key="index">
                            <a href="javascript:void(0)">{{item.cnName}}</a>
                        </li>
                    </ul>
                </div>
                <div class="right-btn">
                    <button class="btn btn-primary" @click="personalInfo">{{$t('personalCenter.editProfile')}}</button>
                </div>
            </div>
            <section>
                <div class="main-list">
                    <router-view></router-view>
                </div>
            </section>
        </div>

    </div>
</div>
</template>
<script>
import {get} from '../../utils/http'
import MainHeader from '../common/header.vue'
export default {
  data () {
    return {
      navList: [
        { 'name': 'topic', 'cnName': this.$t('personalCenter.topic'), 'path': 'topic' },
        { 'name': 'comment', 'cnName': this.$t('personalCenter.comment'), 'path': 'comment' },
        { 'name': 'collection', 'cnName': this.$t('personalCenter.collection'), 'path': 'collection' }
      ],
      nowIndex: 0,
      personalUser: []
    }
  },
  components: {
    MainHeader
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted () {
    get(`/api/u/${this.userInfo.username}`).then(data => {
        console.log(data)
      if (data.resultcode === 0) {
          alert(data.message)
        this.$router.push({ path: '/login' })
      } else {
        this.personalUser = data.data
      }
    })
    // this.routerId = this.$route.path.split('/')
  },
  methods: {
    routerGo (index) {
      this.$router.push(`/memberCenter/${this.navList[index].path}`)
    },
    personalInfo () {
      this.$router.push({ path: '/personalInfo' })
    }
  }
}
</script>
