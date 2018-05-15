<style lang='scss' scoped>
.bibar-list-header {
  table {
    text-align: left;
    margin-bottom: 0;
    thead {
      // background-color: #e7f4ff;
      th {
        font-size: 16px;
        font-weight: bold;
        padding: 16px 0;
      }
    }
    tbody {
      border: none;
      tr {
        cursor: pointer;
        // border: none;
        td {
          // border: none;
          font-size: 15px;
          padding: 16px 0;
          a {
            font-weight: 600;
            img {
              width: 20px;
              height: 20px;
              margin-right: 6px;
            }
          }
        }
      }
    }
  }
}
</style>

<template>
  <div class="main">
    <!--<MainHeader @backLoadMain='toMainLoadFun'></MainHeader>-->
    <MainHeader></MainHeader>
    <!--主体-->
    <section class="bibar-Main">
      <!-- <div class="pt40"></div> -->
      <section class="bibar-w1100">
        <!-- left slide -->
        <!--<BibarLeft v-if="initHide"></BibarLeft>-->
        <!--主体左侧-->
        <section class="bibar-Mainleft bx-mainLeft">
          <div class="chartListBox">
            <!-- chart列表 -->
            <div class="bibar-list-header">
              <table class="table table-hover">
                <!--<caption>Optional table caption.</caption>-->
                <thead>
                  <tr>
                    <th style="padding-left:50px;">#</th>
                    <th>名称</th>
                    <th>价格</th>
                    <th>涨跌幅</th>
                    <th>交易量</th>
                    <th>流通市值</th>
                    <th>流通数量</th>
                    <!--<th></th>-->
                  </tr>
                </thead>
                <tbody>
                  <!--<tr v-if="chartShow === index">
                    <td colspan="7">
                      <btb ref="toNowChild" :bId="item.id"></btb>
                    </td>
                  </tr>-->
                  <tr @click='toBibarDetail(item)' v-for="(item,index) in summaryList" :key='index'>
                    <td>
                      <a href="javascript:void(0)" @click='toBibarDetail(item)'>{{index + 1}}</a>
                    </td>
                    <td>
                      <a href="javascript:void(0)" @click='toBibarDetail(item)'>
                        <span><img :src="item.picture" alt=""></span> {{item.name_ch}} - {{item.symbol}}
                      </a>
                    </td>
                    <td>
                      <a href="javascript:void(0)" @click='toBibarDetail(item)'>
                        <i class="iconfont icon-CNY"></i>￥ {{item.price * CNY | formatNum(2)}}
                      </a>
                    </td>
                    <td :class="item.change_1h >= 0 ? 'text-green' : 'text-red'">{{item.change_1h | bfb(2)}}</td>
                    <td>
                      <i class="iconfont icon-CNY"></i>￥ {{item.volume | cnyFunStr(CNY,2)}}</td>
                    <td :title="item.marketcap">
                      <i class="iconfont icon-CNY"></i>￥ {{item.marketcap | cnyFunStr(CNY,2)}}</td>
                    <td>{{item.available_supply | cnyFunStr(CNY,2)}}</td>
                    <!--<td @click="toggleChart(index)">
                      <i style="font-size:16px; color:#909499; cursor:pointer;" class="iconfont">&#xe604;</i>
                    </td>-->
                  </tr>
                </tbody>
              </table>
              <div class="loader" v-if='showLoader'>
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
              </div>
            </div>
            <div style="border-bottom:1px solid #e8e8e8;margin-bottom:20px;"></div>
            <!-- 分页条 -->
            <div class="pages" v-if='summaryList.length > 0'>
              <ul class="mo-paging">
                <!-- prev -->
                <!-- first -->
                <li :class="['paging-item', 'paging-item--first', {'paging-item--disabled' : cpno === 1}]" @click="first">首页</li>
                <li class="paging-item paging-item--prev" :class="{'paging-item--disabled' : cpno === 1}" @click="prev">上一页</li>
                <li :class="['paging-item', {'paging-item--current' : cpno === tmp}]" :key="index" v-for="(tmp, index) in showPageBtn" @click="go(tmp)">{{tmp}}</li>
                <!--<li :class="['paging-item', 'paging-item--more']" @click="next" v-if="showNextMore">...</li>-->
                <!-- next -->
                <li :class="['paging-item', 'paging-item--next', {'paging-item--disabled' : cpno === cpageCount}]" @click="next">下一页</li>
                <!-- last -->
                <li :class="['paging-item', 'paging-item--last', {'paging-item--disabled' : cpno === cpageCount}]" @click="last">尾页</li>
              </ul>
            </div>
          </div>
          <!-- 富文本区 -->
          <!--<div class="mainBibar-editor" :class="{initSty:initShow}" style="margin:auto; background:#fff;">
            <BibarPostContent :bid='toEditorBid' @backFtContent='BibarContentFun' v-show="initHide"></BibarPostContent>
          </div>-->
          <!--新闻-->
          <article v-if="initHide" class="bibar-box bibar-boxindex2" style="margin-top:20px;">
            <div class="bibar-indexNews">
              <div class="bibar-indexNews-TAB">
                <ul class="bibar-tabs-listSty2">
                  <li class="bibar-tabs-item active">
                    <a href="#bibar-newstab1" data-toggle="tab">全部</a>
                  </li>
                  <!--<li class="bibar-tabs-item" :key='index' v-for="(tmp,index) in newList" :class="{active:state==index}" @click="changeActive(index)"> <a href="#bibar-newstab1" data-toggle="tab">{{tmp}}</a></li>-->
                </ul>
              </div>
              <!--新闻列表-->
              <!--<router-view ref="showBibarContent"></router-view>-->
            </div>
          </article>
        </section>
        <!--主体右侧-->
        <section class="bibar-Mainright">
          <BibarRight ref="showBrief"></BibarRight>
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
import { get } from '../../utils/http'

export default {
  data: function () {
    return {
      newList: ['全部', '讨论', '文章', '新闻', '交易'],
      newRouter: ['all', 'talk', 'works', 'news', 'trade'],
      state: 0,
      i: 1,
      collapseId: '',
      hrefCollapse: '',
      BTC: null,
      CNY: 0,
      summaryList: [],
      upSty: false,
      chartShow: 0,
      chartState: false,
      cpno: 1,
      cpageLimit: 20,
      cpageCount: 0,
      showPrevMore: false,
      showNextMore: false,
      initHide: false,
      initShow: false,
      toEditorBid: '',
      showLoader: false
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
    this.showLoader = true
    get(`/api/blist/${this.cpno}/${this.cpageLimit}`).then((data) => {
      // 总页数
      this.cpageCount = data.data.page_count
      this.BTC = data.data.exrateData.BTC
      this.CNY = data.data.exrateData.CNY
      this.summaryList = data.data.summaryList
      this.showLoader = false
    })
    if (this.chartShow === 0) {
      this.chartState = true
    }
  },
  mounted () {
    $('.mainBibar-editor').find('.wangeditor').css({ 'width': '790px' })
    // this.loadShow()
    // this.$refs.showBrief.briefFun('bitcoin')
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
    // loadShow () {
    //   if (!this.userInfo.isLogin) {
    //     this.initShow = true
    //     this.initHide = false
    //   } else {
    //     this.initShow = false
    //     this.initHide = true
    //   }
    // },
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
      if (page === '···') {
        return
      }
      this.chartShow = 0
      // this.summaryList = []
      if (this.cpno !== page) {
        this.cpno = page
      }
      this.showLoader = true
      get(`/api/blist/${page}/${this.cpageLimit}`).then((data) => {
        // 总页数
        this.cpageCount = data.data.page_count
        this.BTC = data.data.exrateData.BTC
        this.CNY = data.data.exrateData.CNY
        this.summaryList = data.data.summaryList
        this.showLoader = false
      })
    },
    // 改变币列表
    changeBList (index, item) {
      this.chartShow = index
      this.$refs.showBrief.briefFun(item.id)
    },
    // 去币详情
    toBibarDetail (tmp) {
      this.$router.push({
        path: `/msgDetail/${tmp.id}`,
        query: {
          b: JSON.stringify({'zh': tmp.name_ch})
        }
      })
    }
    // // 展开折叠chart图
    // toggleChart(index) {
    //   this.chartShow = index
    // }
    // 调chart图
    // toChart (id) {
    //   console.log(id)
    //   this.$refs.showChart.getChart(id)
    // }
    // // 退登状态----重新加载页面
    // toMainLoadFun () {
    //   this.loadShow()
    // }
  }
}
</script>

<style>
.bibar-Main>.bibar-w1100>.bx-mainLeft {
  width: 960px;
  margin-top:20px;
}

.chartListBox {
  background: #fff;
  padding: 40px;
  position: relative;
  overflow: hidden;
}
/*table样式*/
.bibar-list-header table thead{
  background: #E7F4FF;
  border:none;
}
.bibar-list-header table thead tr{
  border:none;
}
.bibar-list-header table thead tr th{
  border:none;
}
.bibar-list-header table thead tr th{
    color: #000;
    font-size: 16px;
    font-weight: 400;
    min-width: 15px;
    max-width: 150px;
    padding: 0 5px;
    white-space: nowrap;
}
.bibar-list-header table thead tr th:nth-child(2){
    width: 200px;
}
.bibar-list-header table tbody tr td{
  border-top:none;
  border-top: 1px solid #f3f3f3;
  padding: 20px 0;
}
.bibar-list-header table tbody tr:first-child td{
  border:none;
}
.bibar-list-header table tbody tr td:first-child{
  padding-left: 50px;
}
.bibarMainGzList {
  background: #fff
}

.bibar-list-item {
  /* padding: 0 40px; */
  overflow: hidden;
  position: relative;
}

.bibar-box {
  box-shadow: none;
}

.bibar-list-item ul li {
  float: left;
  margin: 10px 0;
  width: 16%;
  text-align: center;
}

.bibar-list-item ul li:first-child {
  text-align: left;
  margin-right: 22px;
}

.bibar-list-item ul li a {
  font-size: 16px;
  font-weight: bold;
}

.bibar-list-item ul li:first-child a span img {
  width: 20px;
  height: 20px;
  margin-top: -3px;
}

.panel-tb-hd {
  display: block;
  padding-top: 10px;
  margin: 0 40px;
}

.down-avtive {
  color: #009525 !important;
}

.up-active {
  color: #D70508 !important;
}

.panel-group .panel+.panel {
  margin-top: 0 !important;
}

.panel-group .panel {
  border-radius: 0 !important;
  border: none !important;
}

.panel-body,
.bibar-boxindex1 {
  padding-bottom: 0 !important;
}

.panel-collapse {
  height: auto !important;
}

.bibar-list-item ul li a {
  width: 16%;
  white-space: nowrap;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
  overflow: hidden;
}

/*分页*/

.pages {
  float: right;
}

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

.paging-item--disabled,
.paging-item--more {
  background-color: #fff !important;
  color: #505050 !important;
}

/*禁用*/

.paging-item--disabled {
  cursor: not-allowed;
  opacity: .75;
}

.paging-item--more,
.paging-item--current {
  cursor: default !important;
}
















/*选中*/

.paging-item--current {
  background-color: #0275d8 !important;
  color: #fff !important;
  position: relative !important;
  z-index: 1 !important;
  border-color: #0275d8 !important;
}

.initLfSty {
  width: 1200px !important;
}

.initSty {
  width: 960px !important;
}

.initClass {
  width: 1200px !important;
}

.initListSty {
  margin-left: 35px;
  margin-right: 0px !important;
}
</style>
