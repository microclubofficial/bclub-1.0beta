<template>
<div>
   <article class="bibar-box bibar-boxindex1">
          <div class="loader" style="top:20%; left:33%; z-index:10004;" v-if='showLoader'>
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                      <div class="dot"></div>
                    </div>
                <div class="bibarTop"  @click="toMsgDetail(bibarData.id, bibarData.zhName)" v-if='!showLoader'>
                  <div class="bibar-indexDisplay">
                    <div class="bibar-indexDisplay-header">
                        <div class="logopic"><img :src="bibarData.picture"></div>
                        <div class="logonameEnglish">{{bibarData.zhName}}</div>
                        <div class="logonameChinese">{{bibarData.symbol}}</div>
                    </div>
                    <!--<a href="#" class="btn btn-default"><i class="iconfont icon-add-sm"></i> 关注</a>-->
                    </div>
                <!--数-->
                <div class="bibar-indexDisplay-data"> <i class="iconfont icon-rmb">&#xe634;</i> <span class="bibar-indexDisplay-dollar">{{cny_price | formatNum(2)}}</span><span class="bibar-indexDisplay-rmb"><i class="iconfont">&#xe6ca;</i><i class="iconfont icon-CNY">&#xe736;</i>{{bibarData.price | formatNum(2)}}</span> <span class="bibar-indexDisplay-den"><i class="iconfont icon-denyu">=</i> <i class="iconfont icon-BTC">&#xe63a;</i> {{bibarData.price | bitcoin(BTC_RATE, nowId)}}</span> </div>
                <!--涨跌-->
                <div class="bibar-indexDisplay-trend">
                    <div v-show="!isDown" class="bibar-indextrend green"> <span class="num">{{change1h}}</span> <i class="iconfont">&#xe618;</i> </div>
                    <div v-show="isDown" class="bibar-indextrend red"> <span class="num">{{change1h}}</span> <i class="iconfont">&#xe617;</i> </div>
                </div>
                <div class="clear hline"></div>
                <!--比值-->
                <div class="bibar-indexDisplay-datamore">
                    <div class="col-sm-6">
                        <dl>
                            <dt>{{$t('details.marketCap')}} :</dt>
                            <dd> <i class="iconfont icon-USD" v-if='(parseFloat(bibarData.marketCap) * CNY_RATE).toFixed(2) > 0'>&#xe634;</i>{{bibarData.marketCap | cnyFun(CNY_RATE,2)}}
                                <div v-if='(parseFloat(bibarData.marketCap) * CNY_RATE).toFixed(2) > 0' class="sprit-12 bg-green ml10">第{{bibarData.level}}名</div>
                            </dd>
                            <dd> <i v-if="parseFloat((bibarData.marketCap + '').replace(/[^\d.-]/g, '')).toFixed(2) + '' > 0" class="iconfont icon-yueden">&#xe6ca;</i> <i v-if="parseFloat((bibarData.marketCap + '').replace(/[^\d.-]/g, '')).toFixed(2) + '' > 0" class="iconfont icon-rmb icon-CNY">&#xe736;</i>{{bibarData.marketCap | formatNum(2)}} </dd>
                            <dd> <i v-if="(parseInt(bibarData.marketCap) * BTC_RATE).toFixed(2) > 0" class="iconfont icon-yueden">&#xe6ca;</i> <i v-if="(parseInt(bibarData.marketCap) * BTC_RATE).toFixed(2) > 0" class="iconfont icon-BTC">&#xe63a;</i> {{bibarData.marketCap | bitcoinFun(BTC_RATE)}} </dd>
                        </dl>
                        <dl>
                            <dt>{{$t('details.globalMarketRate')}} :</dt>
                            <dd> {{market > 0 ? bibarData.global_market_rate : '--'}}
                                <div v-if='market > 0' class="bibar-uipress"><span :style="{width:market + 'px'}"></span></div>
                            </dd>
                        </dl>
                        <dl>
                            <dt>{{$t('details.totalSupply')}} :</dt>
                            <dd>{{bibarData.supple | formatNum(2)}}&nbsp;&nbsp;<span class="logonameChinese">{{bibarData.symbol}}</span></dd>
                        </dl>
                    </div>
                    <div class="col-sm-6">
                        <dl>
                            <dt>{{$t('details.tradingVolume24h')}} :</dt>
                            <dd> <i v-if='(parseFloat(bibarData.volume_ex) * CNY_RATE).toFixed(2) > 0' class="iconfont icon-USD">&#xe634;</i>{{bibarData.volume_ex | cnyFun(CNY_RATE,2)}}
                                <div v-if='(parseFloat(bibarData.volume_ex) * CNY_RATE).toFixed(2) > 0' class="sprit-12 bg-green ml10">第{{bibarData.volume_level}}名</div>
                            </dd>
                            <dd> <i v-if="parseFloat((bibarData.volume_ex + '').replace(/[^\d.-]/g, '')).toFixed(2) + '' > 0" class="iconfont icon-yueden">&#xe6ca;</i><i v-if="parseFloat((bibarData.volume_ex + '').replace(/[^\d.-]/g, '')).toFixed(2) + '' > 0" class="iconfont icon-CNY">&#xe736;</i> {{bibarData.volume_ex | formatNum(2)}}</dd>
                            <dd> <i v-if="(parseInt(bibarData.volume_ex) * BTC_RATE).toFixed(2) > 0" class="iconfont icon-yueden">&#xe6ca;</i><i v-if="(parseInt(bibarData.volume_ex) * BTC_RATE).toFixed(2) > 0" class="iconfont icon-btb icon-BTC">&#xe63a;</i>{{bibarData.volume_ex | bitcoinFun(BTC_RATE)}} </dd>
                        </dl>
                        <dl>
                            <dt>{{$t('details.availableSupply')}} :</dt>
                            <dd>{{bibarData.available_supply | formatNum(2)}}&nbsp;&nbsp;<span v-if="parseFloat((bibarData.available_supply + '').replace(/[^\d.-]/g, '')).toFixed(2) + '' > 0" class="logonameChinese">{{bibarData.symbol}}</span></dd>
                        </dl>
                        <dl>
                            <dt>{{$t('details.circulationRate')}} :</dt>
                            <dd> {{rate > 0 ? bibarData.Circulation_rate : '--'}}
                                <div v-if='rate > 0' class="bibar-uipress"><span :style="{width:rate + 'px'}"></span></div>
                            </dd>
                        </dl>
                    </div>
                </div>
                <div class="clear hline"></div>
                </div>
                <article class="bibar-indexDisplay-chart">
                    <div class="bibar-indexDisplay-chartTAB">
                    </div>
                    <div class="clear hline" v-if='!showLoader'></div>
                    <!--chart-->
                    <div ref="chat" :style="{width:'810px',height:'450px',margin: '0 auto'}" :class="{initChart:initShow}"></div>
                </article>
            </article>

</div>
</template>

<script>
import Highcharts from 'highcharts/highstock'
import HighchartsMore from 'highcharts/highcharts-more'
import HighchartsDrilldown from 'highcharts/modules/drilldown'
import Highcharts3D from 'highcharts/highcharts-3d'
import $ from 'jquery'
import { get } from '../../../utils/http'

HighchartsMore(Highcharts)
HighchartsDrilldown(Highcharts)
Highcharts3D(Highcharts)

export default {
  name: 'bibar',
  props: ['bId'],
  data: function () {
    return {
      id: 'chart',
      ohlc: [],
      volumeData: [],
      bibarData: {},
      kline: {},
      price: null,
      CNY_RATE: 0,
      BTC_RATE: 0,
      cny_price: 0,
      change1h: null,
      isDown: false,
      msgId: '',
      chartList: [],
      nowId: '',
      // bId: 'bitcoin',
      market: 0,
      initmarket: 0,
      rate: 0,
      initmarketT: 0,
      timer: null,
      timerT: null,
      routerId: '',
      showLoader: false
    }
  },
  created () {
    this.loadShow()
  },
  watch: {
    $route (val) {
      this.getChartData(val.params.currency)
    }
  },
  mounted () {
    this.routerId = this.$route.params.currency
    this.getChartData(this.bId)
  },
  computed: {
    chartId () {
      return this.$store.state.chartId.chartId
    },
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  methods: {
    // 获取chart数据
    getChartData (bId) {
// https://data.jianshukeji.com/stock/history/000001
      var that = this
      if (bId) {
        this.nowId = bId
      } else if (this.bId) {
        this.nowId = this.bId
      } else if (this.$route.params.currency) {
        this.nowId = this.$route.params.currency
      } else {
        this.nowId = this.chartId
      }
      this.showLoader = true
      $.getJSON(`/api/currency_news/${this.nowId}`, function (data) {
        this.showLoader = false
        // main数据
        that.bibarData = data.data
        // 父组件传值
        that.$emit('btbFun', that.bibarData.zhName)
        // 总市值进度条
        that.market = parseFloat(that.bibarData.global_market_rate.split(/%/g)[0])
        // 流通率进度条
        that.rate = parseFloat(that.bibarData.Circulation_rate.split(/%/g)[0])
        // 人民币汇率
        that.CNY_RATE = parseFloat(that.bibarData.CNY_RATE)
        // 比特币汇率
        that.BTC_RATE = parseFloat(that.bibarData.BTC_RATE)
        // 人民币转换
        that.cny_price = that.bibarData.price * that.CNY_RATE
        // 涨幅
        that.change1h = that.bibarData.change1h
        var change1hStr = that.change1h.toString()
        if (change1hStr.indexOf('-') === -1) {
          that.isDown = false
        } else {
          that.isDown = true
        }
        // k线图
        that.klineChart(that.nowId)
      })
    },
    // k线图
    klineChart (id) {
      let that = this
      get(`/api/kline/${id}`).then(data => {
        that.showLoader = false
        that.volumeData = []
        for (var j = 0; j < data.data.volume_usd.length; j++) {
          that.volumeData.push([
            data.data.volume_usd[j][0], // the date
            data.data.volume_usd[j][1] * that.CNY_RATE // the volume
          ])
        }
        that.ohlc = []
        for (var i = 0; i < data.data.price_usd.length; i++) {
          that.ohlc.push([
            data.data.price_usd[i][0], // the date
            data.data.price_usd[i][1] * that.CNY_RATE // 价格
          ])
        }
        that.drawChart()
      })
    },
    // 绘制chart
    drawChart () {
      Highcharts.stockChart(this.$refs.chat, {
        rangeSelector: {
          selected: 1,
          inputDateFormat: '%Y-%m-%d',
          inputEnabled: false,
          buttons: [
            {
              type: 'all',
              text: '所有'
            },
            {
              type: 'month',
              count: 1,
              text: '1月'
            },
            {
              type: 'month',
              count: 3,
              text: '3月'
            },
            {
              type: 'month',
              count: 6,
              text: '6月'
            },
            {
              type: 'year',
              count: 1,
              text: '1年'
            }
          ]
        },
        title: {
          text: ''
        },
        credits: {
          enabled: false
        },
        xAxis: {
          dateTimeLabelFormats: {
            millisecond: '%H:%M:%S.%L',
            second: '%H:%M:%S',
            minute: '%H:%M',
            hour: '%H:%M',
            day: '%m-%d',
            week: '%m-%d',
            month: '%y-%m',
            year: '%Y'
          }
        },
        tooltip: {
          split: false,
          shared: true
        },
        legend: {
          enabled: true,
          align: 'right',
          // layout: 'vertical',
          verticalAlign: 'top'
        },
        yAxis: [
          {
            labels: {
              align: 'right',
              x: -3
            },
            height: '65%',
            resize: {
              enabled: true
            },
            lineWidth: 2
          },
          {
            labels: {
              align: 'right',
              x: -3
            },
            top: '65%',
            height: '35%',
            offset: 0,
            lineWidth: 2
          }
        ],
        series: [
          {
            type: 'spline',
            name: '价格(CNY)',
            color: '#306FCE',
            lineColor: '#306FCE',
            navigatorOptions: {
              color: Highcharts.getOptions().colors[0]
            },
            data: this.ohlc,
            id: 'sz'
          },
          {
            type: 'column',
            name: '24交易量',
            data: this.volumeData,
            yAxis: 1,
            color: '#44DFE4'
          }
        ]
      })
    },
    // 去chart详情
    toMsgDetail (id, zh) {
      this.msgId = id
      this.$store.commit('CHART_ID', {
        chartId: this.msgId,
        chartCh: this.bibarData.zhName
      })
      this.$router.push({path: `/msgDetail/${this.msgId}`})
    },
    // 显示当前chart
    showNowChild (id) {
      this.nowId = id
      this.getChartData(this.nowId)
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
    }
    // 调chart图
    // getChart (id) {
    //   this.getChartData(id)
    // }
  }
}
</script>
<style>
  /*.bibar-indexDisplay-chart .loader{
      top: 50%;
      left: 30%;
      z-index: 10004;
  }*/
  .bibar-uipress span{
    transition: width .5s;
  }
.bibar-indexDisplay-data i.icon-USD {
  font-size: 14px !important;
}
.bibar-box {
  cursor: pointer;
}
.initChart{width: 810px !important;}
</style>
