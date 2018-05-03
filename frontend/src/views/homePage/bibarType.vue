<template>
  <div class="commun-bibarType">
    <h4>热门币种</h4>
   <div class="bibarType-main">
     <div class="bibarType-main-box shadow-box" @click="toBibarData(type.id,type.id)" :key="index" v-for="(type,index) in bibarType">
       <img :src="type.picture" alt="">
       <div class="bibarType-title">
         <img :src="type.bpicture" alt=""><img style="width:18px; height:18px;" :src="type.b_picture" alt="">{{type.symbol}}-{{type.name_ch}}
         <!--<span class="bibarType-talk-btn">加入讨论</span>-->
         </div>
        <ul>
          <li>关注<span>17825</span></li>
          <li>文章<span>32216</span></li>
          <li>热度<span>7343</span></li>
          <!--<li>创建管理员</li>-->
        </ul>
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
    toBibarData (router, id) {
      this.$store.commit('CHART_ID', {
        'chartId': id
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
  margin: 20px auto;
  text-align: center;
}
.bibarType-main-box{background: #fff; padding-bottom: 20px; cursor: pointer;}
.bibarType-main-box>img{width: 240px;}
.bibarType-main-box>ul{overflow: hidden; padding: 0 10px;}
.bibarType-main-box>ul>li{
  float: left;
  margin-right: 10px;
}
.bibarType-title{margin: 10px 0; padding: 0 10px;}
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
    width: 30%;
}
</style>
