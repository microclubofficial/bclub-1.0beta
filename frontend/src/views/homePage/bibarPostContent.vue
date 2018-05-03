<template>
    <div>
        <div class="avatar"><img :src="userInfo.avatar" alt=""></div>
        <div ref="editor" style="text-align:left" class='editor'></div>
        <span class="toLongText"  @click="toBibarData(4)"><img src="../../assets/img/longText.png">长文</span>
        <button @click="getContent" class="report btnm" data-dismiss="modal">发布</button>
        <button class="cancel" @click="isHideFun"  v-if="!showDilog">取消</button>
        <button class="cancel"  data-dismiss="modal" @click="isHideFun" v-if="showDilog">取消</button>
        <!-- <div>{{backData}}</div> -->
    </div>
</template>

<script>
import E from 'wangeditor'
import {post} from '../../utils/http'
import { Toast } from 'mint-ui'

export default {
  props: ['contentId', 'fromHeader'],
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
      showDilog: false
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
      this.topicData.content = this.editorContent
      let image = this.topicData.content.match(/<img src="\/static[^>]+>/g)
      this.topicData.picture = ''
      if (image !== null) {
        this.topicData.picture = image[0]
        this.topicData.picture = this.topicData.picture.slice(this.topicData.picture.indexOf('/'), this.topicData.picture.lastIndexOf('=') - 7)
      }
      if (this.$route.path !== '/') {
        this.topicData.token = this.$route.params.currency
      }
      this.$store.commit('LONG_ID', {
        hideDilog: !this.showDilog,
        bId: this.$route.params.currency
      })
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
              backFt.updated_at = data.data.updated_at
              backFt.content = data.data.content
              backFt.author = data.data.author
              backFt.avatar = data.data.avatar
              backFt.id = data.data.id
              backFt.picture = data.data.picture
              backFt.reply_user = null
              backFt.replies_count = 0
              if (this.showDilog) {
                this.$emit('backFtNav', backFt)
                this.showDilog = false
              } else {
                this.$emit('backFtContent', backFt)
              }
              $('.w-e-text').html('')
              // this.$emit('backBibarContent', data.data.content)
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
    },
    isHideFun () {
      alert(1)
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
          bId: this.$route.params.currency
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
    var editor = new E(this.$refs.editor)
    editor.customConfig.onchange = (html) => {
      this.editorContent = html
    }
    // 菜单配置
    editor.customConfig.menus = [
      'emoticon',
      'image',
      'link',
      'bold',
      'italic',
      '|',
      'quote'
    ]
    // 上传图片
    // editor.customConfig.uploadImgShowBase64 = true
    editor.customConfig.uploadImgServer = '/api/file'
    editor.customConfig.uploadImgHooks = {
      // success: function (xhr, editor, result) {
      //   // console.log(result)
      // },
      customInsert: function (insertImg, result, editor) {
        that.backFt.picture = result.data.file_path
        insertImg(that.backFt.picture)
      }
    }
    editor.create()
    // get('/api/avatar').then(data => {
    //   this.articles = data.data.topics
    // })
    var div = $('.avatar').parent('div')
    div.addClass('wangeditor')
    $('.editor').css({'height': 'auto', 'padding-bottom': '37px'})
    $('.w-e-text-container').css({'min-height': '87px', 'height': 'auto', 'border': '1px solid rgb(204, 204, 204)'})
    $('.w-e-text-container').find('div').css('min-height', '87px')
    $('.w-e-toolbar').css({'position': 'absolute', 'bottom': '0', 'border': '0', 'background-color': '#fff'})
  }
}
</script>

<style scoped>
.toLongText{
    cursor: pointer;
    position: absolute;
    bottom: 26px;
    right: 400px;
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
    padding: 20px 0;
    position: relative;
    overflow: hidden;
    padding-left: 10%;
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
    bottom: 20px;
    right: 125px;
}
.cancel{
    font-size: 14px;
    color: #909499;
    margin-right: 20px;
    background: #fff;
    position: absolute;
    bottom: 25px;
    right: 192px;
}
.w-e-toolbar{z-index: 9998 !important;}
</style>
