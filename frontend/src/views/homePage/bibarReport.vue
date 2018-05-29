<template>
    <div>
        <div ref="editor" style="text-align:left" class='editor'></div>
        <button @click="getContent" v-show="toApi!==3 || toApi!==4" class="report btnm">{{$t('button.publish')}}</button>
        <button @click="getContent" v-show="toApi===3 || toApi===4" class="report btnm">{{$t('list.reply')}}</button>
        <button class="cancel" @click="isHideFun">{{$t('button.cancel')}}</button>
        <!-- <div>{{backData}}</div> -->
    </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../utils/http'
import { Toast } from 'mint-ui'

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
      replies: [],
      editor: {},
      imgArr: [],
      imgObj: {}
    }
  },
  watch: {
    editorContent (val) {
      // let editorHeight = this.editor.$textElem[0].offsetHeight
      // console.log($('.w-e-text-container').find('.w-e-panel-container').height())
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    },
    language () {
      return this.$store.state.language.language
    }
  },
  methods: {
    showApi (api) {
      this.nowApi = api
    },
    getContent: function () {
      let that = this
      // this.topicData.content = this.editorContent
      this.topicData.content = this.editor.$textElem.html()
      // 处理链接
      if (this.topicData.content.indexOf('href') > 0) {
        let href = this.topicData.content.match(/(?<=(href="))[^"]*?(?=")/ig)
        for (let i = 0; i < href.length; i++) {
          if (href[i].indexOf('http') === -1) {
            this.topicData.content = this.topicData.content.replace(href[i], 'http://' + href[i])
            let reg = /<a.*?>(.*?)<\/a>/ig
            let result = reg.exec(this.topicData.content)
            this.topicData.content = this.topicData.content.replace(result[1], '<i class="iconfont">&#xe60e;</i>' + result[1] + '&nbsp;')
          }
        }
      }
      if (this.topicData.content.indexOf('<p>') > -1) {
        this.topicData.content = this.topicData.content.replace(/(^<p>)|(<\/p>$)/g, '')
      }
      let tempContent = this.topicData.content.replace(/<br>|&nbsp;|\s|<p>|<\/p>|<div>|<\/div>/g, '')
      if (!tempContent) {
        let instance = new Toast({
          message: this.$t('prompt.emptyContent'),
          duration: 1000
        })
        setTimeout(() => {
          instance.close()
        }, 1000)
        $('.w-e-text').html('')
        return false
      }
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
      // 处理评论内容
      if (this.toApi === 0) {
        if (this.topicData.content.indexOf('img') > 0) {
          let commentImg = this.topicData.content.match(/<img.*?(?:>|\/>)/gi)[0].match(/(?<=(src="))[^"]*?(?=")/ig)[0]
          this.topicData.picture = commentImg
        }
      }
      // 处理回复数据
      if (this.toApi === 4) {
        this.topicData.author = this.replyAuthor
        this.topicData.replyContent = this.replyContent.replace(/<p>|<\/p>|<br>/g, '')
        if (!/^<img.*>$/gi.test(this.topicData.replyContent)) {
          // 处理正常内容
          if (this.topicData.replyContent.indexOf('img') > 0) {
            let replyImg = this.topicData.replyContent.match(/<img(?![^<>]*?data-w-e[^<>]*?>).*?>/g)[0].match(/(?<=(src="))[^"]*?(?=")/ig)[0]
            let replyNewData = this.topicData.replyContent.replace(/<img src="\/static[^>]+>/g, `<a href='${replyImg}'  style='color:#0181FF'><i class='iconfont'>&#xe694;</i>查看图片</a>`)
            this.topicData.replyContent = replyNewData
          }
          // this.topicData.replyContent = replyNewData
        } else {
          if (this.topicData.replyContent.indexOf('data-w-e') === -1) {
            let justReplyImg = this.topicData.replyContent.match(/(?<=(src="))[^"]*?(?=")/ig)[0]
            if (this.language === 'zh') {
              this.topicData.replyContent = '图片评论' + `<a href='${justReplyImg}' style='color:#0181FF'><i class='iconfont'>&#xe694;</i>查看图片</a>`
            } else if (this.language === 'en') {
              this.topicData.replyContent = 'Image comment ' + `<a href='${justReplyImg}' style='color:#0181FF'><i class='iconfont'>&#xe694;</i> View image</a>`
            }
          } else {
            let replyImg = this.topicData.replyContent.match(/<img(?![^<>]*?data-w-e[^<>]*?>).*?>/g)[0].match(/(?<=(src="))[^"]*?(?=")/ig)[0]
            let replyNewData
            if (this.language === 'zh') {
              replyNewData = this.topicData.replyContent.replace(/<img src="\/static[^>]+>/g, `<a href='${replyImg}' style='color:#0181FF'><i class='iconfont'>&#xe694;</i>查看图片</a>`)
            } else if (this.language === 'en') {
              replyNewData = this.topicData.replyContent.replace(/<img src="\/static[^>]+>/g, `<a href='${replyImg}' style='color:#0181FF'><i class='iconfont'>&#xe694;</i> View image</a>`)
            }
            this.topicData.replyContent = replyNewData
          }
        }
      }
      // 上传网络图片
      this.imgArr = []
      let mainImg = this.topicData.content.match(/<img[^>]*?(src="(?!\/static\/avatar)[^"]*?")(?![^<>]*?data-w-e[^<>]*?>)[^>]*?>/g)
      if (mainImg !== null) {
        for (let i = 0; i < mainImg.length; i++) {
          if (mainImg[i].indexOf('alt="[') === -1) {
            this.imgArr.push(mainImg[i].match(/(?<=(src="))[^"]*?(?=")/ig)[0])
          }
        }
        this.imgObj.imgName = this.imgArr
        post('/api/photo', this.imgObj).then(data => {
          for (let key in data.data) {
            let reg = new RegExp(key, 'g')
            let content = that.topicData.content.replace(reg, data.data[key])
            that.topicData.content = content
          }
          this.topicData.picture = data.data[this.imgArr[0]]
          // 请求
          // console.log(this.topicData.content)
          // console.log(this)
          this.reportPost()
        })
      } else {
        this.reportPost()
      }
    },
    reportPost () {
      if (this.topicData.content.length > 0 || this.topicData.url.length > 0) {
        post(`/api/${this.nowShowApi[this.toApi]}${this.toApi === 1 ? '/question' : this.toApi === 2 ? '/answer' : this.toApi === 3 ? '/comment' : ''}/replies/${this.toApi === 0 ? this.mainCommnet : this.toApi === 2 ? this.talkId : this.toApi === 3 ? this.contentId : this.toApi === 5 ? this.detailId : this.mainReplay}`, this.topicData).then(data => {
          //   评论发送完毕
          this.editorContent = ''
          if (data.message === '请先登录' || data.message === 'Please login first') {
            alert(data.message)
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
              backData.bool_delete = data.data.bool_delete
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
    },
    isHideFun () {
      $('.w-e-text-container').find('.w-e-text').html('')
      this.isHide = !this.isHide
    }
  },
  mounted () {
    this.editor = new E(this.$refs.editor)
    this.editor.customConfig.onchange = (html) => {
      this.editorContent = html
    }
    // 菜单配置
    this.editor.customConfig.menus = [
      'emoticon',
      'image',
      'link'
    ]
    // 校验链接
    let that = this
    this.editor.customConfig.linkCheck = function (text, link) {
      if (text === '' || link === '') {
        if (that.language === 'en') {
          return 'Link cannot be empty'
        } else if (that.language === 'zh') {
          return '链接不能为空'
        }
      } else {
        let reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/ig
        if (!reg.test(link)) {
          if (that.language === 'en') {
            return '无效的链接'
          } else {
            return 'Invalid link'
          }
        } else {
          return true
        }
      }
    }
    if (this.language === 'en') {
      // 多语言
      this.editor.customConfig.lang = {
        '设置标题': 'Title',
        '字号': 'Font size',
        '宋体': 'SimSun',
        '微软雅黑': 'Microsoft YaHei',
        '插入': 'Insert',
        '字体': 'Font family',
        '正文': 'Content',
        '文字颜色': 'Font color',
        '背景色': 'Background',
        '链接': 'Link',
        '链接文字': 'Link',
        '设置列表': 'Set List',
        '有序列表': '&nbspOrdered list&nbsp&nbsp&nbsp',
        '无序列表': 'Disordered list',
        '对齐方式': 'Align',
        '靠左': '&nbsp&nbspLeft&nbsp&nbsp&nbsp',
        '居中': '&nbspCenter',
        '靠右': '&nbsp&nbspRight',
        '上传图片': 'Upload image',
        '上传': 'Upload',
        '创建': 'Init'
      }
    }
    // 表情配置
    this.editor.customConfig.emotions = [
      {
        title: this.$t('button.emoji'),
        type: 'image',
        content: [
          {
            alt: '[坏笑]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/50/pcmoren_huaixiao_org.png'
          },
          {
            alt: '[舔屏]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/40/pcmoren_tian_org.png'
          },
          {
            alt: '[笑cry]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/4a/2018new_xiaoku_org.png'
          },
          {
            alt: '[馋嘴]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/fa/2018new_chanzui_org.png'
          },
          {
            alt: '[拜拜]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/fd/2018new_baibai_org.png'
          },
          {
            alt: '[右哼哼]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/c1/2018new_youhengheng_org.png'
          },
          {
            alt: '[左哼哼]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/43/2018new_zuohengheng_org.png'
          },
          {
            alt: '[怒骂]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/87/2018new_zhouma_org.png'},
          {
            alt: '[顶]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/ae/2018new_ding_org.png'
          },
          {
            alt: '[微笑]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/e3/2018new_weixioa02_org.png'},
          {
            alt: '[偷笑]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/71/2018new_touxiao_org.png'
          },
          {
            alt: '[舔屏]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/3e/2018new_tianping_org.png'
          },
          {
            alt: '[亲亲]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/2c/2018new_qinqin_org.png'
          },
          {
            alt: '[太开心]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/1e/2018new_taikaixin_org.png'
          },
          {
            alt: '[挤眼]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/43/2018new_jiyan_org.png'
          },
          {
            alt: '[衰]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/a2/2018new_shuai_org.png'
          },
          {
            alt: '[可怜]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/96/2018new_kelian_org.png'
          },
          {
            alt: '[汗]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/28/2018new_han_org.png'
          },
          {
            alt: '[色]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/9d/2018new_huaxin_org.png'
          },
          {
            alt: '[可爱]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/09/2018new_keai_org.png'
          },
          {
            alt: '[钱]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/a2/2018new_qian_org.png'
          },
          {
            alt: '[思考]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/30/2018new_sikao_org.png'
          },
          {
            alt: '[兔子]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/c6/2018new_tuzi_org.png'
          },
          {
            alt: '[熊猫]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/aa/2018new_xiongmao_org.png'
          },
          {
            alt: '[黑寡妇]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/78/fulian3_heiguafu01_org.png'
          },
          {
            alt: '[格鲁特]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/de/fulian3_gelute01_org.png'
          },
          {
            alt: '[哆啦A梦亲亲]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/e0/dora_qinqin_org.png'
          },
          {
            alt: '[小黄人微笑]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/f0/xhrnew_weixiao_org.png'
          },
          {
            alt: '[蜡烛]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/16/2018new_lazhu_org.png'
          },
          {
            alt: '[月亮]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/d5/2018new_yueliang_org.png'
          },
          {
            alt: '[围观]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/6c/2018new_weiguan_org.png'
          },
          {
            alt: '[蛋糕]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/f9/2018new_dangao_org.png'
          },
          {
            alt: '[音乐]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/1f/2018new_yinyue_org.png'
          },
          {
            alt: '[猪头]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/1c/2018new_zhutou_org.png'
          },
          {
            alt: '[鲜花]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/d4/2018new_xianhua_org.png'
          },
          {
            alt: '[太阳]',
            src: 'http://img.t.sinajs.cn/t4/appstyle/expression/ext/normal/cd/2018new_taiyang_org.png'
          }
        ]
      }
    ]
    // 上传图片
    // editor.customConfig.uploadImgShowBase64 = true
    this.editor.customConfig.uploadImgServer = '/api/file'
    this.editor.customConfig.uploadImgHooks = {
      // success: function (xhr, editor, result) {
      //   console.log(result)
      // },
      customInsert: function (insertImg, result, editor) {
        insertImg(result.data.file_path)
      }
    }
    this.editor.create()
    var div = $('.avatar').parent('div')
    div.addClass('wangeditor')
    div.addClass('clearfloat')
    $('.w-e-text-container').css({'min-height': '87px', 'height': 'auto !important', 'border': '1px solid #F3F2F2'})
    $('.w-e-text-container').find('div').css('min-height', '87px')
    $('.w-e-toolbar').css({'position': 'absolute', 'background': '#F8F8F8', 'bottom': '0', 'border': '0'})
    $('.comment-reply').find('.w-e-text-container').css({'border': '1px solid rgb(237, 242, 249)'})
    $('.comment-reply').find('.w-e-toolbar').css({'background': '#EDF5FE'})
    // $('.comment-reply').find('.editor-svg').css({'left': '38px'})
    $('.bibar-hot').find('.cancel').css({'background': '#F8F8F8'})
  }
}
</script>

<style>
  .initTxt{color: #ddd;}
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
    width: 99%;
    margin: auto;
    position: relative;
    float: left;
    padding-bottom: 45px;
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
    right: 8px;
}
.cancel{
    font-size: 14px;
    color: #909499;
    margin-right: 20px;
    background: #fff;
    position: absolute;
    bottom: 15px;
    right: 65px;
}
.w-e-toolbar{z-index: 9998 !important;}
</style>
