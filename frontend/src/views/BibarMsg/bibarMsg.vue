
<template>
  <div class="main">
    <MainHeader @backLoadMain='toMainLoadFun'></MainHeader>
    <!--主体-->
    <section class="bibar-Main">
    <!-- <div class="pt40"></div> -->
    <section class="bibar-w1100">
      <!-- left slide -->
      <BibarLeft v-if="initHide"></BibarLeft>
        <!--主体左侧-->
        <section class="bibar-Mainleft" :class="{initSty:initShow}">
          <div class="chartListBox">
            <!-- chart列表 -->
            <div class="panel-group" id="accordion">
              <div class="panel panel-default" v-for="(item,index) in summaryList" :key='index'>
                <!-- <div id='collapseOne' class="panel-collapse collapse" :class="{in:chartShow === index}"> -->
                <div id='collapseOne' class="panel-collapse collapse in" v-if="chartShow === index">
                  <div class="panel-body">
                    <!--BTB信息框-->
                    <btb ref="toNowChild" :bId="item.id"></btb>
                  </div>
                </div>
                 <!-- 币种列表 -->
                 <a data-toggle="collapse" class="panel-tb-hd" data-parent="#accordion" href='#collapseOne'>
                  <div class="bibar-list-item" @click="chartShow = index">
                  <ul>
                    <li><a href="javascript:void(0)"><span><img :src="item.picture" alt=""></span> {{item.name_ch}} - {{item.symbol}}</a></li>
                    <li><a href="javascript:void(0)"><i class="iconfont icon-CNY"></i>{{item.price | cnyFun(CNY,2)}}</a></li>
                    <li><a href="javascript:void(0)">{{item.change_1h}}</a></li>
                    <li><a href="javascript:void(0)"><i class="iconfont icon-CNY"></i>{{item.volume | cnyFunStr(CNY,2)}}</a></li>
                    <li><a href="javascript:void(0)" :title="item.marketcap"><i class="iconfont icon-CNY"></i>{{item.marketcap | cnyFunStr(CNY,2)}}</a></li>
                    <li><a href="javascript:void(0)"><i style="font-size:16px; color:#909499;" class="iconfont">&#xe604;</i>···</a></li>
                  </ul>
                </div>
                 </a>
                <!-- <div class="pt20"></div> -->
              </div>
            </div>
            <!-- 分页条 -->
            <div class="pages">
              <ul class="mo-paging">
              <!-- prev -->
        <li class="paging-item paging-item--prev" :class="{'paging-item--disabled' : cpno === 1}" @click="prev">prev</li>
        <!-- first -->
        <li :class="['paging-item', 'paging-item--first', {'paging-item--disabled' : cpno === 1}]" @click="first">first</li>
        <li :class="['paging-item', 'paging-item--more']" v-if="showPrevMore">...</li>
        <li :class="['paging-item', {'paging-item--current' : cpno === tmp}]" :key="index" v-for="(tmp, index) in showPageBtn"  @click="go(tmp)">{{tmp}}</li>
        <li :class="['paging-item', 'paging-item--more']" v-if="showNextMore">...</li>
        <!-- next -->
        <li :class="['paging-item', 'paging-item--next', {'paging-item--disabled' : cpno === cpageCount}]" @click="next">next</li>
        <!-- last -->
        <li :class="['paging-item', 'paging-item--last', {'paging-item--disabled' : cpno === cpageCount}]"  @click="last">last</li>
        </ul>
            </div>
          </div>
            <!-- 富文本区 -->
            <div class="mainBibar-editor" :class="{initSty:initShow}" style="margin:auto; background:#fff;">
              <BibarPostContent @backFtContent = 'BibarContentFun' v-show="initHide"></BibarPostContent>
            </div>
            <!--新闻-->
            <article class="bibar-box bibar-boxindex2" style="margin-top:20px;">
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
        <section class="bibar-Mainright" v-show="initHide">
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
import BibarLeft from '../homePage/bibarLeft/bibarSideLeft.vue'
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
      BTC: null,
      CNY: null,
      summaryList: [],
      upSty: false,
      chartShow: 0,
      chartState: false,
      cpno: 1,
      cpageLimit: 10,
      cpageCount: 0,
      showPrevMore: false,
      showNextMore: false,
      initHide: false,
      initShow: false
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    },
    showPageBtn () {
      let pageArr = []
      if (this.cpageCount <= 5) {
        for (let i = 1; i <= this.cpageCount; i++) {
          pageArr.push(i)
        }
        return pageArr
      }
      if (this.cpno <= 2) return [1, 2, 3, '···', this.cpageCount]
      if (this.cpno >= this.cpageCount - 1) return [1, '···', this.cpageCount - 2, this.cpageCount - 1, this.cpageCount]
      if (this.cpno === 3) return [1, 2, 3, 4, '···', this.cpageCount]
      if (this.cpno === this.cpageCount - 2) return [1, '···', this.cpageCount - 3, this.cpageCount - 2, this.cpageCount - 1, this.cpageCount]
      return [1, '···', this.cpno - 1, this.cpno, this.cpno + 1, '···', this.cpageCount]
    }
  },
  components: {
    MainHeader,
    btb,
    BibarRight,
    BibarPostContent,
    BibarLeft
  },
  created () {
    this.collapseId = `collapse${this.i++}`
    this.hrefCollapse = `#${this.collapseId}`
    get(`/api/blist/${this.cpno}/${this.cpageLimit}`).then((data) => {
      // 总页数
      this.cpageCount = data.data.page_count
      this.BTC = data.data.exrateData.BTC
      this.CNY = data.data.exrateData.CNY
      this.summaryList = data.data.summaryList
    })
    if (this.chartShow === 0) {
      this.chartState = true
    }
    this.loadShow()
  },
  mounted () {
    $('.mainBibar-editor').find('.wangeditor').css({'width': '790px'})
    let app = document.getElementById('#app')
    app.scrollTop = 0
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
    // 分页
    prev () {
      if (this.cpno > 1) {
        this.go(this.cpno - 1)
      }
    },
    next () {
      if (this.cpno < this.cpageCount) {
        this.go(this.cpno + 1)
      }
    },
    first () {
      if (this.cpno !== 1) {
        this.go(1)
      }
    },
    last () {
      if (this.cpno !== this.cpageCount) {
        this.go(this.cpageCount)
      }
    },
    go (page) {
      this.chartShow = 0
      this.summaryList = []
      if (this.cpno !== page) {
        this.cpno = page
      }
      get(`/api/blist/${page}/${this.cpageLimit}`).then((data) => {
        // 总页数
        this.cpageCount = data.data.page_count
        this.BTC = data.data.exrateData.BTC
        this.CNY = data.data.exrateData.CNY
        this.summaryList = data.data.summaryList
      })
    },
    // 退登状态----重新加载页面
    toMainLoadFun () {
      this.loadShow()
    }
  }
}
</script>

<style>
.chartListBox{
  background: #fff;
  padding: 20px;
  position: relative;
  overflow: hidden;
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
    margin: 10px 0;
    width: 16%;
    text-align: center;
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
.panel-collapse{height: auto !important;}
.bibar-list-item ul li a{
    width: 16%;
    white-space: nowrap;
    text-overflow: ellipsis;
    -o-text-overflow: ellipsis;
    overflow: hidden;
}
/*分页*/
.pages{float: right;}
.mo-paging {
    display: inline-block;
    padding: 0;
    margin: 1rem 0;
    font-size: 0;
    list-style: none;
    user-select: none;
}
.mo-paging>.paging-item {
    display: inline;
    font-size: 14px;
    position: relative;
    padding: 6px 12px;
    line-height: 1.42857143;
    text-decoration: none;
    border: 1px solid #ccc;
    background-color: #fff;
    margin-left: -1px;
    cursor: pointer;
    color: #0275d8;
}
.mo-paging>.paging-item:first-child {
    margin-left: 0;
}
.mo-paging>.paging-item:hover {
    background-color: #f0f0f0;
    color: #0275d8;
}
.paging-item--disabled,.paging-item--more{
    background-color: #fff !important;
    color: #505050 !important;
}
/*禁用*/
.paging-item--disabled {
    cursor: not-allowed;
    opacity: .75;
}
.paging-item--more,.paging-item--current {
    cursor: default !important;
}
/*选中*/
.paging-item--current {
    background-color: #0275d8 !important;
    color:#fff !important;
    position: relative !important;
    z-index: 1 !important;
    border-color: #0275d8 !important;
}
.initLfSty{width: 1200px !important;}
.initSty{width: 1200px !important;}
.initClass{width: 1200px !important;}
</style>
