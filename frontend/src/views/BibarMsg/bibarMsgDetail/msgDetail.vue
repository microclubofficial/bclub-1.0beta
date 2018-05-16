<template>
  <div class="main">
    <MainHeader></MainHeader>
    <!--主体-->
    <section class="bibar-Main">
    <!--<div class="pt20"></div>-->
    <section class="bibar-w1100">
        <!--主体左侧-->
        <section class="bibar-Mainleft bx-mainLeft">
            <btb @btbFun='frombtb' :bId="bitId"></btb>
            <!-- 富文本区 -->
            <div class="mainBibar-editor" v-if='initHide'>
              <BibarPostContent :tokenBibar='tokenName' @backFtContent = 'BibarContentFun' ></BibarPostContent>
            </div>
            <!--新闻-->
            <article class="bibar-box bibar-boxindex2">
                <div class="bibar-indexNews">
                    <div class="bibar-indexNews-TAB">
                        <ul class="bibar-tabs-listSty2">
                            <li class="bibar-tabs-item active"> <a href="#bibar-newstab1" data-toggle="tab">讨论</a></li>
                            <!--<li class="bibar-tabs-item" :key='index' v-for="(tmp,index) in newList" :class="{active:state==index}" @click="changeActive(index)"> <a href="#bibar-newstab1" data-toggle="tab">{{tmp}}</a></li>-->
                        </ul>
                    </div>
                    <!--新闻列表-->
                    <router-view ref="showBibarContent"></router-view>
                </div>
            </article>
        </section>
        <!--主体右侧-->
        <section class="bibar-Mainright">
            <BibarRight :bId='bitId'></BibarRight>
        </section>
    </section>
    <div class="pt40"></div>
    </section>
  </div>
</template>
<script>
import MainHeader from '../../common/header.vue'
import btb from '../BibarChart/BTB.vue'
import BibarRight from '../BibarRight/bivarRight.vue'
import BibarPostContent from '../../homePage/bibarPostContent.vue'

export default{
  data: function () {
    return {
      newList: ['全部', '讨论', '文章', '新闻', '交易'],
      newRouter: ['all', 'talk', 'works', 'news', 'trade'],
      state: 0,
      i: 1,
      collapseId: '',
      hrefCollapse: '',
      bitId: '',
      initHide: false,
      initShow: false,
      showLoader: true,
      // token
      tokenName: ''
    }
  },
  components: {
    MainHeader,
    btb,
    BibarRight,
    BibarPostContent
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  created () {
    this.collapseId = `collapse${this.i++}`
    this.hrefCollapse = `#${this.collapseId}`
  },
  mounted () {
    this.loadShow()
    // 币种
    this.bitId = this.$route.params.currency
    // 富文本样式
    // $('.mainBibar-editor').find('.wangeditor').css({'width': '860px'})
    let scope = $('.bibar-list-item ul li:eq(2)').find('span').html()
    let scopeStyle = $('.bibar-list-item ul li:eq(2)').find('a')
    if (scope === '-') {
      scopeStyle.addClass('down-avtive')
    } else if (scope === '+') {
      scopeStyle.addClass('up-avtive')
    }
    $('.bx-mainLeft').find('.wangeditor').css({'padding-left': '14%'})
  },
  methods: {
    // 文章列表切换事件
    changeActive: function (index) {
      if (index !== this.state) {
        this.state = index
        this.$router.push(`/msgDetail/${this.bitId}/${this.newRouter[this.state]}`)
      }
    },
    BibarContentFun (data) {
      this.$refs.showBibarContent.showBibarContentFun(data)
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
    },
    frombtb (data) {
      this.tokenName = data
    }
  }
}
</script>

<style>
  /*币讯富文本样式*/
  .mainBibar-editor{
    /*width: 960px;*/
    margin: auto;
    background: rgb(255, 255, 255);
    padding:40px;
  }
  .mainBibar-editor .wangeditor{
    width: 100% !important;
    background: #F8F8F8 !important;
  }
  .mainBibar-editor .wangeditor .editor{
    width: 94%;
  }
 .bibar-Main>.bibar-w1100>.bx-mainLeft{
   width: 960px;margin-top:20px;
   }
.bibarMainGzList{background: #fff}
.bibar-list-item{
  /* padding: 0 40px; */
  overflow: hidden;
  position: relative;
}
.bibar-box{box-shadow: none;}
.bibar-list-item ul li{
  float: left;
  margin: 10px 1px;
}
.bibar-list-item ul li a{
    font-size: 16px;
    font-weight: bold;
}
.bibar-list-item ul li:first-child a span{
  /* display: block; */
  color: #909499;
  font-size: 14px;
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
