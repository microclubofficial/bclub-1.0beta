<template>
  <div id="commun">
      <MainHeader></MainHeader>
      <!--社区币吧数据-->
      <BibarData></BibarData>
      <!--社区各币种-->
      <BibarType></BibarType>
      <!--社区综合-->
      <BibarTogether></BibarTogether>
      <!-- 富文本区 -->
      <div style="width:1100px; margin:auto; background:#fff;">
        <BibarPostContent @backFtContent = 'FtContentFun'></BibarPostContent>
      </div>
      <!--社区列表-->
      <!--主体左侧-->
        <section class="bibar-commun">
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
                    <router-view ref='showFtContent'></router-view>
                </div>
            </article>
        </section>
  </div>
</template>

<script>
import MainHeader from '../common/header.vue'
import BibarData from './bibarData.vue'
import BibarType from './bibarType.vue'
import BibarTogether from './bibarTogether.vue'
import BibarPostContent from './bibarPostContent.vue'

export default{
  name: 'common',
  data: function () {
    return {
      newList: ['热门', '资本市场', '分析师说', '深度', '百科'],
      newRouter: ['hot', 'market', 'analyst', 'depth', 'baike'],
      state: 0,
      isLogin: true
    }
  },
  components: {
    MainHeader,
    BibarData,
    BibarType,
    BibarTogether,
    BibarPostContent
  },
  created: function () {
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
    FtContentFun (data) {
      this.$refs.showFtContent.showFtContentFun(data)
    }
  }
}
</script>

<style>
  .bibar-commun{
    width: 1100px;
    margin: 0 auto
  }
</style>
