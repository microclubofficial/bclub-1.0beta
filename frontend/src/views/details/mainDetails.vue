<template>
  <div class="list-detail">
    <main-header></main-header>
    <div class="main-details-box">
      <!-- 比特币 -->
      <btb v-show="isShow==0"></btb>
      <eth v-show="isShow==1"></eth>
      <xrp v-show="isShow==2"></xrp>
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
export default {
  components: {
    MainHeader,
    btb,
    eth,
    xrp,
    subDetail,
    longTxt
  },
  data: function () {
    return {
      isShow: null
    }
  },
  mounted () {
    this.isShow = this.$route.params.pageId
  },
  methods: {

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
</style>
