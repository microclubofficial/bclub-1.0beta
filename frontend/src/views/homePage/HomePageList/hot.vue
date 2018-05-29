<template>
  <div>
  <div class="bibar-tabAll">
    <!-- {{[articles]}} -->
    <div class="loading" v-if='showLoader'>
      <img src="../../../assets/img/loading.png" alt="" class="icon-loading">
    </div>
    <div class="bibar-tabitem fade in active" :key="index" id="bibar-newstab1" v-for="(tmp,index) in articles">
      <div class="bibar-indexNewsList">
        <div class="bibar-indexNewsItem">
          <div class="speech" v-if="tmp.reply_user !== null"> <span><span class="time">{{tmp.reply_time}}</span>{{$t('list.ago')}} {{tmp.reply_user}} {{$t('list.commented')}}</span><i class="iconfont icon-dot"></i></div>
          <div class="user">
            <!--<img :src="tmp.avatar">-->
            <div class="bibar-author"> <a href="javascript:void(0)"> <span class="photo"><img :src="tmp.avatar"></span> <span class="name">{{tmp.author}}</span> <span class="time" @click='toBibar(tmp)'>{{tmp.diff_time !== 0 ? tmp.diff_time + $t('list.ago') : $t('list.justNow')}} - {{$t('list.from')}}{{tmp.token !== null ? (language === 'zh' ? tmp.zh_token : tmp.en_token) : $t('list.bclub')}}</span> </a> </div>
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
              <li class="set-discuss">
                <a href="javascript:void(0);" @click="showDiscuss(index,tmp.id,0)">
                  <i class="iconfont icon-pinglun"></i> {{$t('list.comment')}}
                  <span>{{tmp.replies_count}}</span>
                </a>
              </li>
              <li class="set-choseStar" @click="collectionTopic(tmp)"> <a :class='{collectionActive:tmp.collect_bool}' href="javascript:void(0);"><i class="iconfont icon-star">&#xe6a7;</i>{{$t('list.collect')}}</a> </li>
              <li v-if='tmp.bool_delete' class="set-delList" @click="delTopic(tmp, index)"> <a href="javascript:void(0);"><i class="iconfont icon-del">&#xe78d;</i>{{$t('list.delete')}}</a> </li>
              <!-- <li> <a href="javascript:void(0);"><i class="iconfont icon-fenxiang"></i> 分享</a> </li> -->
              <!-- <li class="set-choseShang"> <a href="javascript:void(0);"><i class="iconfont icon-dashang"></i> 打赏<span>438</span></a> </li> -->
              <!--<li>-->
                <!-- <div class="dropdown">
                  <a href="javascript:void(0);" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="iconfont icon-genduo"></i> 更多</a>
                  <ul class="dropdown-menu">
                    <li><a href="javascript:void(0);">举报</a></li>
                    <li><a href="javascript:void(0);">没有帮助</a></li>
                  </ul>
                </div> -->
              <!--</li>-->
            </ul>
          </div>
            <div class="bibar-hot" style="display:none;">
       <!-- 评论框 -->
       <div class="editor-comment clearfloat">
         <img :src="userInfo.avatar" alt="" class="avatar" v-show="commentShow">
         <div class="avatar" v-show="showReport"><img :src="userInfo.avatar" alt=""></div>
         <!--默认-->
           <!--<svg v-show="commentShow" version='1.1' xmlns='http://www.w3.org/2000/svg' class="editor-triangle editor-hot-comment-default">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
           </svg>-->
           <!--富文本-->
           <!--<svg style="left:56px; top:62px;" version='1.1' xmlns='http://www.w3.org/2000/svg' v-show="showReport" class="editor-svg">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
          </svg>-->
         <div class="editor-bd clearfloat">
           <span class="comment-img-delete"></span>
           <div class="editor-textarea" v-show="commentShow" @click="commentShowFun">
             <div class="editor-placeholder">{{$t('list.comment')}}...</div>
           </div>
           <div class="editor-toolbar clearfloat">
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
            <div class="comment-all">
              <h3>{{$t('list.allComments')}}({{tmp.replies_count}})</h3>
               <div class="comment-sort">
                <a href="javascript:void(0)" @click='sortList(tmp.id,0)' :class="{active:sortNow === 0}">{{$t('list.newest')}}</a>
                <a href="javascript:void(0)" @click='sortList(tmp.id,1)' :class="{active:sortNow === 1}">{{$t('list.earliest')}}</a>
                <a href="javascript:void(0)" @click='sortList(tmp.id,2)' :class="{active:sortNow === 2}">{{$t('list.likeMost')}}</a>
              </div>
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
                <div class="loading" v-if='showLoaderComment'>
                  <img src="../../../assets/img/loading.png" alt="" class="icon-loading">
                </div>
              <div class="comment-list">
                <div class="comment-item" data-index='' data-id='' :key ='now' v-for="(item,now) in nowData[tmp.id]">
                  <div>
                    <a href="#" data-tooltip='' class="avatar">
                      <img :src="item.avatar" alt="">
                    </a>
                    <div class="comment-item-main">
                      <div class="comment-item-hd">
                        <p href="#" class="user-name">{{item.author}}<span class="time">{{item.diff_time !== 0 ? item.diff_time + $t('list.ago') : $t('list.justNow')}}</span></p>
                      </div>
                      <!-- @ 样式 -->
                      <div class="replyAuthor" v-if="item.at_user !== ''">@{{item.at_user}}:&nbsp;<span class="replyBackConten" style="font-weight: normal;" v-html="replyFun(item.reference)"></span></div>
                      <!-- <p>{{item}}</p> -->
                      <!--评论文-->
                      <p class="commentContent" v-html="commentContent(item.content,item.id)"></p>
                      <a style="font-size:16px; white-space:nowrap;" v-if='item.content !== undefined && item.content.length - imgCommentLength[item.id]  > 200' href="#" class="bibar-indexintromore text-theme" @click="changeMore(item.id)">{{item.id === moreId ? $t('button.fold') : $t('button.unfold')}}<i style="font-size:16px;" class="iconfont" v-if="more === $t('button.unfold')">&#xe692;</i><i style="font-size:16px;" class="iconfont" v-if="more === $t('button.fold')">&#xe693;</i></a>
                    </div>
                    <div class="set" style="margin-left:42px">
                      <ul class="bibar-indexNewsItem-infro">
                        <li class="set-choseTwo"> <a href="javascript:void(0);" class="icon-quan mr15"  @click="changeNum(0,now,item.id,1,item)" :class='{active:item.is_good_bool}'><i class="iconfont">&#xe603;</i><span class="is-good-t">{{item.is_good}}</span></a><a href="javascript:void(0);"  :class='{active:item.is_bad_bool}' class="icon-quan set-choseTwo" @click="changeNum(1,now,item.id,1,item)"><i class="iconfont">&#xe731;</i><span class="is-bad-t">{{item.is_bad}}</span></a></li>
                        <!-- <li class="set-choseShang"> <a href="javascript:void(0);"><i class="iconfont icon-dashang"></i> 打赏<span>438</span></a> </li> -->
                        <li class="set-discuss" @click="replyComment(item.id,now)">
                          <a href="javascript:void(0);">
                            <i class="iconfont icon-pinglun"></i> {{$t('list.reply')}}
                          </a>
                        </li>
                        <li v-if='item.bool_delete' @click='delComment(item,now,tmp)' class="set-delList"> <a href="javascript:void(0);"><i class="iconfont icon-del">&#xe78d;</i>{{$t('list.delete')}}</a> </li>
                      </ul>
                    </div>
                     <!-- 回复 -->
        <div class="comment-reply" v-show="now===replayId">
                <!-- 回复文本框 -->
        <div class="editor-comment clearfloat">
         <div class="avatar" style="margin-top:8px;" v-show="showReportReplay"><img :src="userInfo.avatar" alt=""></div>
         <!--富文本-->
           <!--<svg style="left:56px; top: 62px;" version='1.1' xmlns='http://www.w3.org/2000/svg' v-show="showReportReplay" class="editor-svg">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
          </svg>-->
         <div class="editor-bd clearfloat">
           <span class="comment-img-delete"></span>
           <div class="editor-textarea"  v-show="talkReplyTxt" @click="talkReplyEditor">
             <div class="editor-placeholder">{{$t('list.reply')}}...</div>
           </div>
           <div class="editor-toolbar clearfloat">
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
            <div class="pages" v-if='cpageCountObj[tmp.id] > 1'>
              <ul class="mo-paging">
                <!-- prev -->
                <!-- first -->
                <li :class="['paging-item', 'paging-item--first', {'paging-item--disabled' : cpno[tmp.id] === 1}]" @click="first(tmp.id)">{{$t('pages.first')}}</li>
                <li class="paging-item paging-item--prev" :class="{'paging-item--disabled' : cpno[tmp.id] === 1}" @click="prev(tmp.id)">{{$t('pages.prev')}}</li>
                <li :class="['paging-item', {'paging-item--current' : cpno[tmp.id] === page}]" :key="index" v-for="(page, index) in pageNumber[tmp.id]" @click="go(page,tmp.id)">{{page}}</li>
                <!--<li :class="['paging-item', 'paging-item--more']" @click="next" v-if="showNextMore">...</li>-->
                <!-- next -->
                <li :class="['paging-item', 'paging-item--next', {'paging-item--disabled' : cpno[tmp.id] === cpageCountObj[tmp.id]}]" @click="next(tmp.id)">{{$t('pages.next')}}</li>
                <!-- last -->
                <li :class="['paging-item', 'paging-item--last', {'paging-item--disabled' : cpno[tmp.id] === cpageCountObj[tmp.id]}]" @click="last(tmp.id)">{{$t('pages.end')}}</li>
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
    <!--确认框-->
    <div class="modal fade DleConfirm" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
            &times;
          </button>
          <h4 class="text-center" id="myModalLabel">
            {{$t('prompt.prompt')}}
          </h4>
        </div>
        <div class="modal-body">
          <p style="margin-top:20px;">{{$t('prompt.confirmDelete')}}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">{{$t('button.cancel')}}
          </button>
          <button @click='confirm' type="button" class="btn btn-primary">
            {{$t('button.confirm')}}
          </button>
        </div>
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
import BibarReport from '../bibarReport.vue'
import { Toast } from 'mint-ui'
export default{
  // props: ['getNavData'],
  data: function () {
    return {
      articles: [],
      isClick: 0,
      lid: '',
      i: '',
      showComment: false,
      showReport: false,
      nowData: {},
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
      bottomText: '',
      listLoding: true,
      noLoading: false,
      up: 0,
      loadingShow: false,
      talkReplayBox: false,
      replyContent: [],
      talkReplyTxt: false,
      replayId: '',
      showReportReplay: false,
      collection: null,
      hasImg: false,
      hotreplyContent: [],
      isGood: 0,
      isBad: 0,
      // 分页
      replyId: '',
      cpno: {},
      cpageLimit: 10,
      cpageCount: 0,
      showPrevMore: false,
      showNextMore: false,
      showPage: false,
      // 发帖
      changeIndex: false,
      // 加载
      showLoader: false,
      // 评论加载
      showLoaderComment: false,
      pageTimer: null,
      showId: [],
      more: this.$t('button.unfold'),
      moreId: '',
      // 排序样式
      sortNow: 0,
      pageNumber: {},
      cpageCountObj: {},
      imgCommentLength: {},
      sortId: '',
      isDel: false,
      delId: '',
      delIndex: '',
      delItem: '',
      isdelTopic: true
    }
  },
  components: {
    BibarReport
  },
  computed: {
    getNavaVal () {
      return this.$store.state.homePageList.backForNav
    },
    userInfo () {
      return this.$store.state.userInfo.userInfo
    },
    language () {
      return this.$store.state.language.language
    }
  },
  created: function () {
    // 文章分页
    this.$store.dispatch('clear_backForNav')
    this.showLoader = true
    get(`/api/topic/${this.tpno}`).then(data => {
      this.articles = data.data.topics
      this.showLoader = false
      this.pageCount = data.data.page_count
      if (this.articles.length > 0) {
        this.bottomText = this.$t('prompt.loading')
        this.loadingShow = true
      }
      let that = this
      if (this.pageCount === 1) {
        this.bottomText = this.$t('prompt.noMore')
        this.listLoding = false
        this.noLoading = true
        // this.loadingImg = '../../assets/img/noLoading.png'
        return false
      } else {
        document.querySelector('#app').addEventListener('scroll', function () {
          if (this.clientHeight + this.scrollTop === this.scrollHeight) {
            that.loadTopicPage()
          }
        })
      }
    })
  },
  mounted () {
  },
  watch: {
    getNavaVal (val) {
      if (val.length !== 0) {
        this.articles.unshift(val[0])
      }
      this.i = ''
      $('.bibar-hot').css({'display': 'none'})
      this.changeIndex = true
    }
  },
  methods: {
    // 分页
    loadTopicPage () {
      if (this.tpno < this.pageCount) {
        setTimeout(() => {
          this.showLoader = true
          this.tpno++
          get(`/api/topic/${this.tpno}`).then(data => {
            this.articles = this.articles.concat(data.data.topics)
            this.showLoader = false
            this.bottomText = this.$t('prompt.loading')
            // this.loadingImg = '../../assets/img/listLoding.png'
          })
        }, 1000)
      } else {
        this.bottomText = this.$t('prompt.noMore')
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
            } else {
              alert(data.message)
              this.$router.push('/login')
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
            } else {
              alert(data.message)
              this.$router.push('/login')
            }
          })
        }
        // 评论点赞吐槽
      } else if (classId === 1) {
        // 点赞
        if (isNum === 0) {
          get(`/api/reply/up/${id}`).then(data => {
            if (data.resultcode === 1) {
              // $('.comment-item:eq(' + index + ')').find('.set-choseTwo>a:eq(' + isNum + ')').addClass('active')
              item.is_good = data.data.is_good
              item.is_bad = data.data.is_bad
              item.is_bad_bool = data.data.is_bad_bool
              item.is_good_bool = data.data.is_good_bool
            } else {
              alert(data.message)
              this.$router.push('/login')
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
            } else {
              alert(data.message)
              this.$router.push('/login')
            }
          })
        }
      }
    },
    // 去详情页
    goDetail (id) {
      this.lid = id
      this.$router.push({
        path: `/details/${this.lid}`,
        query: {
          a: JSON.stringify([
            {label: this.$t('breadcrumb.home'), path: '/'},
            {label: this.$t('breadcrumb.all'), path: 'last'}
          ])
        }
      })
    },
    // 评论
    showDiscuss (index, id, sort) {
      this.replyId = id
      this.showLoaderComment = true
      if (!this.cpno[id]) {
        this.cpno[id] = 1
      }
      this.sortList(id, 0)
      $('.bibar-tabitem:eq(' + index + ')').find('.bibar-hot').slideToggle('fast')
      this.showId.push(index)
      for (let i = 0; i < this.showId.length; i++) {
        this.showId[i] = i
      }
      if (index !== this.i) {
        this.i = index
        this.lid = id
      } else {
        this.i = ''
        // this.talkReplayBox = false
        // this.commentShow = false
      }
      this.replayId = ''
      this.toId = 0
      this.lid = id
      // if (!this.showComment) {
      //   this.showComment = true
      //   this.commentShow = true
      // } else {
      //   this.showComment = false
      //   this.commentShow = false
      // }
      this.commentShow = true
      if (this.commentShow) {
        this.showReport = false
      }
      $('.editor-toolbar').find('.wangeditor').css({'padding': '0', 'width': '100%'})
      $('.editor-toolbar').find('.wangeditor>.report').css({'bottom': '0', 'padding': '0'})
      $('.editor-toolbar').find('.wangeditor>.cancel').css('bottom', '4px')
      $('.editor-toolbar').find('.wangeditor>.editor').css({'min-height': '130px', 'padding-bottom': '37px'})
      $('.editor-toolbar').find('.wangeditor>div:eq(2)').css('display', 'none')
    },
    // 数据排序
    sortList (id, sort) {
      this.pageId = id
      if (sort === 0) {
        this.sortId = 'replies'
      } else if (sort === 1) {
        this.sortId = 'replies/early'
      } else {
        this.sortId = 'replies/good'
      }
      this.sortNow = sort
      get(`/api/topic/${this.sortId}/${id}/${this.cpno[id]}`).then(data => {
        if (!this.nowData[id]) this.$set(this.nowData, id, data.data.replies)
        else this.nowData[id] = data.data.replies
        if (!this.pageNumber[id]) this.$set(this.pageNumber, id, this.showPageBtn(id, data.data.page_count))
        else this.pageNumber[id] = this.showPageBtn(id, data.data.page_count)
        this.showLoaderComment = false
        this.cpageCount = data.data.page_count
        this.cpageCountObj[id] = this.cpageCount
        if (this.cpageCount > 1) {
          this.showPage = true
        }
        this.$nextTick(() => {
          $('.comment-item-main').find('img').addClass('zoom-in')
          $('[data-w-e]').removeClass('zoom-in')
          $('.comment-item-main').on('click', 'img', function () {
            if (!$(this)[0].hasAttribute('data-w-e')) {
            // if (!$(this)[0].indexOf('alt="[') === -1) {
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
      this.nowData[this.replyId].unshift(data)
      this.articles[this.i].replies_count = data.replies_count
      // get(`/api/topic/${this.tpno}`).then(data => {
      //   // this.showLoader = false
      //   if (this.tpno === 1) {
      //     this.articles = data.data.topics
      //   } else {
      //     if () {

      //     }
      //   }
      // })
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
      this.talkReplayBox = false
      this.nowData[this.replyId].unshift(data)
      this.articles[this.i].replies_count = data.replies_count
      this.replayId = ''
    },
    // 收藏
    collectionTopic (tmp) {
      let instance
      post(`/api/collect/${tmp.id}`).then(data => {
        if (data.resultcode === 0) {
          alert(data.message)
          this.$router.push('/login')
        } else {
          tmp.collect_bool = data.data.collect_bool
          if (data.data.collect_bool) {
            instance = new Toast({
              message: this.$t('prompt.successCollect'),
              iconClass: 'glyphicon glyphicon-ok',
              duration: 1000
            })
          } else {  
            instance = new Toast({
              message: this.$t('prompt.cancelCollect'),
              duration: 1000
            })
          }
          setTimeout(() => {
            instance.close()
          }, 1000)
        }
      })
    },
    // 处理图片
    EditorContent (val) {
      if (val === undefined) {
        return
      }
      let now = val.replace(/<p[^>]*>|<\/p>|<span[^>]*>|<\/span>|<br>|<h[1-6][^>]*>|<\/h[1-6]>|<h-char[^>]*>|<img[^>]*>|<\/h-char>|<h-inner>|<\/h-inner>/g, '')
      now = now.replace(/&nbsp;*/g, '')
      // now = $(now).text()
      if (now.length > 300) {
        return now.substring(0, 300) + '...'
      }
      return now
    },
    // 艾特图片处理
    replyFun (val) {
      if (val === undefined || val === null) {
        return
      }
      let reply = val.replace(/<p[^>]*>|<\/p>|<h-char[^>]*>|<\/h-char>|<h-inner[^>]*>|<\/h-inner>/g, '')
      if (reply.substring(0, 80).indexOf('href') > 0) {
        let imgLength = 0
        if (reply.substring(0, 80).indexOf('img') > 0) {
          let imgArr = []
          imgArr = reply.match(/<img[^>]*>/gi)
          if (imgArr === null) {
            return
          }
          for (let i = 0; i < imgArr.length; i++) {
            imgLength += imgArr[i].length
          }
        }
        let hrefLength = 0
        let hrefArr = reply.match(/<a.*?>(.*?)<\/a>/ig)[0]
        if (hrefArr === null) {
          return
        }
        // for (let i = 0; i < hrefArr.length; i++) {
        //   hrefLength += hrefArr[i].length
        // }
        hrefLength = hrefArr.length
        return reply.substring(0, 40 + hrefLength + imgLength) + '...'
      } else if (reply.substring(0, 80).indexOf('img') > 0) {
        let imgLength = 0
        let imgArr = reply.match(/<img[^>]*>/gi)
        if (imgArr === null) {
          return
        }
        for (let i = 0; i < imgArr.length; i++) {
          imgLength += imgArr[i].length
        }
        return reply.substring(0, 40 + imgLength)
      } else if (reply.length > 40) {
        return reply.substring(0, 40) + '...'
      } else {
        return reply
      }
    },
    // 评论回复文字处理
    commentContent (val, id) {
      // console.log(val)
      if (val === undefined) {
        return
      }
      val = val.replace(/<p[^>]*>|<\/p>|<h-char[^>]*>|<\/h-char>|<h-inner[^>]*>|<\/h-inner>|<br>/g, '')
      // let imgArr = val.match(/<img[^>]*>/gi)
      if (!this.imgCommentLength[id]) {
        this.imgCommentLength[id] = 0
      }
      // if (val.indexOf('img') > 0) {
      //   for (let i = 0; i < imgArr.length; i++) {
      //     this.imgCommentLength[id] += imgArr[i].length
      //   }
      // }
      this.imgCommentLength[id] = val.lastIndexOf('data-w-e="1">')
      if (val.length - this.imgCommentLength[id] > 200) {
        if (id !== this.moreId) {
          let imgVal = val.replace(/<img src="\/static[^>]+>/g, '')
          return imgVal.substring(0, 200 + this.imgCommentLength[id] - 1) + '...'
        } else {
          return val
        }
      } else {
        return val
      }
    },
    changeMore (id) {
      if (id !== this.moreId) {
        this.moreId = id
        this.more =  this.$t('button.fold')
      } else {
        this.more =  this.$t('button.unfold')
        this.moreId = ''
      }
    },
    confirm () {
      if (this.isdelTopic) {
        post(`/api/topic/delete/${this.delId}`).then(data => {
          if (data.resultcode === 1) {
            this.articles.splice(this.delIndex, 1)
            this.i = ''
            $('.bibar-hot').css({'display': 'none'})
            $('.DleConfirm').modal('hide')
          }
        })
      } else {
        post(`/api/reply/delete/${this.delItem}`).then(data => {
          if (data.resultcode === 1) {
            this.nowData[this.delId].splice(this.delIndex, 1)
            this.articles[this.i].replies_count = this.articles[this.i].replies_count - 1
            $('.DleConfirm').modal('hide')
          }
        })
      }
    },
    // 删除文章
    delTopic (tmp, index) {
      $('.DleConfirm').modal('show')
      this.isdelTopic = true
      this.delId = tmp.id
      this.delIndex = index
    },
    // 删除评论
    delComment (item, now, tmp) {
      $('.DleConfirm').modal('show')
      this.isdelTopic = false
      this.delId = tmp.id
      this.delIndex = now
      this.delItem = item.id
    },
    // 分页
    prev (id) {
      if (this.cpno[id] > 1) {
        this.go(this.cpno[id] - 1, id)
      }
    },
    next (id) {
      if (this.cpno[id] < this.cpageCount) {
        this.go(this.cpno[id] + 1, id)
      }
    },
    first (id) {
      if (this.cpno[id] !== 1) {
        this.go(1, id)
      }
    },
    last (id) {
      if (this.cpno[id] !== this.cpageCount) {
        this.go(this.cpageCount, id)
      }
    },
    go (page, id) {
      if (page === '···') {
        return
      }
      this.chartShow = 0
      this.summaryList = []
      if (this.cpno[id] !== page) {
        this.cpno[id] = page
      }
      this.pageId = id
      this.sortList(id, this.sortNow)
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
    // 来自去币讯
    toBibar (tmp) {
      if (tmp.token === null) {
        return
      }
      this.$router.push({
        path: `/msgDetail/${tmp.token}`,
        query: {
          b: JSON.stringify({'zh': tmp.zh_token})
        }
      })
    },
    showPageBtn (id, tatal) {
      let pageArr = []
      if (tatal <= 5) {
        for (let i = 1; i <= tatal; i++) {
          pageArr.push(i)
        }
        return pageArr
      }
      // if (!this.cpno[i]) this.cpno[i] = 1
      if (this.cpno[id] <= 2) return [1, 2, 3, '···', tatal]
      if (this.cpno[id] >= tatal - 1) return [1, '···', tatal - 2, tatal - 1, tatal]
      if (this.cpno[id] === 3) return [1, 2, 3, 4, '···', tatal]
      if (this.cpno[id] === tatal - 2) return [1, '···', tatal - 3, tatal - 2, tatal - 1, tatal]
      return [1, '···', this.cpno[id] - 1, this.cpno[id], this.cpno[id] + 1, '···', tatal]
    }
  }
  // watch: {
  //   articles (va) {
  //     console.log(va, 12)
  //   }
  // }
}
</script>

<style>
  .editor-hot-comment-default{
    left:53px;
    top: 35px;
  }
.replyBackConten>p:first-child{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 500px;
    float: right;
}
/*分页*/
/*.pages{float: right;}*/
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
/*回复样式*/
.replyAuthor{
    height: 50px;
    background: #F8F8F8;
    line-height: 50px !important;
    padding-left: 20px !important;
    font-weight: 700;
    margin: 15px 2px 15px 0;
    font-size: 15px;
}
.glyphicon{
  font-size: 20px;
}
.indexNewslimitHeight{
  cursor: pointer;
}
/*.bibar-tabitem{overflow: hidden;}*/
.bibar-comment{
    position: relative;
    margin-left: 58px;
}
.editor-comment{
    background-color: #F8F8F8;
    /* padding: 20px; */
    padding-left: 10px;
    padding: 15px;
}
.editor-comment>.avatar{
    width: 35px;
    height: 35px;
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
    margin-top: 30px;
    padding-bottom: 15px;
    font-size: 15px;
    /*border-bottom:1px solid #edf0f5;*/
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
    /*border-bottom: 1px solid #edf0f5;*/
    border-top: none;
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
    font-weight: normal;
}
.comment-item-main>p {
    font-size: 15px;
    line-height: 1.6;
    word-break: break-all;
    overflow: hidden;
    margin: 10px 0;
    display: inline;
}
/*.comment-item-main a{color: #0181ff;}*/
.comment-item-main img{
    display: block;
    cursor: zoom-in;
    max-width: 200px;
    width: 200px;
}
.bibar-indexNewsItem-infro>li{
    float: left;
    /*margin-right: 25px;*/
}
.bibar-indexNewsItem-infro>li i {
    margin-right: 3px;
}
  /*回复*/
.comment-reply{
  border-top: 1px solid #edf0f5;
  margin-top: 20px;
  background: #EDF5FE;
  margin-left: 42px;
  /*padding: 8px 0;*/
}
.comment-reply>.comment-item{
  margin: 15px 0;
}
.comment-reply>.editor-comment{
  /*margin-top: 15px;*/
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
/*.bibar-tabitem{
  overflow: hidden;
}*/
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
.w-e-text-container .w-e-panel-container{
  margin-left: 0 !important;
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
.editor-comment>.avatar{
    width: 35px;
    height: 35px;
    float: left;
    margin-top: 5px;
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
    padding: 8px 0;
}
svg:not(:root) {
    overflow: hidden;
}
.editor-triangle{
    position: absolute;
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
.media-left, .media>.pull-left {
    padding-right: 10px;
    /*width: 15%;*/
    overflow: hidden;
    /* height: 50px; */
    /* position: relative; */
    height: 100px;
}
.pull-left > img{max-width: 150px; overflow: hidden; height: 100%;}
</style>
