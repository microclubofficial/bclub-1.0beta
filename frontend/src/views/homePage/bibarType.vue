<template>
  <div class="commun-bibarType">
    <h4 style="font-weight:bold;">热门币种</h4>
   <div class="bibarType-main">
     <div v-bind:style="{backgroundImage: 'url(' + type.picture + ')'}" class="bibarType-main-box shadow-box" @click="toBibarData(type.id,type.id,type.name_ch)" :key="index" v-for="(type,index) in bibarType">
       <!--<img :src="type.picture" alt="">-->
       <!--<img src="../../assets/img/pic-news02.png" alt="">-->
       <div class="bibarType-bot">
        <div class="bibarType-title">
         <img :src="type.bpicture" alt=""><img style="width:18px; height:18px;" :src="type.b_picture" alt="">{{type.symbol}}-{{type.name_ch}}
         <!--<span class="bibarType-talk-btn">加入讨论</span>-->
         </div>
        <ul>
          <li>关注 <span class="text-number">17825</span></li>
          <li>文章 <span class="text-number">32216</span></li>
          <li>热度 <span class="text-number">7343</span></li>
          <!--<li>创建管理员</li>-->
        </ul>
       </div>
     </div>
   </div>
  </div>
</template>

<script>
import {get} from '../../utils/http'
export default{
  data: function () {
    return {
      bibarType: []
    }
  },
  mounted: function () {
    get('/api/bpicture').then(data => {
      this.bibarType = data.data
    })
  },
  methods: {
    toBibarData (router, id, ch) {
      this.$store.commit('CHART_ID', {
        'chartId': id,
        'chartCh': ch
      })
      this.$router.push(`/msgDetail/${router}`)
    }
  }
}
</script>

<style>
.bibarType-main{
  width: 1200px;
  margin: auto;
  position: relative;
  display: flex;
  justify-content: space-between;
}
.commun-bibarType>h4{
  margin: 60px auto 20px;
  text-align: center;
}
.bibarType-main-box{background: #fff; position: relative; padding-bottom: 20px; cursor: pointer;}
.bibarType-bot{
  padding: 5px 0;
  position: absolute;
  width: 100%;
  bottom: 0;
  background-image: linear-gradient(rgba(255, 255, 255, 0.4),rgba(255,255,255,0.7),rgba(255,255,255,0.85),rgba(255,255,255,0.93),rgba(255,255,255,0.95),rgba(255,255,255,0.97),rgba(255,255,255,1));
}
.bibarType-main-box>img{width: 240px;}
.bibarType-main-box>.bibarType-bot>ul{overflow: hidden; padding: 0 20px;}
.bibarType-main-box>.bibarType-bot>ul>li{
  float: left;
  margin-right: 10px;
}
.bibarType-main-box>.bibarType-bot>ul>li>.text-number{font-weight: bold;font-size:14px;}
.bibarType-title{
  margin: 10px 0;
  font-size: 15px;
  font-weight: bold;
}
.bibarType-title>img{margin-right: 10px;}
.bibarType-title>.bibarType-talk-btn{
    width: 70px;
    height: 28px;
    line-height: 30px;
    text-align: center;
    float: right;
    background: #1E8FFF;
    color: #fff;
    border-radius: 3px;
}
.bibarType-main-box > img {
    width: 360px;
}
.bibarType-main > .bibarType-main-box {
    width: 32%;
    height: 220px;
    background-repeat: no-repeat;
    background-size: 100% 100%;
}
</style>
