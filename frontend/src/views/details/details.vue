<template>
  <div class="list-detail">
    <main-header></main-header>
    <div class="article_container">
      <div class="article_author">
        <div class="top_left">
          <a href="/5900650325" target="_blank" class="avatar"><img src="//xavatar.imedao.com/community/20176/1500374689983-1500374700915.png!100x100.png" alt="金氪投行之家"></a>
        </div>
        <div class="top_right">
          <div class="avatar_name">
            <a href="/5900650325" target="_blank" class="name">金氪投行之家</a>
          </div>
          <div class="avatar_subtitle">
            <span class="source">来自币吧</span>
            <a href="" target="_blank" class="time">&ensp;发布于3分钟前</a>
          </div>
        </div>
      </div>
      <article class="article_bd">
        <h1 class="article_bd_title">3月14日新三板复盘:一路起起伏伏做市收跌0.14%</h1>
        <div class="article_bd_from">来自
          <a href="">金氪投行之家的雪球原创专栏</a>
        </div>
        <p>
          <strong>金氪3月14日讯：</strong>3月14日新三板新增挂牌企业1家，终止挂牌企业1家，共挂牌企业11614家，其中集合竞价10305家，做市转让1309家。 新挂牌企业：中联汇通 终止挂牌企业：顶联信息 退出做市企业：迈奇化学 市场数据： 今日，新三板共有654只股票发生交易，总成金额逾3.77亿元，其中做市转让389只股，成交超1.49亿元；集合竞价265只股，成交近2.28亿元，总成交数量为7761.50万股。 指数方面，三板做市指数（899002）以934.23点开盘，整天小幅缓慢下跌，截止收盘报932.93点，跌幅为0.14%，成分股成交6370万元 作者：金氪投行之家 链接：https://xueqiu.com/5900650325/103158626 来源：雪球 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        </p>
        <div class="image">
          <img src="https://xqimg.imedao.com/16223abc082299293fe913f6.png!custom660.jpg" alt="">
        </div>
        <p>
          金氪3月14日讯：3月14日新三板新增挂牌企业1家，终止挂牌企业1家，共挂牌企业11614家，其中集合竞价10305家，做市转让1309家。 新挂牌企业：中联汇通 终止挂牌企业：顶联信息 退出做市企业：迈奇化学 市场数据： 今日，新三板共有654只股票发生交易，总成金额逾3.77亿元，其中做市转让389只股，成交超1.49亿元；集合竞价265只股，成交近2.28亿元，总成交数量为7761.50万股。 指数方面，三板做市指数（899002）以934.23点开盘，整天小幅缓慢下跌，截止收盘报932.93点，跌幅为0.14%，成分股成交6370万元 作者：金氪投行之家 链接：https://xueqiu.com/5900650325/103158626 来源：雪球 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
        </p>
      </article>

    </div>
  </div>
</template>

<script>
import { get } from '../../utils/http'

import MainHeader from '../common/header'
export default {
  components: {
    MainHeader
  },
  data: function () {
    return {

    }
  },
  created: function () {
    get('/api/topic/1').then(data => {
      console.log(data)
    })
  },
  methods: {

  }
}
</script>

<style lang="scss" scoped>
.article_container {
  width: 60%;
  margin: 100px auto;
}

.article_author {
  display: flex;
  margin-bottom: 30px;
  .top_left {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
    img {
      width: 100%;
    }
  }
  .top_right {
    flex: 1;
    padding: 4px 0 0 8px;
    .avatar_name .name {
      color: #222;
      font-size: 14px;
      font-weight: bold;
    }
    .avatar_subtitle {
      color: #999;
      font-size: 14px;
      line-height: 24px;
      .time {
        color: #999;
        font-size: 14px;
      }
    }
  }
}

.article_bd {
  h1 {
    font-size: 24px;
    color: #222;
    font-family: "Microsoft Yahei";
    font-weight: bold;
    text-align: center;
  }
  .article_bd_from {
    margin: 16px 0;
    color: #666;
    font-size: 16px;
    text-align: center;
    line-height: 24px;
    a {
      color: #0066cc;
      font-size: 16px;
    }
  }
  p {
    font-size: 14px;
    text-indent: 2rem;
    line-height: 28px;
    padding: 0 5px;
  }
  .image {
    margin: 30px auto;
    width:600px;
    img {
      width: 100%;
    }
  }
}
</style>
