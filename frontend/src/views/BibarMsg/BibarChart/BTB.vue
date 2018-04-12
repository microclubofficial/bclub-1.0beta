<template>
<div>
   <article class="bibar-box bibar-boxindex1">
                <div class="bibarTop"  @click="toMsgDetail(bibarData.id)">
                  <div class="bibar-indexDisplay">
                    <div class="bibar-indexDisplay-header">
                        <div class="logopic"><img :src="bibarData.picture"></div>
                        <div class="logonameEnglish">{{bibarData.zhName}}</div>
                        <div class="logonameChinese">{{bibarData.symbol}}</div>
                    </div>
                    <a href="#" class="btn btn-default"><i class="iconfont icon-add-sm"></i> 关注</a> </div>
                <!--数-->
                <div class="bibar-indexDisplay-data"> <i class="iconfont icon-CNY" style="font-size:30px;"></i> <span class="bibar-indexDisplay-dollar">{{cny_price | formatNum(2)}}</span><span class="bibar-indexDisplay-rmb"><i class="iconfont icon-yueden"></i><i class="iconfont icon-USD"></i>{{bibarData.price | formatNum(2)}}</span> <span class="bibar-indexDisplay-den"><i class="iconfont icon-denyu"></i> <i class="iconfont icon-BTC"></i> {{bibarData.price | bitcoinFun(BTC_RATE,0)}}</span> </div>
                <!--涨跌-->
                <div class="bibar-indexDisplay-trend">
                    <div v-show="!isDown" class="bibar-indextrend green"> <span class="num">{{change1h}}</span> <i class="iconfont icon-angleup-bold"></i> </div>
                    <div v-show="isDown" class="bibar-indextrend red"> <span class="num">{{change1h}}</span> <i class="iconfont icon-angledown-bold"></i> </div>
                </div>
                <div class="clear hline"></div>
                <!--比值-->
                <div class="bibar-indexDisplay-datamore">
                    <div class="col-sm-6">
                        <dl>
                            <dt>市值</dt>
                            <dd> <i class="iconfont icon-CNY"></i>{{bibarData.marketCap
 | cnyFun(CNY_RATE,2)}}
                                <div class="sprit-12 bg-green ml10">第{{bibarData.level}}名</div>
                            </dd>
                            <dd> <i class="iconfont icon-yueden"></i> <i class="iconfont icon-rmb icon-USD"></i>{{bibarData.marketCap | formatNum(2)}} </dd>
                            <dd> <i class="iconfont icon-yueden"></i> <i class="iconfont icon-btb icon-BTC"></i> {{bibarData.marketCap | bitcoinFun(BTC_RATE)}} </dd>
                        </dl>
                        <dl>
                            <dt>占全球总市值</dt>
                            <dd> {{bibarData.global_market_rate}}
                                <div class="bibar-uipress"><span class="w40p"></span></div>
                            </dd>
                        </dl>
                        <dl>
                            <dt>总发行量</dt>
                            <dd> <i class="iconfont icon-btb icon-BTC"></i> {{bibarData.supple | formatNum(2)}} </dd>
                        </dl>
                    </div>
                    <div class="col-sm-6">
                        <dl>
                            <dt>交易量(24h)</dt>
                            <dd> <i class="iconfont icon-CNY"></i>{{bibarData.volume_ex | cnyFun(CNY_RATE,2)}}
                                <div class="sprit-12 bg-green ml10">第{{bibarData.volume_level}}名</div>
                            </dd>
                            <dd> <i class="iconfont icon-yueden"></i><i class="iconfont icon-USD"></i> {{bibarData.volume_ex | formatNum(2)}}</dd>
                            <dd> <i class="iconfont icon-yueden"></i><i class="iconfont icon-btb icon-BTC"></i>{{bibarData.volume_ex | bitcoinFun(BTC_RATE)}} </dd>
                        </dl>
                        <dl>
                            <dt>流通数量</dt>
                            <dd> <i class="iconfont icon-btb icon-BTC"></i> {{bibarData.available_supply | formatNum(2)}} </dd>
                        </dl>
                        <dl>
                            <dt>流通率</dt>
                            <dd> {{bibarData.Circulation_rate}}
                                <div class="bibar-uipress"><span class="w90p"></span></div>
                            </dd>
                        </dl>
                    </div>
                </div>
                <div class="clear hline"></div>
                </div>
                <article class="bibar-indexDisplay-chart">
                    <div class="bibar-indexDisplay-chartTAB">
                    </div>
                    <div class="clear hline"></div>
                    <!--chart-->
                    <div ref="chat" :style="{width:'780px',height:'450px',margin: '0 auto'}"></div>
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
import {get} from '../../../utils/http'

HighchartsMore(Highcharts)
HighchartsDrilldown(Highcharts)
Highcharts3D(Highcharts)

export default{
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
      nowId: ''
      // bId: 'bitcoin'
    }
  },
  mounted () {
    this.getChartData(this.bId)
  },
  computed: {
    chartId () {
      return this.$store.state.chartId.chartId
    }
  },
  methods: {
    // 获取chart数据
    getChartData (bId) {
      // https://data.jianshukeji.com/stock/history/000001
      var that = this
      this.bId = bId
      if (this.bId === '') {
        if (this.bId.length === 0) {
          this.bId = this.chartId
        }
      }
      $.getJSON(`/api/currency_news/${that.bId}`, function (data) {
        // main数据
        that.bibarData = data.data
        // 人民币汇率
        that.CNY_RATE = parseFloat(that.bibarData.CNY_RATE)
        // 比特币汇率
        that.BTC_RATE = parseFloat(that.bibarData.BTC_RATE)
        // 人民币转换
        that.cny_price = that.bibarData.price * that.CNY_RATE
        console.log(that.bibarData)
        // 涨幅
        that.change1h = that.bibarData.change1h
        var change1hStr = that.change1h.toString()
        if (change1hStr.indexOf('-') === -1) {
          that.isDown = false
        } else {
          that.isDown = true
        }
      })
      // k线图
      that.klineChart(that.bId)
    },
    // k线图
    klineChart (id) {
      let that = this
      get(`/api/kline/${id}`).then(data => {
        for (var j = 0; j < data.data.volume_usd.length; j++) {
          that.volumeData.push([
            data.data.volume_usd[j][0], // the date
            (data.data.volume_usd[j][1] * that.CNY_RATE) // the volume
          ])
        }
        for (var i = 0; i < data.data.price_usd.length; i++) {
          that.ohlc.push([
            data.data.price_usd[i][0], // the date
            (data.data.price_usd[i][1] * that.CNY_RATE) // 价格
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
          buttons: [{
            type: 'all',
            text: '所有'
          }, {
            type: 'month',
            count: 1,
            text: '1月'
          }, {
            type: 'month',
            count: 3,
            text: '3月'
          }, {
            type: 'month',
            count: 6,
            text: '6月'
          }, {
            type: 'ytd',
            text: 'YTD'
          }, {
            type: 'year',
            count: 1,
            text: '1年'
          }]
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
        yAxis: [{
          labels: {
            align: 'right',
            x: -3
          },
          height: '65%',
          resize: {
            enabled: true
          },
          lineWidth: 2
        }, {
          labels: {
            align: 'right',
            x: -3
          },
          top: '65%',
          height: '35%',
          offset: 0,
          lineWidth: 2
        }],
        series: [{
          type: 'spline',
          name: '价格(CNY)',
          color: '#306FCE',
          lineColor: '#306FCE',
          navigatorOptions: {
            color: Highcharts.getOptions().colors[0]
          },
          data: this.ohlc,
          id: 'sz'
        }, {
          type: 'column',
          name: '24交易量',
          data: this.volumeData,
          yAxis: 1
        }]
      })
    },
    // 去chart详情
    toMsgDetail (id) {
      this.msgId = id
      this.$store.commit('CHART_ID', {
        'chartId': this.msgId
      })
      this.$router.push(`/msgDetail/${this.msgId}`)
    },
    // 显示当前chart
    showNowChild (id) {
      this.nowId = id
      this.getChartData(id)
    }
  }
}
</script>
<style>
.bibar-indexDisplay-data i.icon-USD{font-size: 14px !important;}
.bibar-box{cursor: pointer;}
</style>
