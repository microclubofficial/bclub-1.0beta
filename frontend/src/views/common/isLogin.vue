<template>
  <div>
    <div class="is_Login">
      <div class="nav_user_info">
        <div class="username_info">
          <a href="javascript:;">
            <div class="user-info" @click="handlePersonal">
              <img class="user-avatar" :src="user_token.avatar ? user_token.avatar : userInfo.avatar" alt="">
              <span class="user-name">{{user_token.username ? user_token.username : userInfo.username}}</span>
            </div>
            <div class="nav-info-msg">
              <a href="#" @click="handleMsg">
                <img src="../../assets/img/bell.png" alt="">
                <i class="count" v-show="hasCount">0</i>
              </a>
              <div class="nav_msg_dropdown" v-show="showMsg">
                <ul>
                  <li class="nav_msg_empty">{{$t('nav.noNews')}}</li>
                  <!--<li class="nav_msg_set">
                    <a href="#">
                      <span><img src="../../assets/img/msg.png" alt="">提醒设置</span>
                    </a>
                  </li>-->
                </ul>
              </div>
            </div>
          </a>
        </div>
        <div class="user_info_dropdown" v-show="showPersonal">
          <ul>
            <!--<li>
              <a href="javascript:void(0)" @click.stop.prevent><img :src="user_token.avatar" alt="">
                <span class="user-name">
                  <router-link :to="{path:'/memberCenter'}">{{user_token.username}}</router-link>
                </span>
              </a>
            </li>-->
            <li>
              <a href="javascript:void(0)" @click.stop.prevent><img src="../../assets/img/personal.png" alt="">
                <span>
                  <router-link :to="{path:'/memberCenter'}">{{$t('nav.personal')}}</router-link>
                </span>
              </a>
            </li>
            <li>
              <a href="javascript:void(0)" @click.stop.prevent><img src="../../assets/img/set.png" alt="">
                <span>
                  <router-link :to="{path:'/personalInfo'}">{{$t('nav.editProfile')}}</router-link>
                </span>
              </a>
            </li>
            <!--<li><a href="javascript:void(0)" @click.stop.prevent><img src="../../assets/img/share.png" alt=""><span>股票设置</span></a></li>-->
            <li>
              <a href="#" @click="outlogin"><img src="../../assets/img/outlogin.png" alt="">
                <span>{{$t('nav.logout')}}</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
      <a href="javascript:void(0)" class="nav_btn_longtext" @click="postModel">{{$t('nav.newTopic')}}</a>
    </div>
    <div class="modal fade hmModal" id="myModal1" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h4 class="modal-title" id="myModalLabel">{{$t('message.sthToSay')}}</h4>
          </div>
          <div class="modal-body">
            <BibarPostContent ref="headerChild" @backFtNav = 'FtNavFun'></BibarPostContent>
          </div>
          <!-- <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            <button type="button" class="btn btn-primary">提交更改</button>
          </div> -->
        </div>
    </div>
  </div>
    <!--<vdialog ref="headerChild" v-show="Showdialog" :toDialog='postEditor'></vdialog>-->
  </div>
</template>

<script>
import { get, post } from '../../utils/http.js'
// import vdialog from './dialog.vue'
import { getToken, removeToken } from '../../utils/auth'
import BibarPostContent from '../homePage/bibarPostContent.vue'
export default {
  data: function () {
    return {
      user_token: '',
      hasCount: false,
      showMsg: false,
      showPersonal: false,
      userName: '',
      useravatar: '',
      Showdialog: false,
      postEditor: {
        'title': this.$t('message.sthToSay'),
        'id': 1
      }
      // isShowft: false
    }
  },
  components: {
    BibarPostContent
  },
  computed: {
    userInfo () {
      return this.$store.state.userInfo.userInfo
    }
  },
  created () {
    if (getToken()) {
      this.user_token = JSON.parse(getToken())
    }
    // console.log(this.user_token)
  },
  mounted () {
    // this.outloginSty()
    $('.bibar-headerSearchitem').find('.toLongText').css({'right': '320px', 'bottom': '0'})
    $('.bibar-headerSearchitem').find('.avatar').css({'display': 'none'})
    $('.bibar-headerSearchitem').find('.editor').css({'width': '570px'})
    $('.bibar-headerSearchitem').find('.cancel').css({'right': '52px', 'bottom': '0px'})
    $('.w-e-text-container').css({'overflow-y': 'scroll', 'height': '87px'})
  },
  watch: {
    $route (val) {
      this.Showdialog = false
    }
  },
  beforeRouteLeave () {
    this.Showdialog = false
  },
  methods: {
    toRegister () {
      this.$router.push('/register')
    },
    toLogin () {
      this.$router.push('/login')
    },
    // 查看消息
    handleMsg (e) {
      this.showMsg = !this.showMsg
    },
    // 查看个人中心
    handlePersonal () {
      this.showPersonal = !this.showPersonal
    },
    // 退出登录
    outlogin () {
      post('api/logout').then(data => {
        if (data.resultcode === 1) {
          this.$store.commit('USER_INFO', {
            'username': '',
            'avatar': '',
            'isLogin': false
          })
          removeToken()         
          this.$router.push('/')
          // this.outloginSty()
          // this.$emit('backLoadContent')
        }
      }).catch(err => {
        console.log(err)
      })
    },
    // 发帖
    postModel () {
      $('#myModal1').modal('show')
      this.$refs.headerChild.ftEditor()
    },
    FtNavFun (data) {
      this.$store.dispatch('set_backForNav', data)
    }
    // // 退登样式
    // outloginSty() {
    //   if (!this.userInfo.isLogin) {
    //     this.userName = ''
    //     this.useravatar = '../../assets/img/login.png'
    //     this.isShowft = false
    //   } else {
    //     this.userName = this.userInfo.username
    //     this.useravatar = this.userInfo.avatar
    //     this.isShowft = true
    //   }
    // }
  }
}
</script>

<style>
.user_info_dropdown>ul>li>a {
  display: inline-block;
}

.is_Login {
  float: right;
  margin-left: 48px;
}

.nav_user_info {
  display: inline-block;
  height: 60px;
  position: relative;
  z-index: 101;
  vertical-align: middle;
  font-size: 15px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.username_info {
  position: relative;
  display: table;
  z-index: 3;
  text-align: right;
}

.username_info>a>.user-info>span.user-name {
  display: inline-block;
  max-width: 8em;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  vertical-align: middle;
}

.username_info>a>.user-info>img.user-avatar {
  width: 22px;
  height: 22px;
  margin-left: 22px;
}

.nav-info-msg {
  -webkit-box-sizing: content-box;
  box-sizing: content-box;
  position: absolute;
  width: 22px;
  height: 100%;
  padding-right: 24px;
  top: 0;
  right: 100%;
  cursor: default;
  /* left: -15px; */
}

.nav-info-msg:before {
  position: absolute;
  right: 0;
  top: 50%;
  -webkit-transform: translateY(-50%);
  transform: translateY(-50%);
  height: 24px;
  width: 1px;
  background-color: #cecece;
  content: '';
}

.nav-info-msg>a {
  position: absolute;
  left: 0;
  top: 50%;
  -webkit-transform: translateY(-50%);
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);
}

.nav-info-msg>a>img {
  width: 28px;
  height: 28px;
}

.nav-info-msg .count {
  position: absolute;
  top: 13px;
  line-height: 14px;
  left: 15px;
  font-size: 12px;
  background-color: #f70;
  padding: 1px 3.5px;
  min-width: 14px;
  text-align: center;
  border-radius: 14px;
  font-style: normal;
}

.nav_msg_dropdown,
.user_info_dropdown {
  -webkit-animation-duration: .2s;
  animation-duration: .2s;
  position: absolute;
  z-index: 1;
  top: 100%;
  font-size: 14px;
  color: #33353c;
  cursor: default;
  width: 100%;
  left: 0;
  min-width:120px;
}

.nav_msg_dropdown {
  right: 0;
  width: 140px;
}

.nav_msg_dropdown ul,
.user_info_dropdown ul {
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .2);
}

.nav_msg_dropdown li,
.user_info_dropdown li {
  margin-left: 0 !important;
  height: 40px;
  line-height: 40px;
  width: 100%;
  padding-left: 10px;
}

.user_info_dropdown li img {
  width: 20px;
  height: 20px;
  margin-right: 10px;
}

.nav_msg_empty {
  text-align: center;
  padding: 3px 0;
  color: #909499;
}

.nav_msg_set {
  border-top: 1px solid #edf0f5;
  text-align: center;
  /* padding-top: 10px; */
}

.nav_msg_set>a>span>img {
  margin-left: -30px;
}

a.nav_btn_longtext {
  display: inline-block;
  /*width: 58px;*/
  text-align: center;
  margin-left: 12px;
  vertical-align: middle;
  color: #0094D9;
  font-size: 13px;
  border: 1px solid #0094D9;
  padding: 4px 15px;
  border-radius: 30px;
  height: 35px;
  line-height: 28px;
}
/*模态框*/
.modal-dialog>.modal-content>.modal-body>.wangeditor>.editor{
  width: 525px;
}
 .modal-dialog>.modal-content>.modal-body>.wangeditor>.editor>.w-e-panel-container{
    width: 300px!important;
    z-index: 20000;
    border-top: 1px solid #ccc!important;
    position: fixed!important;
    top: 195px!important;
}
.modal-body{
    position: relative;
    padding: 0 15px 15px 15px !important;
    margin: 0 !important;
}
.modal-title{
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #000 !important;
}
.modal-header{border: none;border-bottom: 1px solid #e5e5e5;}
.modal-body>.wangeditor{
    width: 570px !important;
    /* margin: 20px auto 0 auto; */
    background-color: #fff;
    padding: 12px 0 !important;
    margin: 0 !important;
    position: relative;
    min-height: 160px;
    /* padding-left: 16%; */
}
.modal-open .modal{
  overflow-y: hidden !important;
}
.modal-body>.wangeditor>.avatar{display: none;}
.modal-body>.wangeditor .report{
  right: 0;
  bottom:21px;
}
.modal-body>.wangeditor .cancel{
    bottom: -6px;
    right: 60px;
}
.modal .modal-content{
  border-radius: 5px !important;
}
/* .w-e-toolbar .w-e-menu{z-index: 10000 !important;} */
.modal-body>.wangeditor>.editor>.w-e-toolbar{
  background: #fff !important;
  bottom: -20px !important;
}
.modal-body>.wangeditor>.editor>.w-e-text-container{border: 1px solid #edf0f5 !important; z-index: 9999;height: 87px !important;}
.modal-body>.wangeditor>.editor>.w-e-text-container>.w-e-panel-container{
    /* margin-left: -285px !important; */
    z-index: 20000;
    position: fixed !important;
    top: 195px !important;
}
.modal-body>.wangeditor .toLongText{
    bottom: 0;
    right: 320px;
}
.modal-body>.wangeditor>.editor{width: 525px;}
</style>
