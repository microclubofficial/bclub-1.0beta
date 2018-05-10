<template>
  <div>
  <div class="personal-topiclist">
    <div class="loading" v-if='showLoader'>
      <img src='../../../assets/img/loading.png' alt='' class="icon-loading">
    </div>
    <!-- {{[articles]}} -->
    <div class="bibar-tabitem fade in active" :key="index" id="bibar-newstab1" v-for="(tmp,index) in articles">
      <div class="bibar-indexNewsList">
        <div class="bibar-indexNewsItem">
          <div class="speech" v-if="tmp.reply_user !== null"> <span>{{tmp.reply_user}}<span class="time">{{tmp.reply_time}}</span>前评论了讨论</span><i class="iconfont icon-dot"></i></div>
          <div class="user">
            <div class="bibar-author"> <a href="#"> <span class="photo"><img :src="tmp.avatar"></span> <span class="name">{{tmp.author}}</span> <span class="time">{{tmp.diff_time !== '0秒' ? tmp.diff_time + '前' : '刚刚发布'}}·来自币吧</span> </a> </div>
            <div class="bibar-list">
              <div class="tit"><a href="javascript:void(0)" @click="goDetail(tmp.id)">{{tmp.title}}</a></div>
          <div class="txt indexNewslimitHeight" @click="goDetail(tmp.id)">
            <div class="media">
            <div class="media-body">
              <div v-html="EditorContent(tmp.content)"></div>
            </div>
            <a class="pull-left" href="javascript:void(0)" v-if="tmp.picture">
              <img class="media-object" :src="tmp.picture">
            </a>
            </div>
          </div>
          <div class="set">
            <ul class="bibar-indexNewsItem-infro">
              <li class="set-choseOne"> <a href="javascript:void(0);" class="icon-quan mr15" :class='{active:tmp.is_good_bool}'  @click="changeNum(0,index,tmp.id,0,tmp)" ><i class="iconfont">&#xe603;</i><span class="is-good">{{tmp.is_good}}</span></a> <a href="javascript:void(0);" :class='{active:tmp.is_bad_bool}' class="icon-quan set-choseOne" @click="changeNum(1,index,tmp.id,0,tmp)"><i class="iconfont">&#xe731;</i><span class="is-bad">{{tmp.is_bad}}</span></a> </li>
              <li class="set-discuss" @click="showDiscuss(index,tmp.id)">
                <a href="javascript:void(0);">
                  <i class="iconfont icon-pinglun"></i> 评论
                  <span>{{tmp.replies_count}}</span>
                </a>
              </li>
              <li class="set-choseStar" @click="collectionTopic(index,tmp.id)"> <a :class="{collectionActive:index === collection}" href="javascript:void(0);"><i class="iconfont icon-star">&#xe6a7;</i>收藏</a> </li>
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
            <div class="bibar-hot" v-show="index===i">
       <!-- 评论框 -->
       <div class="editor-comment">
         <img :src="userInfo.avatar" alt="" class="avatar" v-show="commentShow">
         <div class="editor-bd">
           <span class="comment-img-delete"></span>
           <svg version='1.1' xmlns='http://www.w3.org/2000/svg' v-show="commentShow" class="editor-triangle">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
           </svg>
           <div class="editor-textarea" v-show="commentShow" @click="commentShowFun">
             <div class="editor-placeholder">评论...</div>
           </div>
           <div class="editor-toolbar">
              <BibarReport :toApi='toId' :mainCommnet='lid' v-show="showReport" @backList = 'showContent' ></BibarReport>
          </div>
         <span class="img-upload-delete">
             <img src="../../../assets/img/del.png" alt="">
        </span>
       </div>
       </div>
       <!-- 评论内容 -->
       <div class="comment-wrap">
          <div class="hook-comment"></div>
          <div class="comment-container">
            <div class="loading" v-if='showLoaderComment'>
              <img src="../../../assets/img/loading.png" alt="" class="icon-loading">
            </div>
            <div class="comment-all">
              <h3>全部评论({{tmp.replies_count}})</h3>
              <!-- <div class="comment-sort">
                <a href="#" class="active">最近</a>
                <a href="#">最早</a>
                <a href="#">赞</a>
              </div> -->
              <!-- 回复内容 -->
                  <!-- <div class="comment-item" data-index='' data-id='' v-for="(tmp,rIndex) in replyContent" :key='rIndex'>
                  <div>
                    <a href="#" data-tooltip='' class="avatar">
                      <img :src="tmp.avatar" alt="">
                    </a>
                    <div class="comment-item-main">
                      <div class="comment-item-hd">
                        <a href="#" class="user-name">{{tmp.author}}</a>
                        <span class="time allTalk-time">{{tmp.created_at}}</span>
                      </div>
                      <p class="replyAuthor">@<span>{{tmp.author}}:</span><span style="display:inline-block">{{talkComment[replayId].content | needContent()}}</span></p>
                      <p v-html="tmp.content">{{tmp.content}}</p>
                      <p></p>
                    </div>
                  </div>
                </div> -->
                <!-- 评论 -->
              <div class="comment-list">
                <div class="comment-item" data-index='' data-id=''  :key ='now' v-for="(item,now) in nowData">
                  <div>
                    <a href="#" data-tooltip='' class="avatar">
                      <img :src="item.avatar" alt="">
                    </a>
                    <div class="comment-item-main">
                      <div class="comment-item-hd">
                        <p href="#" class="user-name">{{item.author}}<span class="time">{{item.diff_time !== '0秒' ? item.diff_time + '前' : '刚刚'}}发布</span></p>
                      </div>
                      <!-- @ 样式 -->
                      <p class="replyAuthor" v-if="item.at_user !== ''">@{{item.at_user}}:&nbsp;<span class="replyBackConten" style="display:inline-block;font-weight: normal;" v-html="replyFun(item.reference)"></span></p>
                      <!-- <p>{{item}}</p> -->
                      <p v-html="item.content">{{item.content}}</p>
                    </div>
                    <div class="set">
                      <ul class="bibar-indexNewsItem-infro">
                        <li class="set-choseTwo"> <a href="javascript:void(0);" class="icon-quan mr15"  @click="changeNum(0,now,item.id,1,item)" :class='{active:item.is_good_bool}'><i class="iconfont">&#xe603;</i><span class="is-good-t">{{item.is_good}}</span></a><a href="javascript:void(0);"  :class='{active:item.is_bad_bool}' class="icon-quan set-choseTwo" @click="changeNum(1,now,item.id,1,item)"><i class="iconfont">&#xe731;</i><span class="is-bad-t">{{item.is_bad}}</span></a></li>
                        <!-- <li class="set-choseShang"> <a href="javascript:void(0);"><i class="iconfont icon-dashang"></i> 打赏<span>438</span></a> </li> -->
                        <li class="set-discuss" @click="replyComment(item.id,now)">
                          <a href="javascript:void(0);">
                            <i class="iconfont icon-pinglun"></i> 回复
                          </a>
                        </li>
                      </ul>
                    </div>
                     <!-- 回复 -->
        <div class="comment-reply"  v-show="now === replayId">
                <!-- 回复文本框 -->
        <div class="editor-comment">
         <img :src="userInfo.avatar" alt="" class="avatar" v-show="talkReplyTxt">
         <div class="editor-bd">
           <span class="comment-img-delete"></span>
           <svg version='1.1' xmlns='http://www.w3.org/2000/svg' v-show="talkReplyTxt" class="editor-triangle">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
           </svg>
           <div class="editor-textarea"  v-show="talkReplyTxt" @click="talkReplyEditor">
             <div class="editor-placeholder">回复...</div>
           </div>
           <div class="editor-toolbar">
              <BibarReport ref='childShowApi' :toApi='toRId' :replyAuthor='item.author' :replyContent='item.content' :mainReplay='tmp.id' v-show="showReportReplay" @backhotReplies = 'showReplyContent'></BibarReport>
          </div>
         <span class="img-upload-delete">
             <img src="../../../assets/img/del.png" alt="">
          </span>
       </div>
       </div>
       </div>
                  </div>
                </div>
              </div>
              <!-- 分页条 -->
            <div class="pages" v-if='showPage'>
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
          </div>
       </div>
       </div>
            </div>
          </div>
     <!-- <div class='backContent' :key ='now' v-for="(item,now) in nowData">{{item}}</div> -->
        </div>
      </div>
    </div>
    <div class="loading-bar" v-if='loadingShow'>
                  <!-- <svg class="icon icon-loading" aria-hidden="true">
                      <use xlink:href="#icon-loading"  style="fill:blue" ></use>
                  </svg>加载中... -->
                  <img v-show="listLoding" src="../../../assets/img/listLoding.png" alt="" class="icon-loading">
                  <img v-show="noLoading" src="../../../assets/img/noLoading.png" alt="" class="icon-loading">{{bottomText}}
                </div>
  </div>
  </div>
</template>

<script>
import {get, post} from '../../../utils/http'
import BibarReport from '../../homePage/bibarReport.vue'
import { Toast } from 'mint-ui'
export default{
  data: function () {
    return {
      articles: [],
      ishandbad: 0,
      isClick: 0,
      lid: '',
      i: '',
      showComment: false,
      showReport: false,
      nowData: [],
      commentShow: false,
      backFt: {
        'author': '',
        'avatar': '',
        'created_at': '',
        'updated_at': '',
        'title': '',
        'content': '',
        'is_good': 0,
        'is_bad': 0,
        replt_count: 0
      },
      toId: 0,
      toRId: 0,
      upId: 0,
      tpno: 1,
      pageCount: 0,
      bottomText: '加载中...',
      listLoding: true,
      noLoading: false,
      up: 0,
      loadingShow: false,
      talkReplayBox: false,
      replyContent: [],
      talkReplyTxt: false,
      replayId: '',
      showReportReplay: false,
      collection: 0,
      hasImg: false,
      hotreplyContent: [],
      isGood: 0,
      isBad: 0,
      // 分页
      replyId: 0,
      cpno: 1,
      cpageLimit: 10,
      cpageCount: 0,
      showPrevMore: false,
      showNextMore: false,
      showPage: false,
      // loading
      showLoader: false,
      showLoaderComment: false
    }
  },
  components: {
    BibarReport
  },
  created: function () {
    // 文章分页
    this.$store.dispatch('clear_backForNav')
    this.showLoader = true
    get(`/api/u/topic/${this.userInfo.username}/${this.tpno}`).then(data => {
      this.articles = data.data.topics
      this.showLoader = false
      this.pageCount = data.data.page_count
      if (this.articles.length > 0) {
        this.loadingShow = true
      }
      var that = this
      document.querySelector('#app').addEventListener('scroll', function () {
        if (this.clientHeight + this.scrollTop === this.scrollHeight) {
          that.loadTopicPage()
        }
      })
    })
  },
  mounted () {
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
  methods: {
    // 分页
    loadTopicPage () {
      if (this.tpno < this.pageCount) {
        setTimeout(() => {
          this.showLoader = true
          this.tpno++
          get(`/api/u/topic/${this.userInfo.username}/${this.tpno}`).then(data => {
            this.articles = this.articles.concat(data.data.topics)
            this.showLoader = false
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
    // 点赞吐槽
    changeNum (isNum, index, id, classId, item) {
      if (index !== this.up) {
        this.up = index
      }
      // 文章点赞吐槽
      if (classId === 0) {
        // 点赞
        if (isNum === 0) {
          get(`/api/topic/up/${id}`).then(data => {
            if (data.resultcode === 1) {
              // $('.bibar-tabitem:eq(' + index + ')').find('.set-choseOne>a:eq(' + isNum + ')').addClass('active')
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
          get(`/api/topic/down/${id}`).then(data => {
            if (data.resultcode === 1) {
              // $('.bibar-tabitem:eq(' + index + ')').find('.set-choseOne>a:eq(' + isNum + ')').addClass('active')
              item.is_good = data.data.is_good
              item.is_bad = data.data.is_bad
              item.is_bad_bool = data.data.is_bad_bool
              item.is_good_bool = data.data.is_good_bool
            } else if (data.message === '未登录') {
              alert(data.message)
              this.$router.push('/login')
            } else {
              alert(data.message)
            }
          })
        }
        // 评论点赞吐槽
      } else if (classId === 1) {
        // 点赞
        if (isNum === 0) {
          get(`/api/reply/up/${id}`).then(data => {
            console.log(data)
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
            console.log(data)
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
      }
    },
    // 去详情页
    goDetail (id) {
      this.lid = id
      this.$router.push(`/details/${this.lid}`)
    },
    // 评论
    showDiscuss (index, id) {
      this.replyId = id
      this.showLoaderComment = true
      get(`/api/topic/${id}/${this.cpno}`).then(data => {
        this.nowData = data.data.replies
        this.showLoaderComment = false
        this.cpageCount = data.data.page_count
        if (this.cpageCount > 1) {
          this.showPage = true
        } else {
          this.showPage = false
        }
        this.$nextTick(() => {
          $('.comment-item-main').find('img').addClass('zoom-in')
          $('[data-w-e]').removeClass('zoom-in')
          $('.comment-item-main').on('click', 'img', function () {
            // console.log($(this)).not('[data-w-e]')
            if (!$(this)[0].hasAttribute('data-w-e')) {
              if (!$(this).hasClass('zoom-out')) {
                if ($(this).hasClass('zoom-in')) {
                  $(this).removeClass('zoom-in')
                }
                $(this).addClass('zoom-out')
              } else if ($(this).hasClass('zoom-out')) {
                $(this).removeClass('zoom-out')
                $(this).addClass('zoom-in')
              }
            }
          })
        })
      })
      if (index !== this.i) {
        this.i = index
        this.lid = id
      } else {
        this.i = ''
      }
      this.replayId = ''
      this.toId = 0
      this.lid = id
      // this.showComment = !this.showComment
      this.commentShow = true
      if (this.commentShow) {
        this.showReport = false
      }
      $('.editor-toolbar').find('.wangeditor>.report').css({'bottom': '0'})
      $('.editor-toolbar').find('.wangeditor>.cancel').css({'bottom': '4px'})
      $('.editor-toolbar').find('.wangeditor>.editor').css({'min-height': '130px', 'padding-bottom': '37px'})
      $('.editor-toolbar').find('.wangeditor>div:eq(2)').css('display', 'none')
    },
    // 是否显示评论默认框
    commentShowFun () {
      this.showReport = true
      this.commentShow = false
      this.replayId = ''
    },
    // 评论富文本框
    showContent (data) {
      this.commentShow = true
      this.showReport = false
      // this.showLoaderComment = true
      this.nowData.unshift(data)
      this.articles[this.i].replies_count = data.replies_count
    },
    showFtContentFun (ftData) {
      this.articles = [ftData, ...this.articles]
    },
    // 评论回复
    replyComment (id, now) {
      if (now !== this.replayId) {
        this.replayId = now
      } else {
        this.replayId = ''
      }
      this.commentShow = true
      this.showReport = false
      if (!this.talkReplayBox) {
        this.talkReplayBox = true
        this.showReportReplay = true
      }
      // this.talkReplayBox = !this.talkReplayBox
      // this.talkReplyTxt = !this.talkReplyTxt
      this.toRId = 4
    },
    // 显示回复富文本框
    talkReplyEditor () {
      this.talkReplyTxt = !this.talkReplyTxt
      this.showReportReplay = !this.showReportReplay
    },
    // 回复返回数据
    showReplyContent (data) {
      this.nowData.unshift(data)
      // this.showLoaderComment = true
      this.articles[this.i].replies_count = data.replies_count
      this.replayId = ''
    },
    // 收藏
    collectionTopic (index, id) {
      let instance
      post(`/api/collect/${id}`).then(data => {
        if (data.message === 'success') {
          this.collection = index
          instance = new Toast({
            message: '收藏成功',
            iconClass: 'glyphicon glyphicon-ok',
            duration: 1000
          })
        } else {
          instance = new Toast({
            message: '取消收藏',
            duration: 1000
          })
        }
        setTimeout(() => {
          instance.close()
        }, 1000)
      })
    },
    // 处理图片
    EditorContent (val) {
      let now = `<div>${val}</div>`
      now = $(now).text()
      if (now.length > 128) {
        return now.substring(0, 128) + '...'
      }
      return now
    },
    replyFun (val) {
      let reply = val.replace(/<p>|<\/p>/g, '')
      if (/^\/static.*/ig.test(reply)) {
        return '图片评论' + `<a style='color:#0181FF' href='${reply}'><i class='iconfont'>&#xe694;</i>查看图片</a>`
      }
      return reply
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
      if (page === '···') {
        return
      }
      this.chartShow = 0
      this.summaryList = []
      if (this.cpno !== page) {
        this.cpno = page
      }
      get(`/api/topic/${this.replyId}/${page}`).then(data => {
        this.nowData = data.data.replies
      })
    }
  }
}
</script>

<style>
  .replyBackConten>p:first-child{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 500px;
    float: right;
}
/*回复样式*/
.replyAuthor{
    height: 50px;
    background: #F2F2F2;
    line-height: 50px !important;
    padding-left: 20px !important;
    font-weight: 700;
    margin-right: 2px;
}
.glyphicon{
  font-size: 20px;
}
.collectionActive{
  color: #ffa727 !important;
}
.personal-topiclist{
  position: relative;
  padding: 20px;
}
.indexNewslimitHeight{
  cursor: pointer;
}
.bibar-tabitem{overflow: hidden;}
.bibar-comment{
    position: relative;
    margin-left: 58px;
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
.editor-textarea .comment-placeholder {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    padding: 5px 10px;
    color: #d4d7dc;
}
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
.comment-wrap{
    margin-bottom: 5px;
}
.comment-container{
    padding: 0 8px;
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
    width: 32px;
    height: 32px;
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
.comment-item-main img{
    display: block;
    cursor: zoom-in;
    max-width: 200px;
}
.bibar-indexNewsItem-infro>li{
    float: left;
    /*margin-right: 25px;*/
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
.bibar-tabitem{
  overflow: hidden;
}
.bibar-indexNewsList{
    float: left;
    /* width: 860px; */
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
/*.avatar{margin-bottom: 15px;}*/
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
   padding: 15px 10px 15px 0;
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
.editor-textarea .comment-placeholder {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    padding: 5px 10px;
    color: #d4d7dc;
}
</style>
