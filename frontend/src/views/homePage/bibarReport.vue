<template>
    <div>
        <div class="avatar"><img :src="userInfo.avatar" alt=""></div>
        <svg version='1.1' xmlns='http://www.w3.org/2000/svg' class="editor-svg">
          <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
        </svg>
        <div ref="editor" style="text-align:left" class='editor'></div>
        <button @click="getContent" v-show="toApi!==3 || toApi!==4" class="report btnm">发布</button>
        <button @click="getContent" v-show="toApi===3 || toApi===4" class="report btnm">回复</button>
        <button class="cancel" @click="isHideFun">取消</button>
        <!-- <div>{{backData}}</div> -->
    </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../utils/http'

export default {
  props: ['contentId', 'toApi', 'talkId', 'mainReplay', 'mainCommnet', 'replyAuthor', 'replyContent', 'detailId'],
  name: 'editor',
  data () {
    return {
      editorContent: '',
      topicData: {
        'content': '',
        'url': ''
      },
      backData: {
        'author': '',
        'avatar': '',
        'created_at': '',
        'updated_at': '',
        'title': '',
        'content': '',
        'is_good': 0,
        'is_bad': 0,
        'url': '',
        replt_count: 0
      },
      nowShowApi: ['topic', 'bar', 'bar', 'bar', 'comment', 'topic'],
      isHide: false,
      replies: []
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  methods: {
    showApi (api) {
      this.nowApi = api
    },
    getContent: function () {
      this.topicData.content = this.editorContent
      if (this.toApi !== 0 && this.toApi !== 5 && this.toApi !== 4) {
        // 处理正常内容
        let image = this.topicData.content.match(/<img src="\/static[^>]+>/g)
        let newData = this.topicData.content.split(/<img src="\/static[^>]+>/g)
        this.topicData.url = ''
        if (image !== null) {
          for (let j = 0; j < image.length; j++) {
            this.topicData.url += `${image[j]}`
          }
        }
        this.topicData.content = ''
        for (let i = 0; i < newData.length; i++) {
          this.topicData.content += `${newData[i]}`
        }
      }
      // 处理回复数据
      if (this.toApi === 4) {
        this.topicData.author = this.replyAuthor
        this.topicData.replyContent = this.replyContent.replace(/<p>|<\/p>|<br>/g, '')
        if (!/^<img.*>$/gi.test(this.topicData.replyContent)) {
          // 处理正常内容
          let replyNewData = this.topicData.replyContent.split(/<img src="\/static[^>]+>/g)[0]
          this.topicData.replyContent = replyNewData
        } else {
          this.topicData.replyContent = this.topicData.replyContent.match(/(?<=(src="))[^"]*?(?=")/ig)[0]
        }
      }
      if (this.topicData.content.length > 0 || this.topicData.url.length > 0) {
        post(`/api/${this.nowShowApi[this.toApi]}${this.toApi === 1 ? '/question' : this.toApi === 2 ? '/answer' : this.toApi === 3 ? '/comment' : ''}/replies/${this.toApi === 0 ? this.mainCommnet : this.toApi === 2 ? this.talkId : this.toApi === 3 ? this.contentId : this.toApi === 5 ? this.detailId : this.mainReplay}`, this.topicData).then(data => {
          //   评论发送完毕
          this.editorContent = ''
          if (data.message === '未登录') {
            alert('先去登录')
            this.$router.push('/login')
          } else {
            if (data.data.content !== '') {
              let backData = {}
              backData.at_user = data.data.at_user
              backData.avatar = data.data.avatar
              backData.author = data.data.author
              backData.author_id = data.data.author_id
              backData.content = data.data.content
              backData.diff_time = data.data.diff_time
              backData.is_bad = data.data.is_bad
              backData.is_good = data.data.is_good
              backData.id = data.data.id
              backData.picture = data.data.picture
              backData.url = data.data.url
              backData.reference = data.data.reference
              backData.replies_count = data.data.replies_count
              let hotreplies = {}
              hotreplies = data.data
              // 热门回复
              this.$emit('backhotReplies', hotreplies)
              // 回复
              this.replies = data.data.replies
              this.$emit('backReplies', this.replies)
              this.$emit('backList', backData)
              $('.w-e-text-container').find('.w-e-text').html('')
            }
          }
        })
      }
    //   get('api/topic').then(data => {
    //     console.log('这是传回来' + data)
    //   })
    },
    isHideFun () {
      $('.w-e-text-container').find('.w-e-text').html('')
      this.isHide = !this.isHide
    }
  },
  mounted () {
    var editor = new E(this.$refs.editor)
    editor.customConfig.onchange = (html) => {
      this.editorContent = html
    }
    // 菜单配置
    editor.customConfig.menus = [
      'emoticon',
      'image',
      'link'
    ]
    // 上传图片
    // editor.customConfig.uploadImgShowBase64 = true
    editor.customConfig.uploadImgServer = '/api/file'
    editor.customConfig.uploadImgHooks = {
      // success: function (xhr, editor, result) {
      //   console.log(result)
      // },
      customInsert: function (insertImg, result, editor) {
        insertImg(result.data.file_path)
      }
    }
    editor.create()
    var div = $('.avatar').parent('div')
    div.addClass('wangeditor')
    div.addClass('clearfloat')
    $('.w-e-text-container').css({'min-height': '87px', 'height': 'auto', 'border': '1px solid #F3F2F2'})
    $('.w-e-text-container').find('div').css('min-height', '87px')
    $('.w-e-toolbar').css({'position': 'absolute', 'background': '#F8F8F8', 'bottom': '0', 'border': '0'})
    $('.comment-reply').find('.w-e-text-container').css({'border': '1px solid rgb(237, 242, 249)'})
    $('.comment-reply').find('.w-e-toolbar').css({'background': '#EDF5FE'})
    $('.comment-reply').find('.editor-svg').css({'left': '38px'})
    $('.bibar-hot').find('.cancel').css({'background': '#F8F8F8'})
  }
}
</script>

<style>
  .editor-svg{
    position: absolute;
    top: 22px;
    left: 41px;
    width: 5px;
    height: 10px;
    z-index: 10001;
  }
  .editor-svg>.arrow {
    stroke: #F3F2F2;
    fill: #f9fcfe;
}
  .w-e-text-container{background: #fff;}
.w-e-panel-tab-title>.w-e-item:nth-child(2){display: none;}
.comment-reply .wangeditor{
  /*padding-left: 7% !important;*/
  width: 100%;
  background: #EDF5FE;
}
.comment-reply .wangeditor .editor{
  padding-bottom: 33px;
}
.comment-reply .wangeditor .report{
  /*right: 60px;*/
  bottom: 1px;
}
.comment-reply .wangeditor .cancel{
  background: #EDF5FE !important;
  bottom: 4px;
}
/*.bibar-commun {
    margin: -20px auto 0 auto;
}*/
.bibar-box {
    background-color: #fff;
    box-shadow: navajowhite;
}
.wangeditor{
    position: relative;
}
.avatar{
    float: left;
    margin-right: 10px;
    width: 35px;
    height: 35px;
    border-radius: 50%;
}
.avatar>img{
    width: 100%;
    height: 100%;
    border-radius: 50%;
}
.editor{
    width: 85%;
    margin: auto;
    position: relative;
    float: left;
}
.btnm{
    display: inline-block;
    min-width: 48px;
    line-height: 1.25;
    font-size: 14px;
    text-align: center;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    cursor: pointer;
    padding-top: 5px;
    padding-bottom: 5px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 2px;
    vertical-align: middle;
    color: #fff;
    background-color: #1369bf;
    border: 1px solid #1369bf;
}
.report{
    min-width: 64px;
    padding: 0 10px;
    height: 30px;
    line-height: 30px;
    border-radius: 2px;
    position: absolute;
    bottom: 10px;
    right: 98px;
}
.cancel{
    font-size: 14px;
    color: #909499;
    margin-right: 20px;
    background: #fff;
    position: absolute;
    bottom: 15px;
    right: 150px;
}
.w-e-toolbar{z-index: 9998 !important;}
</style>
