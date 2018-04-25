<template>
  <div id="commun">
      <MainHeader @backLoadMain='toMainLoadFun'></MainHeader>
      <section class="bibar-Main">
    <section class="bibar-w1100">
      <!-- left slide -->
      <BibarLeft v-if="initHide"></BibarLeft>
        <!--主体左侧-->
      <section class="bibar-Mainleft" :class="{initClass:initShow}">
          <!--社区币吧数据-->
      <BibarData v-show="initShow"></BibarData>
      <!--社区各币种-->
      <BibarType v-show="initShow"></BibarType>
      <!--社区综合-->
      <BibarTogether v-show="initShow"></BibarTogether>
      <!-- 富文本区 -->
      <div style="width:790px; margin:auto; background:#fff;" class="Maineditor" :class="{initHideEditor:initHide}"  v-if="initHide">
        <BibarPostContent @backFtContent = 'FtContentFun'></BibarPostContent>
      </div>
      <!--社区列表-->
      <!--主体左侧-->
        <section class="bibar-commun" :class="{initSty:initShow}">
            <div class="pt20"></div>
            <!--新闻-->
            <article class="bibar-box bibar-boxindex2">
                <div class="bibar-indexNews">
                    <div class="bibar-indexNews-TAB">
                        <ul class="bibar-tabs-listSty2">
                            <li class="bibar-tabs-item" :key='index' v-for="(tmp,index) in newList" :class="{active:state==index}" @click="changeActive(index)"> <a href="#bibar-newstab1" data-toggle="tab">{{tmp}}</a></li>
                        </ul>
                    </div>
                    <!--新闻列表-->
                    <router-view ref="showFtContent" :getNavData='backForNav'></router-view>
                </div>
            </article>
        </section>
        </section>
        <!--主体右侧-->
        <section class="bibar-Mainright" v-if="initHide">
            <BibarRight></BibarRight>
        </section>
    </section>
    <div class="pt40"></div>
    </section>
  </div>
</template>

<script>
import MainHeader from '../common/header.vue'
import BibarData from './bibarData.vue'
import BibarType from './bibarType.vue'
import BibarTogether from './bibarTogether.vue'
import BibarPostContent from './bibarPostContent.vue'
import BibarRight from '../BibarMsg/BibarRight/bivarRight.vue'
import BibarLeft from '../homePage/bibarLeft/bibarSideLeft.vue'

export default{
  name: 'common',
  data: function () {
    return {
      newList: ['热门', '资本市场', '分析师说', '深度', '百科'],
      newRouter: ['hot', 'market', 'analyst', 'depth', 'baike'],
      state: 0,
      isLogin: true,
      backForNav: [],
      initShow: false,
      initHide: false
    }
  },
  components: {
    MainHeader,
    BibarData,
    BibarType,
    BibarTogether,
    BibarPostContent,
    BibarRight,
    BibarLeft
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted () {
    this.loadShow()
  },
  methods: {
    // 社区文章列表切换事件
    changeActive: function (index) {
      if (index !== this.state) {
        this.state = index
        this.$router.push(`${this.newRouter[this.state]}`)
      } else {
        this.$router.push(`${this.newRouter[this.state]}`)
      }
    },
    // 正文发帖
    FtContentFun (data) {
      // this.$store.dispatch('set_backForNav', data)
      this.$refs.showFtContent.showFtContentFun(data)
    },
    // 退登状态----重新加载页面
    toMainLoadFun () {
      this.loadShow()
    },
    // 退登状态
    loadShow () {
      if (!this.userInfo.isLogin) {
        this.initShow = true
        this.initHide = false
      } else {
        this.initShow = false
        this.initHide = true
      }
    }
  }
}
</script>

<style>
  .bibar-commun{
    width: 790px;
    margin: 0 auto
  }
  .Maineditor>.wangeditor>.toLongText{right: 420px !important;}
  /* .initHideEditor{margin-top:80px !important;} */
  .initSty{width: 1200px !important;}
  .initClass{width: 1200px !important;}
</style>
