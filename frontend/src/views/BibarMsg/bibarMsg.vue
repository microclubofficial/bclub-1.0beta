<template>
  <div class="main">
    <MainHeader></MainHeader>
    <!--主体-->
    <section class="bibar-Main">
    <div class="pt40"></div>
    <section class="bibar-w1100">
        <!--主体左侧-->
        <section class="bibar-Mainleft">
            <div class="panel-group" id="accordion">
              <div class="panel panel-default" v-for="(item,index) in summaryList" :key='index'>
                <div id='collapseOne' class="panel-collapse collapse">
                  <div class="panel-body">
                    <!--BTB信息框-->
                    <btb></btb>
                  </div>
                </div>
                 <!-- 币种列表 -->
                 <a data-toggle="collapse" class="panel-tb-hd" data-parent="#accordion" href='#collapseOne'>
                  <div class="bibar-list-item">
                  <ul>
                    <li><a href="#"><span><img :src="item.picture" alt=""></span> {{item.name_ch}} - {{item.symbol}}</a></li>
                    <li><a href="#"><i class="iconfont icon-CNY"></i>{{item.price | cnyFun(CNY,2)}}</a></li>
                    <li><a href="#">{{item.change_1h}}</a></li>
                    <li><a href="#"><i class="iconfont icon-CNY"></i>{{item.volume | cnyFun(CNY,2)}}</a></li>
                    <li><a href="#"><i class="iconfont icon-CNY"></i>{{item.marketcap | cnyFun(CNY,2)}}</a></li>
                    <li><a href="#"><i style="font-size:16px; color:#909499;" class="iconfont">&#xe604;</i>···</a></li>
                  </ul>
                </div>
                 </a>
                <!-- <div class="pt20"></div> -->
              </div>
            </div>
            <!-- 富文本区 -->
            <div class="mainBibar-editor" style="width:860px; margin:auto; background:#fff;">
              <BibarPostContent @backFtContent = 'BibarContentFun'></BibarPostContent>
            </div>
            <!--新闻-->
            <article class="bibar-box bibar-boxindex2">
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
        </section>
        <!--主体右侧-->
        <section class="bibar-Mainright">
            <BibarRight></BibarRight>
        </section>
    </section>
    <div class="pt40"></div>
    </section>
  </div>
</template>
<script>
import MainHeader from '../common/header.vue'
import btb from './BibarChart/BTB.vue'
import eth from './BibarChart/ETH.vue'
import xrp from './BibarChart/XRP.vue'
import BibarRight from './BibarRight/bivarRight.vue'
import BibarPostContent from '../homePage/bibarPostContent.vue'
import {get} from '../../utils/http'

export default{
  data: function () {
    return {
      newList: ['全部', '讨论', '文章', '新闻', '交易'],
      newRouter: ['all', 'talk', 'works', 'news', 'trade'],
      state: 0,
      i: 1,
      collapseId: '',
      hrefCollapse: '',
      cpno: 1,
      cpageSize: 10,
      BTC: 0,
      CNY: 0,
      summaryList: [],
      upSty: false
    }
  },
  components: {
    MainHeader,
    btb,
    eth,
    xrp,
    BibarRight,
    BibarPostContent
  },
  created () {
    this.collapseId = `collapse${this.i++}`
    this.hrefCollapse = `#${this.collapseId}`
  },
  mounted () {
    get(`/api/blist/${this.cpno}/${this.cpageSize}`).then((data) => {
      this.BTC = data.data.exrateData.BTC
      this.CNY = data.data.exrateData.CNY
      this.summaryList = data.data.summaryList
      // console.log(this.summaryList[0].indexOf('-'))
      // for (var i = 0; i < this.summaryList.length; i++) {
      //   if (this.summaryList[i].indexOf('-')) {
      //     this.upSty = false
      //   } else {
      //     this.upSty = true
      //   }
      // }
      $('.mainBibar-editor').find('.wangeditor').css({'width': '860px'})
    })
  },
  methods: {
    // 文章列表切换事件
    changeActive: function (index) {
      if (index !== this.state) {
        this.state = index
        this.$router.push(`/bibarLayout/${this.newRouter[this.state]}`)
      }
    },
    BibarContentFun (data) {
      this.$refs.showBibarContent.showBibarContentFun(data)
    }
  }
}
</script>

<style>
.bibarMainGzList{background: #fff}
.bibar-list-item{
  /* padding: 0 40px; */
  overflow: hidden;
  position: relative;
}
.bibar-box{box-shadow: none;}
.bibar-list-item ul li{
  float: left;
  margin: 10px 25px;
}
.bibar-list-item ul li a{
    font-size: 16px;
    font-weight: bold;
}
.bibar-list-item ul li:first-child a span img{
    width: 20px;
    height: 20px;
    margin-top: -3px;
}
.panel-tb-hd{
  display: block;
  padding-top: 10px;
  margin:  0 40px;
}
.down-avtive{color: #009525 !important;}
.up-active{color:#D70508 !important;}
.panel-group .panel+.panel {
    margin-top: 0 !important;
}
.panel-group .panel{
  border-radius: 0 !important;
  border:none !important;
}
.panel-body, .bibar-boxindex1{padding-bottom: 0 !important;}

</style>
