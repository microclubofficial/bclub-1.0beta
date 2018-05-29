<style lang="scss" scoped>
/*.member-center{margin-top: 40px;}*/
.personal-info {
  height: 150px;
  position: relative;
  background-color: #fefefe;
  border: 1px solid #eee;
  box-shadow: 1px 1px 1px #ccc;
  padding: 0 20px;
  display: flex;
  display: -webkit-flex;
  .avatar {
    left: 15px;
    top: -70px;
    position: absolute;
    border: solid 2px #fff;
    width: 170px;
    height: 170px;
    border-radius: 10px;
    overflow: hidden;
    margin-right: 20px;
    img {
      width: 100%;
    }
  }
  .right-main {
    float: left;
    margin-left: 200px;
    flex: 9;
    .nav-pills {
      margin-top: 20px;
      li {
        &.active {
          a {
            background: #1e8fff;
          }
        }
        &:nth-child(2) {
          border: solid 1px #dfdfdf;
          border-radius: 4px;
          margin-left: 10px;
        }
        &:nth-child(3) {
          border: solid 1px #dfdfdf;
          border-radius: 4px;
          margin-left: 10px;
        }
      }
      a {
        padding: 4px 12px;
      }
    }
    h3 {
      padding-top: 18px;

      span {
        &:nth-child(2) {
          font-size: 14px;
          color: #666;
          padding-left: 20px;
        }
      }
    }
  }
  .right-btn {
    flex: 1;
    margin-top: 18px;
    .edit-btn {
      background: #fff;
      color: #666;
      border: none;
      &::after {
        content: '';
        width: 28px;
        height: 28px;
        display: block;
        position: absolute;
        background: url(../../assets/img/i00.png);
        background-size: cover;
        top: 8px;
        right: 18px;
      }
    }
  }
}

.main-list {
  background-color: #fafafa;
  box-shadow: 1px 1px 1px #ccc;
  margin-top: 10px;
  min-height: 300px;
}
.bg-box {
  width: 100%;
  height: 140px;
  position: relative;
  background: #ccc;
  margin-top: 20px;
  .bgimg-box {
    width: 100%;
    height: 140px;
    background: #ccc;
    > img {
      width: 100%;
      height: 100%;
      display: block;
    }
  }
  .upload-box {
    width: 120px;
    height: 36px;
    line-height: 36px;
    border-radius: 5px;
    border: solid 1px #dfdfdf;
    position: absolute;
    top: 10px;
    right: 10px;
    color: #fff;
    display: block;
    > span {
      float: right;
      padding-right: 10px;
      &::before {
        content: "";
        width: 22px;
        height: 18px;
        background: url(../../assets/img/msg.png) no-repeat;
        display: inline-block;
        margin: 0 6px;
      }
    }
  }
}
</style>

<template>
<div>
 <MainHeader></MainHeader>
    <div class="member-center">
        <div class="container">
            <!-- <h3 style="margin:20px 0;">{{$t('personalCenter.personal')}}</h3> -->
            <div class="bg-box">
                <div class="bgimg-box">
                    <img  src="../../assets/img/pic-news.png"/>
                </div>
                <div class="upload-box">
                    <span>上传封面照片</span>
                </div>
            </div>
            <div class="personal-info">
                <div class="avatar">
                    <img :src="personalUser.avatar" alt="">
                </div>
                <div class="right-main">
                    <h3>
                        <span>{{personalUser.username}}</span>
                        <span>个人说明个人说明</span>
                     </h3>
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
                    <button class="edit-btn" @click="personalInfo">{{$t('personalCenter.editProfile')}}</button>
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
import { get } from "../../utils/http";
import MainHeader from "../common/header.vue";
export default {
  data() {
    return {
      navList: [
        {
          name: "topic",
          cnName: this.$t("personalCenter.topic"),
          path: "topic"
        },
        {
          name: "comment",
          cnName: this.$t("personalCenter.comment"),
          path: "comment"
        },
        {
          name: "collection",
          cnName: this.$t("personalCenter.collection"),
          path: "collection"
        }
      ],
      nowIndex: 0,
      personalUser: []
    };
  },
  components: {
    MainHeader
  },
  computed: {
    userInfo() {
      return this.$store.state.userInfo.userInfo;
    }
  },
  mounted() {
    get(`/api/u/${this.userInfo.username}`).then(data => {
      if (data.message === "未登录") {
        this.$router.push({ path: "/login" });
      } else {
        this.personalUser = data.data;
      }
    });
    // this.routerId = this.$route.path.split('/')
  },
  methods: {
    routerGo(index) {
      this.$router.push(`/memberCenter/${this.navList[index].path}`);
    },
    personalInfo() {
      this.$router.push({ path: "/personalInfo" });
    }
  }
};
</script>
