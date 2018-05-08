<template>
  <div class="comment-item">
    <main-header></main-header>
    <div class="article_container">
      <div class="article_author">
        <div class="top_left">
          <a href="javascript:void(0)" class="avatar"><img :src='articleDetail.avatar'></a>
        </div>
        <div class="top_right">
          <div class="avatar_name">
            <a href="javascript:void(0)" class="name">{{articleDetail.author}}</a>
          </div>
          <div class="avatar_subtitle">
            <span class="source">来自币吧</span>
            <a href="" target="_blank" class="time">&ensp;发布于{{articleDetail.diff_time}}</a>
          </div>
        </div>
      </div>
      <article class="article_bd">
        <h1 class="article_bd_title">{{articleDetail.title}}</h1>
        <!--<div class="article_bd_from">来自
          <a href="">金氪投行之家的雪球原创专栏</a>
        </div>-->
        <p class="detail-main-content" v-html="articleDetail.content">
          <strong>{{articleDetail.diff_time}}:</strong>{{articleDetail.content}}
        </p>
        <div class="image">
          <!-- <img src="https://xqimg.imedao.com/16223abc082299293fe913f6.png!custom660.jpg" alt=""> -->
        </div>
      </article>
      <div class="meta-container">
        <!-- <a href="#" class="reward-btn">赞</a> -->
        <!--分享-->
        <!--<div class="meta-share">
        <a href="#" class="btn-share-wechat">
          <span><img src="../../assets/img/weixin.png" alt=""></span>
        </a>
        <a href="#" class="btn-share-weibo">
          <span><img src="../../assets/img/weibo.png" alt=""></span>
        </a>
      </div>-->
      <div class="meta-handle">
        <div class="set">
            <ul class="bibar-indexNewsItem-infro">
              <li class="set-choseOne"> <a href="javascript:void(0);" class="icon-quan mr15" :class='{active:articleDetail.is_good_bool}'  @click="changeNumAriticle(0,articleDetail)" ><i class="iconfont">&#xe603;</i><span class="is-good">{{articleDetail.is_good}}</span></a> <a href="javascript:void(0);" :class='{active:articleDetail.is_bad_bool}' class="icon-quan set-choseOne" @click="changeNumAriticle(1,articleDetail)"><i class="iconfont">&#xe731;</i><span class="is-bad">{{articleDetail.is_bad}}</span></a> </li>
              <li class="set-choseStar" @click="collectionTopic(articleDetail)"> <a href="javascript:void(0)" class="btn-article-retweet" :class='{collectionActive:articleDetail.collect_bool}'>
          <i class="iconfont icon-star">&#xe6a7;</i>收藏
        </a> </li>
              <!-- <li> <a href="javascript:void(0);"><i class="iconfont icon-fenxiang"></i> 分享</a> </li> -->
              <!-- <li class="set-choseShang"> <a href="javascript:void(0);"><i class="iconfont icon-dashang"></i> 打赏<span>438</span></a> </li> -->
              <li>
                <!-- <div class="dropdown">
                  <a href="javascript:void(0);" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="iconfont icon-genduo"></i> 更多</a>
                  <ul class="dropdown-menu">
                    <li><a href="javascript:void(0);">举报</a></li>
                    <li><a href="javascript:void(0);">没有帮助</a></li>
                  </ul>
                </div> -->
              </li>
            </ul>
          </div>
      </div>
      <div class="meta-info">
        <!--<span>{{repliesCcount}}</span>评论-->
        <!--<span>{{repliesCcount}}</span>评论 · <span>{{articleDetail.is_good}}</span>赞-->
        <!--<a href="#" class="btn-report-spam">举报</a>-->
      </div>
      </div>
      <div class="detail-editor-toolbar">
        <BibarReport :toApi='5' :detailId='articleDetail.id' @backList = 'showDetailContent'></BibarReport>
      </div>
      <!-- 评论内容 -->
       <div class="comment-wrap">
          <div class="hook-comment"></div>
          <div class="comment-container">
            <div class="loading">
              <img src="../../assets/img/loading.png" alt="">
            </div>
            <div class="comment-all">
              <h3>全部评论({{repliesCcount}})</h3>
              <!-- <div class="comment-sort">
                <a href="#" class="active">最近</a>
                <a href="#">最早</a>
                <a href="#">赞</a>
              </div> -->
                <div class="comment-list">
                  <!-- <pull-to> -->
                  <div class="comment-item" data-index='' data-id=''  :key ='now' v-for="(item,now) in nowData">
                  <div>
                    <a href="#" data-tooltip='' class="avatar">
                      <img :src="item.avatar" alt="">
                    </a>
                    <div class="comment-item-main">
                      <div class="comment-item-hd">
                        <a href="#" class="user-name">{{item.author}}</a>
                        <span class="time">{{item.diff_time}}前发布</span>
                      </div>
                      <!-- @ 样式 -->
                      <p class="replyAuthor" v-if="item.reference !== ''">@<span>{{item.at_user}}:</span><span style="display:inline-block;font-weight: normal;" v-html='needTxt(item.reference)'></span></p>
                      <!-- <p>{{item}}</p> -->
                      <!-- <p>{{item}}</p> -->
                      <p v-html="item.content">{{item.content}}</p>
                    </div>
                    <div class="set">
                      <ul class="bibar-indexNewsItem-infro">
                        <li class="set-choseOne"> <a href="javascript:void(0);" class="icon-quan mr15" :class='{active:item.is_good_bool}'  @click="changeNum(0,now,item.id,item)"><i class="iconfont">&#xe603;</i><span class="is-good">{{item.is_good}}</span></a><a href="javascript:void(0);" :class='{active:item.is_bad_bool}' class="icon-quan" @click="changeNum(1,now,item.id,item)"><i class="iconfont">&#xe731;</i><span class="is-bad">{{item.is_bad}}</span></a> </li>
                        <li class="set-discuss" @click="replyComment(item.id,now)">
                          <a href="javascript:void(0);">
                            <i class="iconfont icon-pinglun"></i> 回复
                          </a>
                        </li>
                      </ul>
                    </div>
                    <!-- 回复 -->
        <div class="comment-reply" v-show="talkReplayBox && now === replayId && !changeIndex">
                <!-- 回复文本框 -->
        <div class="editor-comment">
         <img :src="userInfo.avatar" alt="" class="avatar" v-show="talkReplyTxt">
         <div class="editor-bd">
           <span class="comment-img-delete"></span>
           <svg version='1.1' xmlns='http://www.w3.org/2000/svg' class="editor-triangle">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
           </svg>
           <div class="editor-textarea"  v-show="talkReplyTxt" @click="talkReplyEditor">
             <div class="editor-placeholder">回复...</div>
           </div>
           <div class="editor-toolbar">
              <BibarReport ref='childShowApi' :toApi='toRId' :replyAuthor='item.author' :replyContent='item.content' @backhotReplies = 'showReplyContent' :mainReplay='articleDetail.id' v-show="showReportReplay"></BibarReport>
          </div>
         <span class="img-upload-delete">
             <img src="../../assets/img/del.png" alt="">
          </span>
       </div>
       </div>
       </div>
                  </div>
                </div>
                <div class="loading-bar" v-if='loadingShow'>
                  <!-- <svg class="icon icon-loading" aria-hidden="true">
                      <use xlink:href="#icon-loading"  style="fill:blue" ></use>
                  </svg>加载中... -->
                  <img v-show="listLoding" src="../../assets/img/listLoding.png" alt="" class="icon-loading">
                  <img v-show="noLoading" src="../../assets/img/noLoading.png" alt="" class="icon-loading">{{bottomText}}
                </div>
              <!-- </pull-to> -->
              </div>
            </div>
          </div>
       </div>
    </div>
  </div>
</template>

<script>
import { get, post } from '../../utils/http'
import MainHeader from '../common/header'
import BibarReport from '../homePage/bibarReport.vue'
import { Toast } from 'mint-ui'
// import PullTo from 'vue-pull-to'

export default {
  components: {
    MainHeader,
    BibarReport
    // PullTo
  },
  data: function () {
    return {
      nowData: [],
      did: null,
      isGood: 0,
      ishandbad: 0,
      backDetail: {
        'content': ''
      },
      articleDetail: [],
      nowObj: [],
      toId: 0,
      pageCount: 0,
      pno: 1,
      bottomText: '加载中...',
      listLoding: true,
      noLoading: false,
      loadingShow: true,
      talkReplayBox: false,
      talkReplyTxt: false,
      showReportReplay: false,
      toRId: 0,
      replayId: 0,
      repliesCcount: 0,
      showCollection: false,
      // 发评论
      changeIndex: false
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  mounted () {
    this.did = this.$route.params.id
    // console.log(this.pageCount)
    get(`api/topic/${this.did}/${this.pno}`).then(data => {
      this.articleDetail = data.data.topic
      this.repliesCcount = data.data.replies_count
      this.nowData = data.data.replies
      if (this.nowData.length === 0) {
        this.loadingShow = false
      }
      this.pageCount = data.data.page_count
      var that = this
      document.querySelector('#app').addEventListener('scroll', function () {
        if (this.scrollHeight - this.scrollTop === this.clientHeight) {
          that.loadDetailPage()
        }
      })
    })
    $('.editor').css({'padding-bottom': '35px'})
    $('.editor-toolbar').find('.report ').css({'right': '260px', 'bottom': '2px'})
    $('.editor-toolbar').find('.cancel ').css({'right': '315px', 'bottom': '6px'})
    $('.article_bd').find('img').css({'display': 'block', 'text-align': 'center', 'margin': '10px auto'})
    $('.detail-editor-toolbar').find('.editor').css({'padding-bottom': '45px'})
  },
  methods: {
    loadDetailPage () {
      // console.log(this.pno < this.pageCount)
      if (this.pno < this.pageCount) {
        setTimeout(() => {
          get(`api/topic/${this.did}/${this.pno}`).then(data => {
            this.nowData = this.nowData.concat(data.data.replies)
            this.pno++
            this.bottomText = '加载中...'
            // this.loadingImg = '../../assets/img/listLoding.png'
          })
        }, 1000)
      } else {
        this.bottomText = '没有啦'
        this.listLoding = false
        this.noLoading = true
        // this.loadingImg = '../../assets/img/noLoading.png'
        return false
      }
    },
    // 正文点赞吐槽
    changeNumAriticle (isNum, articleDetail) {
      if (isNum === 0) {
        get(`/api/topic/up/${articleDetail.id}`).then(data => {
          if (data.resultcode === 1) {
            // $('.comment-item:eq(' + index + ')').find('.set-choseTwo>a:eq(' + isNum + ')').addClass('active')
            articleDetail.is_good = data.data.is_good
            articleDetail.is_bad = data.data.is_bad
            articleDetail.is_bad_bool = data.data.is_bad_bool
            articleDetail.is_good_bool = data.data.is_good_bool
          } else if (data.message === '未登录') {
            this.$router.push('/login')
          } else {
            alert(data.message)
          }
        })
      } else if (isNum === 1) {
        get(`/api/topic/down/${articleDetail.id}`).then(data => {
          if (data.resultcode === 1) {
            // $('.comment-item:eq(' + index + ')').find('.set-choseTwo>a:eq(' + isNum + ')').addClass('active')
            articleDetail.is_good = data.data.is_good
            articleDetail.is_bad = data.data.is_bad
            articleDetail.is_bad_bool = data.data.is_bad_bool
            articleDetail.is_good_bool = data.data.is_good_bool
          } else if (data.message === '未登录') {
            this.$router.push('/login')
          } else {
            alert(data.message)
          }
        })
      }
    },
    // 点赞吐槽
    changeNum (isNum, index, id, item) {
      if (index !== this.up) {
        this.up = index
      }
      // 点赞
      if (isNum === 0) {
        get(`/api/reply/up/${id}`).then(data => {
          if (data.resultcode === 1) {
            // $('.comment-item:eq(' + index + ')').find('.set-choseTwo>a:eq(' + isNum + ')').addClass('active')
            item.is_good = data.data.is_good
            item.is_bad = data.data.is_bad
            item.is_bad_bool = data.data.is_bad_bool
            item.is_good_bool = data.data.is_good_bool
          } else if (data.message === '未登录') {
            this.$router.push('/login')
          } else {
            alert(data.message)
          }
        })
        // 吐槽
      } else if (isNum === 1) {
        get(`/api/reply/down/${id}`).then(data => {
          if (data.resultcode === 1) {
            // $('.comment-item:eq(' + index + ')').find('.set-choseTwo>a:eq(' + isNum + ')').addClass('active')
            item.is_good = data.data.is_good
            item.is_bad = data.data.is_bad
            item.is_bad_bool = data.data.is_bad_bool
            item.is_good_bool = data.data.is_good_bool
          } else if (data.message === '未登录') {
            this.$router.push('/login')
          } else {
            alert(data.message)
          }
        })
      }
    },
    showDetailContent (data) {
      this.changeIndex = true
      this.nowData.unshift(data)
      get(`api/topic/${this.did}/${this.pno}`).then(data => {
        console.log(data)
        this.repliesCcount = data.data.replies_count
      })
    },
    // 评论回复
    replyComment (id, now) {
      this.changeIndex = false
      if (now !== this.replayId) {
        this.replayId = now
      }
      this.showReport = false
      if (!this.talkReplayBox) {
        this.talkReplayBox = true
        this.showReportReplay = true
      }
      this.toRId = 4
    },
    // 显示回复富文本框
    talkReplyEditor () {
      this.talkReplyTxt = !this.talkReplyTxt
      this.showReportReplay = !this.showReportReplay
    },
    // 回复返回数据
    showReplyContent (data) {
      this.talkReplayBox = false
      this.nowData.unshift(data)
      this.talkReplayBox = false
      this.showReportReplay = false
      get(`api/topic/${this.did}/${this.pno}`).then(data => {
        this.repliesCcount = data.data.replies_count
      })
    },
    // 回复人文字处理
    needTxt (val) {
      if (val) {
        let newTxt = val.slice(3, val.indexOf('</p>'))
        if (newTxt.indexOf('img') > 0) {
          newTxt = newTxt.substring(0, 300) + '...'
        } else if (newTxt.length > 20) {
          newTxt = newTxt.substring(0, 20) + '...'
        }
        return newTxt
      }
    },
    // 收藏
    collectionTopic (articleDetail) {
      let instance
      post(`/api/collect/${articleDetail.id}`).then(data => {
        if (data.data.collect_bool) {
          articleDetail.collect_bool = data.data.collect_bool
          instance = new Toast({
            message: data.message,
            iconClass: 'glyphicon glyphicon-ok',
            duration: 1000
          })
        } else {
          articleDetail.collect_bool = data.data.collect_bool
          instance = new Toast({
            message: data.message,
            duration: 1000
          })
        }
        setTimeout(() => {
          instance.close()
        }, 1000)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .detail-editor-toolbar{text-align: center;}
  .detail-editor-toolbar>.wangeditor>.report{padding: 0;}
  /*回复样式*/
.replyAuthor{
    height: 50px;
    background: #F2F2F2;
    line-height: 50px !important;
    padding-left: 20px !important;
    font-weight: 700;
    margin-right: 2px;
}
.detail-editor-toolbar>.wangeditor{
    width: 697px;
    margin: 0 auto;
}
/*.editor-toolbar>.wangeditor{
  padding-left: 18%;
}*/
.reward-btn{
    display: block;
    width: 56px;
    height: 56px;
    border-radius: 28px;
    background: #f70;
    color: #fff;
    line-height: 56px;
    margin: auto;
    text-align: center;
    margin: 20px auto;
}
.meta-container {
    margin: 0 auto 20px;
    z-index: 10;
    font-size: 13px;
    overflow: hidden;
}
.meta-share {
    float: right;
    padding-left: 10px;
    margin-left: 10px;
    position: relative;
}
.meta-share:before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 1px;
    height: 14px;
    margin: auto;
    background-color: #dadee5;
}
.meta-share a {
    margin: 0 6px;
    line-height: 1;
}
.meta-share a span img{
  width: 24px;
  height: 24px;
}
.btn-share-wechat {
    color: rgba(0,153,51,.8);
}
.meta-handle {
    float: left;
}
.meta-handle>a {
    color: #666c72;
    margin: 0 5px;
    line-height: 1.2;
}
.meta-handle>a>span>img{width: 20px; height: 20px;margin-bottom: 1px; margin-right: 5px;}
.meta-info {
    color: #666c72;
    line-height: 1.5;
}
.meta-info {
    color: #666c72;
    line-height: 1.5;
}
.meta-info .btn-report-spam {
    position: relative;
    display: inline-block;
    padding-left: 8px;
    margin-left: 15px;
    opacity: .5;
}
.meta-info .btn-report-spam:before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 1px;
    height: 14px;
    margin: auto;
    background-color: #dadee5;
}
.article_container {
    width: 1100px;
    /* margin: 80px auto 20px auto; */
    background: #fff;
    margin: auto;
    padding: 20px 35px;
    margin-top: 60px;
}

.article_author {
  display: flex;
  margin-bottom: 30px;
}
.article_author .top_left {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    overflow: hidden;
  }
.article_author .top_left img {
    width: 100%;
}
.article_author .top_right{
    flex: 1;
    padding: 4px 0 0 8px;
}
.article_author .top_right .avatar_name .name {
    color: #222;
    font-size: 14px;
    font-weight: bold;
  }
.avatar_subtitle {
    color: #999;
    font-size: 14px;
    line-height: 24px;
  }
.avatar_subtitle .time {
    color: #999;
    font-size: 14px;
}
.article_bd  h1 {
    font-size: 24px;
    color: #222;
    font-family: "Microsoft Yahei";
    font-weight: bold;
    text-align: center;
    margin: 20px 0;
  }
.article_bd .article_bd_from {
    margin: 16px 0;
    color: #666;
    font-size: 16px;
    text-align: center;
    line-height: 24px;
  }
.article_bd .article_bd_from a {
    color: #0066cc;
    font-size: 16px;
  }
.article_bd p {
    font-size: 14px;
    text-indent: 2rem;
    line-height: 28px;
    padding: 0 5px;
  }
.article_bd .image {
    margin: 30px auto;
    width:600px;
  }
.article_bd img {
    width: 100%;
}
.comment-wrap{
    margin-bottom: 5px;
}
.comment-container{
    padding: 0 8px;
}
.loading{
    margin-top: 60px;
    display: none;
}
.comment-all{
  position: relative;
}
.comment-all>h3 {
    margin: 15px 0 10px;
    font-size: 15px;
}
.comment-sort {
    position: absolute;
    top: 0;
    right: 0;
    text-align: right;
    /* margin-right: 5px; */
}
.comment-sort a.active {
    color: #06c;
}
.comment-sort a {
    position: relative;
    display: inline-block;
    margin-right: 26px;
    color: #909499;
    line-height: 1;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    font-size: 13px;
}
.comment-sort a:after {
    content: '';
    position: absolute;
    right: -13px;
    top: 2px;
    width: 1px;
    height: 14px;
    background-color: #edf0f5;
}
.comment-list{
    border-bottom: 0;
}
.comment-item{
    padding: 15px 0 10px;
    border-top: 1px solid #edf0f5;
    margin: 15px 0;
}
.comment-item .avatar {
    float: left;
    width: 48px;
    height: 48px;
}
a.avatar {
    display: inline-block;
    overflow: hidden;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    line-height: 1;
}
a.avatar img {
    width: 100%;
    height: 100%;
    vertical-align: middle;
}
.comment-item-main{
    margin-left: 42px;
}
.comment-item-hd{
    margin-bottom: 4px;
}
.comment-item-hd .user-name {
    font-size: 15px;
    font-weight: 700;
    margin-right: 0;
}
.comment-item-hd .time {
    float: right;
    font-size: 12px;
    color: #909499;
}
.comment-item-main>p {
    font-size: 15px;
    line-height: 1.6;
    word-break: break-all;
    overflow: hidden;
    margin: 10px 0;
}
.bibar-indexNewsItem-infro>li{
    float: left;
    margin-right: 25px;
}
.bibar-indexNewsItem-infro>li i {
    margin-right: 3px;
}
.loading-bar{text-align: center;}
.icon-loading {
    transform: rotate(0deg);
    animation-name: loading;
    animation-duration: 3s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
    width: 28px;
    height: 28px;
    margin-right: 20px;
  }
  @keyframes loading
  {
    from {transform: rotate(0deg);}
    to {transform: rotate(360deg);}
  }

   /*回复*/
.comment-reply{
  border-top: 1px solid #edf0f5;
  margin-top: 50px;
}
.comment-reply>.comment-item{
  margin: 15px 0;
}
.comment-reply>.editor-comment{
  margin-top: 15px;
}
.talkCommentEditor>.wangeditor>.editor{
  padding-bottom: 30px;
}
.talkCommentEditor .report{
  right: 317px !important;
}
.talkCommentEditor .cancel{
  right: 375px !important;
}
.talkBibar{
  width: 100%;
  position: relative;
}
.talkBibar-main{
  width: 1100px;
  margin: 80px auto 20px auto;
  position: relative;
}
.talkBibar-article{
  background: #fff;
  padding: 20px 25px;
}
.bibar-indexNewsItem .set>ul>.set-question{
   padding: 6px 10px;
   text-align: center;
   background: #1E8FFF;
   border-radius: 3px;
}
.bibar-indexNewsItem .set>ul>.set-question>a{color: #fff;}
.bibar-indexNewsItem .set>ul>.set-answer{
  padding: 5px 10px;
  border: 1px solid #1E8FFF;
  border-radius: 3px;
}
.bibar-indexNewsItem .set>ul>.set-answer>a{color: #1E8FFF;}
.comment-item{
  overflow: hidden;
}
.bibar-indexNewsList{
    float: left;
}
.talkBibar-flow{
    float: right;
    padding: 15px 0px 10px;
    margin: 10px 0;
}
.talkBibar-flow>.visitors{
  padding-left: 20px;
  border-left: 1px solid #D8D8D8;
}
.talkBibar-flow>.visitors>p:first-child{margin-bottom: 15px;}
.talkBibar-flow>.visitors>p{
  color: #80A2C6;
  font-size: 14px;
}
.talkBibar-flow>.visitors>p>span{
  color: #000;
  font-weight: bold;
  margin-left: 15px;
}
.talkSection{
  margin-top: 30px;
}
.talkSection>span{
  border:1px solid #1E8FFF;
  color: #1E8FFF;
  border-radius: 33%;
  padding: 5px 15px;
  margin: 10px 15px;
}
.talkBibar-editor{
  padding: 30px;
  background: #fff;
  position: relative;
}
.avatar{margin-bottom: 15px;}
.avatar>span{
  font-size: 16px;
  margin-left: 15px;
}
.avatar>.anonymous-users{
  float: right;
  font-size: 14px;
  color: #87A7C9;
}
.talkBibar-editor>button{
  position: absolute;
  z-index: 1;
}
.talkBibar-editor>.editor>.w-e-toolbar{
    background: snow !important;
    border-top: 1px solid rgb(216, 216, 216) !important;
    border-right: none !important;
    border-bottom: 1px solid rgb(216, 216, 216) !important;
    border-left: none !important;
    position: inherit !important;
}
.talkBibar-editor>.editor>.w-e-toolbar .w-e-menu{padding: 7px 10px;}
.talkBibar-editor>.set{right: 135px;}
.talkBibar-editor>.report{right: 50px; bottom: 10px;}
.w-e-text::-webkit-scrollbar{
  background:snow;
}
.w-e-text-container .w-e-panel-container{
  margin-left: 0 !important;
  left: 10% !important;
}
.talkBibar-editor .w-e-text-container{
  min-height: 150px !important;
  border:none !important;
}
.talkLeft{
    margin-top: 20px;
    width: 860px;
    position: relative;
    overflow: hidden;
    float: left;
}
.bibar-comment{
    width: 100%;
    overflow: hidden;
    float: left;
    margin-left: 0 !important;
}
.editor-comment{
    margin-top: 5px;
    background-color: #f8f8f8;
    /* padding: 20px; */
    padding-left: 10px;
}
.editor-comment>.avatar{
    width: 32px;
    height: 32px;
    float: left;
}
img.avatar{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    vertical-align: middle;
}
.editor-bd{
    margin-left: 42px;
    position: relative;
    z-index: 1;
}
svg:not(:root) {
    overflow: hidden;
}
.editor-triangle{
    position: absolute;
    top: 10px;
    left: -4px;
    width: 5px;
    height: 10px;
    z-index: 11;
}
.editor-triangle>.arrow{
    stroke: #edf0f5;
    fill: #f9fcfe;
}
.editor-textarea{
    position: relative;
    z-index: 10;
    min-height: 32px;
    border: 1px solid #edf0f5;
    font-size: 13px;
    line-height: 1.6;
    background-color: #fff;
}
.editor-textarea>div{
    line-height: 32px;
    margin-left: 10px;
}
.editor-textarea .comment-placeholder {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    padding: 5px 10px;
    color: #d4d7dc;
}
.media-left, .media>.pull-left {
    padding-right: 10px;
    width: 15%;
    overflow: hidden;
    /* height: 50px; */
    /* position: relative; */
    height: 100px;
}
.pull-left > img{width: 100%; height: 100%;}
.img-upload-delete{
    display: none;
    position: absolute;
    top: 0;
    right: 0;
    width: 24px;
    height: 24px;
    text-align: center;
    color: #fff;
    line-height: 24px;
    /* background-color: rgba(0,0,0,.7); */
    cursor: pointer;
    z-index: 10;
}
.img-upload-delete>img{
    width: 24px;
    height: 24px;
}
</style>
