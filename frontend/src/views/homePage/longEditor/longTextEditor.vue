<template>
  <div>
    <div ref="editor" style="text-align:left" class='editor'></div>
    <button type="button" @click="getContent" class="report">发布</button>
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
      }
    }
  },
  computed: {
    longId () {
      return this.$store.state.longId
    }
  },
  mounted () {
    let that = this
    var editor = new E(this.$refs.editor)
    editor.customConfig.onchange = (html) => {
      this.editorContent = html
    }
    // 菜单配置
    editor.customConfig.menus = [
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
      'image',
      'table'
    ]
    // 上传图片
    // editor.customConfig.uploadImgShowBase64 = true
    editor.customConfig.uploadImgServer = '/api/file'
    editor.customConfig.uploadImgHooks = {
      success: function (xhr, editor, result) {
        // console.log(result)
      },
      customInsert: function (insertImg, result, editor) {
        // console.log(result)
        that.backLong.url = result.data.file_path
        insertImg(that.backLong.url)
      }
    }
    editor.create()
    $('.long-text-editor').find('.w-e-text-container').css({'border': 'none'})
  },
  methods: {
    getContent: function () {
      this.topicData.content = this.editorContent
      this.imgArr = []
      // let image = this.topicData.content.match(/<img src="\/static[^>]+>/g)
      let image = this.topicData.content.match(/<img[^>]*?(src="(?!\/static\/avatar)[^"]*?")(?!data-w-e)[^>]*?>/g)
      console.log(image)
      this.topicData.picture = ''
      if (this.longId.hideDilog) {
        this.topicData.token = this.longId.bId
      }
      this.topicData.title = this.title
      this.imgObj.imgName = this.imgArr
      if (image !== null) {
        console.log(image)
        for (let i = 0; i < image.length; i++) {
          this.imgArr.push(image[i].match(/(?<=(src="))[^"]*?(?=")/ig)[0])
        }
        post('/api/photo', this.imgObj).then(data => {
          console.log(data)
        })
      }
      if (image !== null) {
        this.topicData.picture = this.topicData.content.match(/<img[^>]*?(src="[^"]*?")(?!data-w-e)[^>]*?>/g)[0]
      }
      //  && this.topicData.picture.indexOf(/static/gi) > 0
      console.log(this.topicData)
      if (this.topicData.content.length > 0 || this.topicData.picture.length > 0) {
        post('/api/topic', this.topicData).then(data => {
          console.log(data)
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
                // this.$router.push(`/msgDetail/${this.longId.bId}`)
              } else {
                // this.$router.push('/')
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
    padding: 6px 10px;
   text-align: center;
   background: #1E8FFF;
   border-radius: 3px;
   color: #fff;
}
.set{
  color: #1E8FFF;
  background: snow;
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
}
.w-e-text-container{z-index: 9999 !important;}
.w-e-toolbar{z-index: 9998 !important;}
</style>
