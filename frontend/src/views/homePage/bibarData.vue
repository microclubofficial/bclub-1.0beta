
<style>@import 'swiper/dist/css/swiper.css'</style>
<style>
.commun-bibarData{
  width: 100%;
  position: relative;
  background: linen;
  /* margin-top: 80px; */
}
.commun-bibarData>.bibarData-main{
  width: 1100px;
  margin: 10px auto;
  padding: 10px 0;
}
.bibarData-box{
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.bibarData-box>li{
  width: 15%;
  height: 100px;
  /*margin-right: 1%;*/
  border: 1px solid #D7D7D7;
  background: #fff;
  margin-bottom: 1%;
  box-shadow:#ddd 2px 0px 3px 0px;
}
.bibarData-box>li>a{
  display: block;
  padding-left: 28px;
  height: 100px;
  padding-top: 20px;
}
.bibarData-main p{font-size: 14px}
.bibar-class>span{margin-left: 10px; width:18px; height:18px;}
.bibar-class>span>img{width:18px; height:18px;}
.swiper-wrapper{padding-bottom:45px;}
.swiper-container {
      width: 100%;
      height: 100%;
    }
.swiper-slide {
      font-size: 18px;
      /* background: #fff; */

      /* Center slide text vertically */
      display: -webkit-box;
      display: -ms-flexbox;
      display: -webkit-flex;
      display: flex;
      -webkit-box-pack: center;
      -ms-flex-pack: center;
      -webkit-justify-content: center;
      justify-content: center;
      -webkit-box-align: center;
      -ms-flex-align: center;
      -webkit-align-items: center;
      align-items: center;
    }
    .swiper-pagination-bullet {
      padding:3px 6px;
      text-align: center;
      line-height: 20px;
      font-size: 12px;
      color:#000;
      opacity: 1;
      background: #ffffff;
      margin: 0 10px;
      cursor: pointer;
      border-radius: 0 !important;
      display:initial !important;
    }
    .swiper-pagination-bullet-active {
      color:#fff;
      background: #007aff;
    }
</style>
<template>
  <swiper :options="swiperOption" ref="mySwiper">
    <!-- slides -->
    <swiper-slide>
      <ul class="bibarData-box">
          <li v-for="(tmp,index) in firstList" :key="index" @click='toBibarDetail(tmp)'>
            <a href="javascript:void(0)">
              <p class="bibar-class">
                {{tmp.symbol}}
                <span><img :src="tmp.picture" alt=""></span>
              </p>
              <h3><i class="iconfont" style="font-size:24px;margin-left:-5px;">&#xe634;</i>{{tmp.price * CNY | formatNum(2)}}</h3>
              <p style="color:#17B769" :class="tmp.change_1h >= 0 ? 'text-green' : 'text-red'">{{tmp.change_1h | bfb(2)}}</p>
            </a>
          </li>
        </ul>
    </swiper-slide>
    <swiper-slide>
      <ul class="bibarData-box">
          <li v-for="(tmp,index) in twoList" :key="index" @click='toBibarDetail(tmp)'>
            <a href="javascript:void(0)">
              <p class="bibar-class">
                {{tmp.symbol}}
                <span><img :src="tmp.picture" alt=""></span>
              </p>
              <h3><i class="iconfont" style="font-size:24px;margin-left:-5px;">&#xe634;</i>{{tmp.price | cnyFun(CNY,2)}}</h3>
              <p style="color:#17B769" :class="tmp.change_1h >= 0 ? 'text-green' : 'text-red'">{{tmp.change_1h | bfb(2)}}</p>
            </a>
          </li>
        </ul>
    </swiper-slide>
    <swiper-slide>
      <ul class="bibarData-box">
          <li v-for="(tmp,index) in threeList" :key="index" @click='toBibarDetail(tmp)'>
            <a href="javascript:void(0)">
              <p class="bibar-class">
                {{tmp.symbol}}
                <span><img :src="tmp.picture" alt=""></span>
              </p>
              <h3><i class="iconfont" style="font-size:24px;margin-left:-5px;">&#xe634;</i>{{tmp.price | cnyFun(CNY,2)}}</h3>
              <p style="color:#17B769" :class="tmp.change_1h >= 0 ? 'text-green' : 'text-red'">{{tmp.change_1h | bfb(2)}}</p>
            </a>
          </li>
        </ul>
    </swiper-slide>
    <!-- Optional controls -->
    <div class="swiper-pagination"  slot="pagination"></div>
  </swiper>
</template>

<script>
import { swiper, swiperSlide } from 'vue-awesome-swiper'
import {get} from '../../utils/http.js'
export default{
  name: 'carrousel',
  data: function () {
    return {
      firstList: [],
      twoList: [],
      threeList: [],
      pno: 1,
      hotCount: 12,
      CNY: 0,
      swiperOption: {
        pagination: {
          el: '.swiper-pagination',
          renderBullet: function (index, className) {
            return '<span class="' + className + '">' + (index + 1) + '</span>'
          },
          clickable: true
        },
        autoplay: {
          delay: 3000,
          stopOnLastSlide: false,
          disableOnInteraction: true
        }
      }
    }
  },
  components: {
    swiper,
    swiperSlide
  },
  computed: {
    swiper () {
      return this.$refs.mySwiper.swiper
    }
  },
  created () {
  },
  mounted: function () {
    let that = this
    // 币列表
    get(`/api/blist/1/${that.hotCount}`).then(data => {
      that.firstList = data.data.summaryList
      that.CNY = data.data.exrateData.CNY
    })
    get(`/api/blist/2/${that.hotCount}`).then(data => {
      that.twoList = data.data.summaryList
      that.CNY = data.data.exrateData.CNY
    })
    get(`/api/blist/3/${that.hotCount}`).then(data => {
      that.threeList = data.data.summaryList
      that.CNY = data.data.exrateData.CNY
    })
  },
  methods: {
    // 去币详情页
    toBibarDetail (tmp) {
      this.$router.push({
        path: `/msgDetail/${tmp.id}`,
        query: {
          b: JSON.stringify({'zh': tmp.name_ch})
        }
      })
    }
  }
}
</script>
<style>
.text-red{color:red;}
</style>
