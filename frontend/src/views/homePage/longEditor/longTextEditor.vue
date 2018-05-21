<template>
  <div>
    <div ref="editor" style="text-align:left" class='editor'></div>
    <button type="button" @click="getContent" class="report">{{$t('button.publish')}}</button>
  </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../../utils/http.js'
import { Toast } from 'mint-ui'
export default{
  props: ['title'],
  name: 'editor',
  data: function () {
    return {
      editorContent: '',
      backLong: {
        author: '',
        author_id: 0,
        avatar: '',
        content: '',
        created_at: '',
        diff_time: '',
        id: '',
        is_bad: 0,
        is_bad_bool: false,
        is_good: 0,
        is_good_bool: false,
        title: '',
        updated_at: ''
      },
      topicData: {
        'content': '',
        'title': '',
        'picture': ''
      },
      imgArr: [],
      imgObj: {
        imgName: []
      },
      editor: {}
    }
  },
  computed: {
    longId () {
      return this.$store.state.longId
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
      'head',
      'bold',
      'fontSize',
      'fontName',
      'italic',
      'underline',
      'strikeThrough',
      'foreColor',
      'backColor',
      'link',
      'list',
      'justify',
      'quote',
      'emoticon',
      'image'
    ]
    // 校验链接
    this.editor.customConfig.linkCheck = function (text, link) {
      if (text === '' || link === '') {
        return ('无效的链接')
      } else {
        let reg = /[hH][tT][tT][pP]([sS]?):\/\/(\S+\.)+\S{2,}$/ig
        if (!reg.test(link)) {
          return ('请输入正确的链接地址')
        } else {
          return true
        }
      }
    }
    // 表情配置
    this.editor.customConfig.emotions = [
      {
        title: '表情',
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
      success: function (xhr, editor, result) {
        // console.log(result)
      },
      customInsert: function (insertImg, result, editor) {
        // console.log(result)
        that.backLong.url = result.data.file_path
        insertImg(that.backLong.url)
      }
    }
    this.editor.create()
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
      let tempContent = this.topicData.content.replace(/<br>|&nbsp;|\s|<p>|<\/p>|<div>/g, '')
      if (!tempContent) {
        let instance = new Toast({
          message: '发帖内容不能为空',
          duration: 1000
        })
        setTimeout(() => {
          instance.close()
        }, 1000)
        $('.w-e-text').html('')
        return false
      }
      this.imgArr = []
      let image = this.topicData.content.match(/<img[^>]*?(src="(?!\/static\/avatar)[^"]*?")(?![^<>]*?data-w-e[^<>]*?>)[^>]*?>/g)
      this.topicData.picture = ''
      if (this.longId.hideDilog) {
        this.topicData.token = this.longId.bId
        this.topicData.tokenname = this.longId.bName
      }
      this.topicData.title = this.title
      if (image !== null) {
        for (let i = 0; i < image.length; i++) {
          if (image[i].indexOf('alt="[') === -1) {
            this.imgArr.push(image[i].match(/(?<=(src="))[^"]*?(?=")/ig)[0])
          }
          // console.log(image[i])
        }
        this.imgObj.imgName = this.imgArr
        post('/api/photo', this.imgObj).then(data => {
          for (let key in data.data) {
            let reg = new RegExp(key, 'g')
            let content = that.topicData.content.replace(reg, data.data[key])
            that.topicData.content = content
          }
          // 请求
          this.topicData.picture = this.imgArr[0]
          // console.log(this.topicData.content)
          // console.log(this)
          this.postEditor()
        })
      } else {
        // 首图
        if (/<img[^>]+>/g.test(this.topicData.content)) {
          this.topicData.picture = this.topicData.content.match(/<img(?![^<>]*?data-w-e[^<>]*?>).*?>/g)[0].match(/(?<=(src="))[^"]*?(?=")/ig)[0]
        }
        this.postEditor()
      }
    },
    postEditor () {
      // 首图
      if (this.topicData.content.length > 0 || this.topicData.picture.length > 0) {
        post('/api/topic', this.topicData).then(data => {
          if (data.message === '未登录') {
            alert('先去登录')
            this.$router.push('/login')
          } else {
            if (data.data.content !== '') {
              this.backLong.content = data.data.content
              this.backLong.author = data.data.author
              this.backLong.avatar = data.data.avatar
              this.backLong.id = data.data.id
              this.backLong.diff_time = data.data.diff_time
              this.backLong.is_good = data.data.is_good
              $('.w-e-text-container').find('p').html('')
              if (this.longId.hideDilog) {
                this.$router.push({
                  path: `/msgDetail/${this.longId.bId}`,
                  query: {
                    b: JSON.stringify({'zh': this.longId.bName})
                  }
                })
              } else {
                this.$router.push('/')
              }
            }
          }
        })
      } else {
        let instance = new Toast({
          message: '发帖内容不能为空',
          duration: 1000
        })
        setTimeout(() => {
          instance.close()
        }, 1000)
      }
    }
  }
}
</script>

<style>
.report{
  /*padding: 6px 10px;*/
   text-align: center;
   background: #1E8FFF;
   border-radius: 3px;
   color: #fff;
}
.set{
  color: #1E8FFF;
  /*background: snow;*/
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
.long-text-editor>div>.editor> .w-e-toolbar{
  border-top:1px solid #ccc !important;
  border-bottom: 1px solid #ccc !important;
  border-left: none !important;
  border-right: none !important;
  background: #fff !important;
  width:100%;
  /*position:relative !important;*/
}
.long-text-editor>div>.editor> .w-e-text-container{
  border:none !important;
  height: 300px !important;
}
.long-text-editor>div>.editor> .w-e-text-container > .w-e-panel-container{
  top: 0 !important;
}
.long-text-editor>div>.editor> .w-e-text-container > .w-e-panel-container{
  top: 0 !important;
  left: 315px !important;
}
.w-e-text-container{z-index: 9999 !important;}
.w-e-toolbar{z-index: 9998 !important;}
.w-e-panel-tab-title>.w-e-item:nth-child(2){display: none;}
</style>
