<template>
<div>
 <!--简介-->
            <article class="bibar-box bibar-boxindex3" v-if="$route.path !== '/'">
                <div class="bibar-boxtitle"> <span class="name">简介</span> </div>
                <div class="bibar-boxbody">
                    <div class="bibar-indexintro">
                        <p>比特币（Bitcoin，简称BTC）是目前使用最为广泛的一种数字货币，它诞生于2009年1月3日，是一种点对点（P2P）传输的数字加密货币，总量2100万枚。比特币（Bitcoin，简称BTC）是目前使用最为广泛的一种数字货币，它诞生于2009年1月3日，是一种点对点（P2P）传输的数字加密货币，总量2100万枚。</p>
                    </div>
                    <a href="#" class="bibar-indexintromore text-theme" @click="showText">展开 <i class="iconfont icon-quan-arrowdown"></i></a>
                    <div class="bibar-indexinftrList">
                        <dl>
                            <dt>发行时间</dt>
                            <dd>2008/11/01</dd>
                        </dl>
                        <dl>
                            <dt>众筹价格</dt>
                            <dd>--</dd>
                        </dl>
                        <dl>
                            <dt>白皮书</dt>
                            <dd><a href="#" class="text-theme">bitcoin.org/bitbitcoin.org/bit</a></dd>
                        </dl>
                        <dl>
                            <dt>官网</dt>
                            <dd><a href="#" class="text-theme">bitcoin.org/bitbitcoin.org/bit</a></dd>
                        </dl>
                        <dl>
                            <dt>区块查询</dt>
                            <dd><a href="#" class="text-theme">blockchain.info</a></dd>
                        </dl>
                    </div>
                </div>
            </article>
            <!-- 热门话题 -->
            <!-- tab -->
      <div class="recommend-tab shadow-box" v-if="$route.path === '/'">
        <div class="hot_talk">
          <h5>热门话题<span>更多话题>></span></h5>
        </div>
        <ul id="myTab" class="nav nav-tabs">
          <li class="active" @click="showHotTab(0)"><a href="#tech" data-toggle="tab">全球</a></li>
          <li @click="showHotTab(1)"><a href="#future" data-toggle="tab">美股</a></li>
          <li @click="showHotTab(2)"><a href="#american" data-toggle="tab">沪深</a></li>
          <li @click="showHotTab(3)"><a href="#hongkong" data-toggle="tab">港股</a></li>
        </ul>
        <div id="myTabContent" class="tab-content">
          <div class="tab-pane fade in active" id="tech">
            <li></li>
          </div>
          <div class="tab-pane fade" id="future">
          </div>
          <div class="tab-pane fade" id="american">
          </div>
          <div class="tab-pane fade" id="hongkong">
          </div>
        </div>
      </div>
            <div class="pt20"></div>
            <!--影响力-->
            <div class="bibar-box bibar-boxindex3">
                <div class="bibar-boxtitle"> <span class="name">影响力</span> <span class="fr"><a href="#" @click="changePage(0)">上五位</a> <a href="#" @click="changePage(1)">下五位</a> </span></div>
                <div class="bibar-boxbody">
                    <ul class="bibar-indexYQLlist">
                        <li class="bibar-indexYQLitem" v-for="(tmp, index) in sideList" :key="index">
                            <div class="bibar-author"> <a href="#"><span class="photo"><img :src="tmp.avatar"></span> <span class="name">{{tmp.username}}</span> <span class="time">相关评论{{tmp.reply_count}}条</span> </a></div>
                            <!--<a href="#" class="btn btn-theme btn-outline">提问</a>-->
                          </li>
                    </ul>
                </div>
            </div>
            <div class="pt20"></div>
            <!--分析师-->
            <div class="bibar-box bibar-boxindex3">
                <div class="bibar-boxtitle"> <span class="name">分析师</span></div>
                <div class="bibar-boxbody">
                    <ul class="bibar-indexYQLlist">
                        <li class="bibar-indexYQLitem" v-for="(tmp,index) in analystList" :key="index">
                            <div class="bibar-author"> <a href="#"><span class="photo"><img :src="tmp.avatar"></span> <span class="name">{{tmp.username}}</span> <span class="time"><i class="iconfont icon-hot"></i> 热度{{tmp.sum_is_good}}</span> </a></div>
                            <!--<a href="#" class="btn btn-theme btn-outline">提问</a>-->
                            </li>
                    </ul>
                </div>
            </div>
            <div class="pt20"></div>
  <div class="indexrightscroll-top">
    <!--热门-->
    <div class="bibar-box bibar-boxindex3">
      <div class="bibar-boxtitle"> <span class="name">热门币</span> <a href="#" class="fr" @click="changeBtb(0)">上一页</a><a href="#" class="fr" @click="changeBtb(1)">下一页</a></div>
      <div class="bibar-boxbody">
        <ul class="bibar-indexRMlist">
          <li class="bibar-indexRMitem row" v-for="(tmp,index) in hotList" :key="index" @click='toBibarDetail(tmp)'>
            <div class="col-sm-4"><a href="#">{{tmp.symbol}}</a></div>
            <div class="col-sm-4"><span class="fr">{{tmp.price |  cnyFun(CNY,2)}}</span></div>
            <div class="col-sm-4"><span class="fr" :class="tmp.change_1h >= 0 ? 'text-green' : 'text-red'">{{tmp.change_1h | bfb(2)}}</span></div>
          </li>
        </ul>
      </div>
    </div>
    <div class="pt20"></div>
    <div class="bibar-indexFoot">
      <ul class="bibar-indexfootlist">
        <li class="bibar-indexfootitem"> <a href="#">币吧指南</a> <a href="#">币吧协议</a> <a href="#">应用工作</a> </li>
        <li class="bibar-indexfootitem"> <a href="#">申请开通币吧机构号</a> </li>
        <li class="bibar-indexfootitem"> <a href="#">侵权举报</a> <a href="#">网上有害信息举报专区</a> </li>
        <li class="bibar-indexfootitem"> 违法和不良信息举报：021-54060502 </li>
        <li class="bibar-indexfootitem"> <a href="#">联系我们</a> <span>© 2018 币吧</span> </li>
      </ul>
    </div>
  </div>
</div>
</template>

<script>
import $ from 'jquery'
import {get} from '../../../utils/http'
export default{
  data: function () {
    return {
      txt: '',
      txth: '',
      isBx: false,
      sideList: [],
      sidePage: 1,
      pageCount: 0,
      analystPage: 1,
      analystList: [],
      hotbPage: 1,
      hotCount: 8,
      hotList: [],
      hotPageCount: 0,
      CNY: 0,
      brief: []
    }
  },
  created: function () {
    this.txt = $('.bibar-indexintro').html()
    var divH = $('.bibar-indexintro').height()
    var $p = $('p', $('.bibar-indexintro')).eq(0)
    while ($p.outerHeight() > divH) {
      $p.text($p.text().replace(/(\s)*([a-zA-Z0-9]+|\W)(\.\.\.)?$/, '...'))
    };
    this.txth = $('.bibar-indexintro').html()
    $('#myTab li:eq(1) a').tab('show')
    // 影响力
    this.sideFun(this.sidePage)
    // 分析师
    this.analystFun(this.analystPage)
    // 热门币
    this.bibarHot(this.hotbPage)
    console.log(this.$route.path.split)
  },
  methods: {
    showText: function () {
      var btnTxt = $('.bibar-indexintromore').html()
      if (btnTxt === '展开 <i class="iconfont icon-quan-arrowdown"></i>') {
        $('.bibar-indexintromore').html('收起 <i class="iconfont icon-quan-arrowup"></i>')
        $('.bibar-indexintro').html(this.txth)
        $('.bibar-indexintro').css({'height': 'auto'})
      } else {
        $('.bibar-indexintromore').html('展开 <i class="iconfont icon-quan-arrowdown"></i>')
        $('.bibar-indexintro').html(this.txth)
        $('.bibar-indexintro').css({'height': '108px'})
      };
    },
    // 热门话题
    showHotTab (id) {
      if (id === 0) {
      }
    },
    // 影响力
    sideFun (pno) {
      get(`/api/side/influence/${pno}`).then(data => {
        this.sideList = data.data.reply
        this.pageCount = data.data.page_count
      })
    },
    // 影响力翻页
    changePage (id) {
      if (id === 0) {
        if (this.sidePage > 1 && this.sidePage < this.pageCount) {
          this.sidePage--
          this.sideFun(this.sidePage)
        }
      } else if (id === 1) {
        if (this.sidePage < this.pageCount) {
          this.sidePage++
          this.sideFun(this.sidePage)
        }
      }
    },
    // 分析师
    analystFun (pno) {
      get(`/api/side/analyst/${pno}`).then(data => {
        this.analystList = data.data.analyst
      })
    },
    // 热门币
    bibarHot (pno) {
      get(`/api/blist/${pno}/${this.hotCount}`).then(data => {
        this.hotList = data.data.summaryList
        this.CNY = data.data.exrateData.CNY
        this.hotPageCount = data.data.page_count
      })
    },
    // 热门币翻页
    changeBtb (id) {
      if (id === 0) {
        if (this.hotbPage > 1 && this.hotbPage < this.hotPageCount) {
          this.hotbPage--
          this.bibarHot(this.hotbPage)
        }
      } else if (id === 1) {
        if (this.hotbPage < this.hotPageCount) {
          this.hotbPage++
          this.bibarHot(this.hotbPage)
        }
      }
    },
    // 去币详情
    toBibarDetail (tmp) {
      this.$router.push(`/msgDetail/${tmp.id}`)
    },
    // 简介
    briefFun () {
      get('/api/side/tokenintroduce/')
    }
  }
}
</script>

<style>
.nav>li>a {
    padding: 8px 12px !important;
}
.hot_talk{padding: 10px 12px;}
.hot_talk>h5>span{
    float: right;
    font-size: 12px;
    color: #bfbfbf;}
.nav-tabs>li.active>a{
    color: #555;
    cursor: default;
    background-color: #F7F8F7 !important;
    border-top: 2px solid #26ADDD !important;
    border-right: none !important;
    border-left: none !important;
    border-bottom-color: transparent;
    border-radius: 0 !important;
}
.recommend-tab{background: #fff;}
.nav-tabs {
    border-top: 1px solid #F3F4F3 !important;
    border-bottom: 1px solid #F3F4F3 !important;
    background: #F7F8F7;
    margin: 10px 0 20px 0;
}
.btn {
    padding: 0px 5px !important;
}
.text-red{color:red;}
</style>
