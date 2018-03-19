<template>
  <div class="main">
    <MainHeader></MainHeader>
    <!--主体-->
    <section class="bibar-Main">
    <div class="pt40"></div>
    <section class="bibar-w1100">
        <!--主体左侧-->
        <section class="bibar-Mainleft">
            <!--BTB信息框-->
            <Bibar></Bibar>
            <div class="pt20"></div>
            <!--新闻-->
            <article class="bibar-box bibar-boxindex2">
                <div class="bibar-indexNews">
                    <div class="bibar-indexNews-TAB">
                        <ul class="bibar-tabs-listSty2">
                            <li class="bibar-tabs-item" :key='index' v-for="(tmp,index) in newList" :class="{active:state==index}" @click="changeActive(index)"> <a href="#bibar-newstab1" data-toggle="tab">{{tmp}}</a></li>
                        </ul>
                    </div>
                    <!--新闻列表-->
                    <router-view></router-view>
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
import Bibar from './bibar.vue'
import BibarRight from './BibarRight/bivarRight.vue'

export default{
  data: function () {
    return {
      newList: ['全部', '讨论', '文章', '新闻', '交易'],
      newRouter: ['all', 'talk', 'works', 'news', 'trade'],
      state: 0
    }
  },
  created: function () {
  },
  components: {
    MainHeader,
    Bibar,
    BibarRight
  },
  methods: {
    // 文章列表切换事件
    changeActive: function (index) {
      if (index !== this.state) {
        this.state = index
        this.$router.push(`/${this.newRouter[this.state]}`)
      }
    }
  }
}
</script>
