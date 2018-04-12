<template>
  <div>
    <div ref="editor" style="text-align:left" class='editor'></div>
    <button @click="getContent" class="report">发布</button>
  </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../../utils/http.js'
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
        'title': ''
      }
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
      'bold',
      'italic',
      'head',
      'image',
      'emoticon',
      'link'
    ]
    // 上传图片
    // editor.customConfig.uploadImgShowBase64 = true
    editor.customConfig.uploadImgServer = '/api/file'
    editor.customConfig.uploadImgHooks = {
      // success: function (xhr, editor, result) {
      //   // console.log(result)
      // },
      customInsert: function (insertImg, result, editor) {
        that.backData.url = result.data.file_path
        insertImg(that.backData.url)
      }
    }
    editor.create()
    $('.long-text-editor').find('.w-e-text-container').css({'border': 'none'})
    // $('.long-text-editor').find('.w-e-toolbar').css({''})
  },
  methods: {
    getContent: function () {
      this.topicData.content = this.editorContent
      this.topicData.title = this.title
      console.log(this.topicData)
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
            this.backLong.is_good = data.dta.is_good
            $('.w-e-text-container').find('p').html('')
          }
        }
      })
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
.long-text-editor>div>.editor> .w-e-toolbar{
  border-top:1px solid #ccc !important;
  border-bottom: 1px solid #ccc !important;
  border-left: none !important;
  border-right: none !important;
  background: #fff !important;
}
.w-e-text-container .w-e-panel-container{
    margin-left: -396px !important;
}
</style>
