<template>
  <div class="list-detail">
    <main-header></main-header>
    <div class="main-details-box">
      <!-- 比特币 -->
      <btb v-show="isShow==0" :bId="chartId"></btb>
      <eth v-show="isShow==1" :bId="chartId"></eth>
      <!-- 富文本区 -->
      <div class="mainBibar-editor bibarType-editor bibar-box" style="width:1100px; margin:20px auto 20px; padding:20px 0; background:#fff;" v-show="isShow==0 || isShow==1 || isShow==0">
        <BibarPostContent></BibarPostContent>
      </div>
      <!-- 新闻列表 -->
      <!--新闻-->
            <article class="bibar-box bibar-boxindex2" v-show="isShow==0 || isShow==1 || isShow==0">
                <div class="bibar-indexNews">
                    <div class="bibar-indexNews-TAB">
                        <ul class="bibar-tabs-listSty2">
                            <li class="bibar-tabs-item" :key='index' v-for="(tmp,index) in newList" :class="{active:state==index}" @click="changeActive(index)"> <a href="#bibar-newstab1" data-toggle="tab">{{tmp}}</a></li>
                        </ul>
                    </div>
                    <!--新闻列表-->
                    <router-view ref="showBibarContent"></router-view>
                </div>
            </article>
      <xrp v-show="isShow==2" :bId="chartId"></xrp>
      <subDetail v-show="isShow==3"></subDetail>
      <longTxt v-show='isShow==4'></longTxt>
    </div>
  </div>
</template>

<script>
import MainHeader from '../common/header'

// 比特币
import btb from '../BibarMsg/BibarChart/BTB.vue'
import eth from '../BibarMsg/BibarChart/ETH.vue'
import xrp from '../BibarMsg/BibarChart/XRP.vue'
import subDetail from '../homePage/subDetail.vue'
import longTxt from '../homePage/longTxt.vue'
import BibarPostContent from '../homePage/bibarPostContent.vue'
export default {
  components: {
    MainHeader,
    btb,
    eth,
    xrp,
    subDetail,
    longTxt,
    BibarPostContent
  },
  data: function () {
    return {
      isShow: null,
      newList: ['全部', '讨论', '文章', '新闻', '交易'],
      newRouter: ['all', 'talk', 'works', 'news', 'trade'],
      state: 0,
      i: 1
    }
  },
  computed: {
    chartId () {
      return this.$store.state.chartId.chartId
    }
  },
  mounted () {
    this.isShow = this.$route.params.pageId
  },
  methods: {
    // 文章列表切换事件
    changeActive: function (index) {
      if (index !== this.state) {
        this.state = index
        this.$router.push(`/bibarLayout/${this.newRouter[this.state]}`)
      }
    }
  }
}
</script>

<style>
.list-detail{width: 100%;}
.list-detail>.main-details-box{
  width: 1100px;
  margin: 80px auto;
  position: relative;
}
.bibarType-editor > .wangeditor > .cancel{right: 335px !important;}
.bibarType-editor > .wangeditor > .report{right: 274px !important;}
.bibarType-editor > .wangeditor > .toLongText[data-v-1bdf9d92]{right:524px !important;}
</style>
