<template>
  <section class="bibar-sidebar">
        <a class="personal_avatar" href=""><img :src="userInfo.avatar" alt=""></a>
        <div class="user_name">{{userInfo.username}}</div>
        <table class="user_friends">
          <tbody>
            <tr>
              <td>
                <a href="">
                  <strong>12</strong>
                  <br>
                  <span>关注</span>
                </a>
              </td>
              <td>
                <a href="">
                  <strong>0</strong>
                  <br>
                  <span>粉丝</span>
                </a>
              </td>
            </tr>
          </tbody>
        </table>
        <ul class="user_pannel">
          <li @click="toSomeWhere(index)" :key="index" v-for="(pannel,index) in personalList.from"><i class="iconfont" v-html="pannel.icon"></i><a href="javascript:void(0)">{{pannel.tit}}</a></li>
        </ul>
        <ul class="user_pannel">
          <li :key="index" v-for="(pannel,index) in personalList.friend"><i class="iconfont" v-html="pannel.icon"></i><a href="javascript:void(0)">{{pannel.tit}}</a></li>
        </ul>
        <ul class="user_pannel">
          <li :key="index" v-for="(pannel,index) in personalList.myHouse"><i class="iconfont" v-html="pannel.icon"></i><a href="javascript:void(0)">{{pannel.tit}}</a></li>
        </ul>
        <ul class="about_bibar">
          <li :key="index" v-for="(pannel,index) in personalList.aboutMe"><i class="iconfont" v-html="pannel.icon"></i><a href="javascript:void(0)">{{pannel.tit}}</a></li>
        </ul>
      </section>
</template>

<script>
export default{
  data: function () {
    return {
      personalList: {
        'from': [
          {'icon': '&#xe627;', 'tit': '首页'},
          {'icon': '&#xe608;', 'tit': '主题'},
          {'icon': '&#xe616;', 'tit': '评论'},
          {'icon': '&#xe6a7;', 'tit': '收藏'}
        ],
        'friend': [
          {'icon': '&#xe603;', 'tit': '赞我的'},
          {'icon': '&#xe638;', 'tit': '评论我的'},
          {'icon': '&#xe60b;', 'tit': '提到我的'},
          {'icon': '&#xe60a;', 'tit': '收到的问题'}
        ],
        'myHouse': [
          {'icon': '&#xe66c;', 'tit': '我的专栏'},
          {'icon': '&#xe66b;', 'tit': '我的钱包'}
        ],
        'aboutMe': [
          {'icon': '&#xe655;', 'tit': '关于币吧'},
          {'icon': '&#xe88a;', 'tit': '财经导航'},
          {'icon': '&#xe6c8;', 'tit': '投资者专栏'}
        ]
      }
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted: function () {

  },
  methods: {
    toSomeWhere (index) {
      if (index === 0) {
        this.$router.push('/')
      } else if (index === 1) {
        this.$router.push('/memberCenter/topic')
      } else if (index === 2) {
        this.$router.push('/memberCenter/comment')
      } else if (index === 3) {
        this.$router.push('/memberCenter/collection')
      }
    }
  }
}
</script>

<style>
  /* 左边栏 --- 个人资料 */
.bibar-sidebar{
    float: left;
    width: 150px;
    text-align: center;
    padding-bottom: 10px;
    background: #fff;
}
.bibar-sidebar>.personal_avatar{
    width: 60px;
    height: 60px;
    border: 1px solid #edf0f5;
    margin-top: 30px;
    display: inline-block;
    overflow: hidden;
    border-radius: 50%;
    line-height: 1;
}
.personal_avatar img{
    width: 100%;
    height: 100%;
    vertical-align: middle;
}
.bibar-sidebar table{
    width: 100%;
    height: 60px;
    position: relative;
    border-bottom: 1px solid #edf0f5;
    cursor: pointer;
}
.bibar-sidebar tbody{border-bottom: 1px solid #edf0f5;}
.user_friends{
    line-height: 1.4;
}
.bibar-sidebar td {
    font-size: 14px;
    color: #40474e;
    vertical-align: middle;
}
.user_friends td{
    width: 50%;
}
.user_friends a{display: block;}
.user_friends a span{
    font-size: 12px;
    color: #666c72;
}
.bibar-sidebar table:after {
    position: absolute;
    left: 50%;
    top: 12px;
    height: 36px;
    width: 1px;
    background: #edf0f5;
    content: '';
}
.user_pannel{
    position: relative;
    padding: 12px 0;
}
.user_pannel:before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 15px;
    width: 118px;
    height: 1px;
    background: #edf0f5;
}
.user_pannel li, .about_bibar li {
  text-align: left;
    padding-left: 15px;
}
.user_pannel i, .about_bibar i {
    font-size: 18px;
    color: #888e94;
    vertical-align: middle;
}
.user_pannel a, .about_bibar a {
    margin-left: 6px;
    vertical-align: middle;
}
.about_bibar {
    margin-top: 10px;
    overflow: hidden;
}
</style>
