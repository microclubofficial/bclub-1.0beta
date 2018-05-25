<template>
    <div>
        <div class="avatar"><img :src="userInfo.avatar" alt=""></div>
        <!--<svg version='1.1' style='top:61px; left:56px; z-index:10001' xmlns='http://www.w3.org/2000/svg' class="editor-triangle">
            <path d='M5 0 L 0 5 L 5 10' class="arrow"></path>
           </svg>-->
        <div ref="editor" style="text-align:left" class='editor'></div>
        <span class="toLongText" @click="toBibarData(4)"><i class="iconfont" style='font-size:14px;'>&#xe67d;</i>{{$t('button.longText')}}</span>
        <button @click="getContent()" class="report btnm">{{$t('button.publish')}}</button>
        <button class="cancel" @click="isHideFun" v-if="!showDilog">{{$t('button.cancel')}}</button>
        <button class="cancel" @click="isHideFun" v-if="!showDilog">{{$t('button.cancel')}}</button>
        <!-- <div>{{backData}}</div> -->
    </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../utils/http'
import { Toast } from 'mint-ui'

export default {
  props: ['contentId', 'fromHeader', 'tokenBibar'],
  name: 'editor',
  data () {
    return {
      editorContent: '',
      topicData: {
        'content': '',
        'picture': ''
      },
      backFt: {
        'author': '',
        'avatar': '',
        'created_at': '',
        'updated_at': '',
        'title': '',
        'content': '',
        'is_good': 0,
        'is_bad': 0,
        'picture': '',
        replt_count: 0
      },
      showDilog: false,
      editor: {},
      imgArr: [],
      imgObj: {}
    }
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    },
    chartId () {
      return this.$store.state.chartId.chartId
    },
    longId () {
      return this.$store.state.longId
    }
  },
  methods: {
    getContent: function () {
      let that = this
      // this.topicData.content = this.editorContent
      this.topicData.content = this.editor.$textElem.html()
      // 处理插入链接
      if (this.topicData.content.indexOf('href') > -1) {
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
      // let image = this.topicData.content.match(/<img src="\/static[^>]+>/g)
      // this.topicData.picture = ''
      // if (image !== null) {
      //   this.topicData.picture = image[0]
      //   this.topicData.picture = this.topicData.picture.slice(this.topicData.picture.indexOf('/'), this.topicData.picture.lastIndexOf('=') - 7)
      // }
      // 处理首图
      if (/<img.*?(?:>|\/>)/gi.test(this.topicData.content)) {
        let image = this.topicData.content.match(/<img(?![^<>]*?data-w-e[^<>]*?>).*?>/g)
        if (image !== null) {
          image = image[0].match(/(?<=(src="))[^"]*?(?=")/ig)[0]
        }
        this.topicData.picture = image
      }
      // 处理路由
      if (this.$route.path !== '/' && this.$route.path.indexOf('details') === -1) {
        this.topicData.token = this.$route.params.currency
        if (this.tokenBibar) {
          this.topicData.tokenname = this.tokenBibar
        } else if (JSON.stringify(this.$route.query) !== '{}') {
          this.topicData.tokenname = JSON.parse(this.$route.query.b).zh
        } else {
          this.topicData.tokenname = '币吧'
        }
      }
      // 上传网络图片
      this.imgArr = []
      let contentImg = this.topicData.content.match(/<img[^>]*?(src="(?!\/static\/avatar)[^"]*?")(?![^<>]*?data-w-e[^<>]*?>)[^>]*?>/g)
      if (contentImg !== null) {
        for (let i = 0; i < contentImg.length; i++) {
          if (contentImg[i].indexOf('alt="[') === -1) {
            this.imgArr.push(contentImg[i].match(/(?<=(src="))[^"]*?(?=")/ig)[0])
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
          this.postContent()
        })
      } else {
        this.postContent()
      }
      // this.$store.commit('LONG_ID', {
      //   hideDilog: !this.showDilog,
      //   bId: this.$route.params.currency,
      //   bName: JSON.parse(this.$route.query.b).zh
      // })
    },
    // post内容
    postContent () {
      if (this.topicData.content.length > 0 || this.topicData.picture.length > 0) {
        post(`/api/topic`, this.topicData).then(data => {
          this.editorContent = ''
          if (data.message === '未登录') {
            alert('先去登录')
            this.$router.push('/login')
          } else {
            if (data.data.content !== '') {
              let backFt = {}
              backFt.author_id = data.data.author_id
              backFt.board_id = data.data.board_id
              backFt.content_type = data.data.content_type
              backFt.diff_time = data.data.diff_time
              backFt.is_bad = data.data.is_bad
              backFt.is_good = data.data.is_good
              backFt.title = data.data.title
              backFt.token = data.data.token
              backFt.zh_token = data.data.zh_token
              backFt.updated_at = data.data.updated_at
              backFt.content = data.data.content
              backFt.author = data.data.author
              backFt.avatar = data.data.avatar
              backFt.id = data.data.id
              backFt.picture = data.data.picture
              backFt.reply_user = null
              backFt.replies_count = 0
              backFt.bool_delete = data.data.bool_delete
              if (this.showDilog) {
                this.$emit('backFtNav', backFt)
                this.showDilog = false
                $('#myModal1').modal('hide')
                // document.body.removeChild(document.querySelector('.modal-backdrop'))
              } else {
                this.$emit('backFtContent', backFt)
              }
              $('.w-e-text').html('')
              // this.$emit('backBibarContent', data.data.content)
              // this.$router.push('/')
            }
          }
        })
      } else {
        let instance = new Toast({
          message: this.$t('prompt.emptyContent'),
          duration: 1000
        })
        setTimeout(() => {
          instance.close()
        }, 1000)
      }
    },
    isHideFun () {
      $('.w-e-text').html('')
    },
    toBibarData (router) {
      $('#myModal').removeClass('in')
      $('body').removeClass('modal-open')
      if (this.showDilog) {
        document.body.removeChild(document.querySelector('.modal-backdrop'))
      }
      if (this.showDilog) {
        this.$store.commit('LONG_ID', {
          hideDilog: !this.showDilog,
          bId: ''
        })
      } else {
        this.$store.commit('LONG_ID', {
          hideDilog: !this.showDilog,
          bId: this.$route.params.currency,
          bName: JSON.parse(this.$route.query.b).zh
        })
      }
      this.$router.push(`/mainDetail/${router}`)
    },
    ftEditor () {
      this.showDilog = true
    }
  },
  mounted () {
    let that = this
    this.editor = new E(this.$refs.editor)
    this.editor.customConfig.onchange = (html) => {
      this.editorContent = html
    }
    // 菜单配置
    this.editor.customConfig.menus = [
      'emoticon',
      'image',
      'link',
      'bold',
      'italic',
      '|',
      'quote'
    ]
    // 校验链接
    this.editor.customConfig.linkCheck = function (text, link) {
      if (text === '' || link === '') {
        return this.$t('prompt.emptyLink')
      } else {
        let reg = /[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?/ig
        if (!reg.test(link)) {
          return this.$t('prompt.invalidLink')
        } else {
          return true
        }
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
      //   // console.log(result)
      // },
      customInsert: function (insertImg, result, editor) {
        that.backFt.picture = result.data.file_path
        insertImg(that.backFt.picture)
      }
    }
    this.editor.create()
    // get('/api/avatar').then(data => {
    //   this.articles = data.data.topics
    // })
    var div = $('.avatar').parent('div')
    div.addClass('wangeditor')
    div.addClass('clearfloat')
    $('.editor').css({'height': 'auto', 'padding-bottom': '37px'})
    $('.w-e-text-container').css({'min-height': '87px', 'border': '1px solid #F6F5F5'})
    $('.w-e-text-container').find('div').css('min-height', '87px')
    $('.w-e-toolbar').css({'position': 'absolute', 'bottom': '0', 'border': '0', 'background-color': '#F8F8F8'})
  }
}
</script>

<style scoped>
.w-e-panel-tab-title>.w-e-item:nth-child(2){display: none;}
.toLongText{
    cursor: pointer;
    position: absolute;
    bottom: 20px;
    right: 555px;
    color: #999;
}
.toLongText img{
  margin-right: 5px;
}
.bibar-commun {
    margin: -20px auto 0 auto;
}
.bibar-box {
    background-color: #fff;
    box-shadow: navajowhite;
}
.wangeditor{
    width: 790px;
    /* margin: 20px auto 0 auto; */
    background-color: #fff;
    padding: 30px 15px 15px 15px;
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
    width: 540px;
    margin: auto;
    height: 116px;
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
    bottom: 15px;
    right: 22px;
}
.cancel{
    font-size: 14px;
    color: #909499;
    margin-right: 20px;
    background: #fff;
    position: absolute;
    bottom: 20px;
    right: 80px;
}
.w-e-toolbar{z-index: 9998 !important;}
</style>
