<template>
  <div class="header" style="height:60px;">
    <!--头部-->
    <header class="bibar-header">
      <section class="bibar-w1100 container">
        <!--Logo-->
        <h1 class="bibar-headerlogo">
          <router-link :to="{path:'/'}"><img src="../../assets/img/logo-BCLUB.png"></router-link>
        </h1>
        <!--菜单-->
        <nav class="bibar-headernav">
          <ul class="bibar-headernavlist">
            <li class="bibar-headernavitem">
              <a href="javascript:void(0)">
                <router-link :class="{headerActive: routerSelect('')}" :to="{path:'/'}">{{$t('nav.index')}}</router-link>
              </a>
            </li>
            <li class="bibar-headernavitem">
              <a href="javascript:void(0)">
                <router-link :class="{headerActive: routerSelect('bibarLayout')}" :to="{path:'/bibarLayout'}">{{$t('nav.coinNews')}}</router-link>
              </a>
            </li>
            <!--<li class="bibar-headernavitem"> <a href="javascript:void(0)"><router-link :class="{headerActive: routerSelect('community')}" :to="{path:'/community'}">社区</router-link></a> </li>-->
            <!--<li class="bibar-headernavitem"> <a href="javascript:void(0)"><router-link :class="{headerActive: routerSelect('maintalk')}" :to="{path:'/maintalk'}">讨论</router-link></a> </li>-->
            <!--<li class="bibar-headernavitem"> <a href="javascript:void(0)"><router-link :class="{headerActive: routerSelect('cream')}" :to="{path:'/cream'}">精华</router-link></a> </li>-->
          </ul>
        </nav>
        <!--搜索框-->
        <div class="bibar-headerSearch">
          <ul class="bibar-headerSearchlist">
            <!--搜索框-->
            <!--<li class="bibar-headerSearchitem">
                      <div class="input-icon left dib">
                          <input type="text" class="form-control btn-circle w180 bg-greyLight" placeholder="搜索">
                          <i class="iconfont">&#xe613;</i> </div>
                  </li>-->
            <li class="bibar-headerSearchitem">
              <!-- 未登录 -->
              <NavLogin v-if="!user_token || !userInfo.isLogin"></NavLogin>
              <!-- 已登录 -->
              <isLogin v-if="user_token && userInfo.isLogin"></isLogin>
            </li>
            <li class="language-switch">
              <a href="#" @click.stop.prevent="switchLang('en')" :class="{'active-language':language==='en'}">English</a> | <a href="#" :class="{'active-language':language==='zh'}" @click.stop.prevent="switchLang('zh')">中文</a>
            </li>
          </ul>
        </div>
      </section>
    </header>
  </div>
</template>

<script>
import NavLogin from './navlogin.vue'
import isLogin from './isLogin.vue'
import { setToken, getToken } from '../../utils/auth'
export default {
  props: {
    message: Boolean
  },
  data: function () {
    return {
      user_token: '',
      remember_token: '',
      language: 'zh'
    }
  },
  components: {
    NavLogin,
    isLogin
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
    if (getToken('language')) {
      this.language = getToken('language')
      this.$store.commit('LANGUAGE', {
        'language': getToken('language')
      })
    }
  },
  methods: {
    switchLang (lang) {
      setToken('language', lang)
      this.language = lang
      this.$store.commit('LANGUAGE', {
        'language': lang
      })
      location.reload()
    },
    // toLoadMain () {
    //   this.$emit('backLoadMain')
    // },
    routerSelect (url) {
      let path = this.$route.path.substr(1)
      if (url === path) {
        return true
      } else if (path.indexOf(url) === 0 && url !== '') {
        return true
      }
      return false
    }
  }
}
</script>

<style>
/*头*/
.language-switch{
  margin-right:20px;
}
.language-switch a{
  font-size:14px;
}
.language-switch .active-language{
  color:#0181ff;
  pointer-events: none;
}
.bibar-header {
  height: 60px;
  background-color: #fff;
  /*box-shadow: 0px 0px 4px 3px #efefef;*/
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100%;
  min-width: 1200px;
  z-index: 10003;
}

.bibar-w1100 {
  width: 1200px;
  margin: 0 auto;
}

.bibar-w1100:after {
  visibility: hidden;
  display: block;
  font-size: 0;
  content: " ";
  clear: both;
  height: 0;
}

.bibar-headerlogo {
  float: left;
  width: 104px;
  height: 60px;
  line-height: 50px;
}

.bibar-headernav ul li {
  float: left;
}

.bibar-headernav ul li a {
  padding:0 10px;
  height: 60px;
  line-height: 56px;
  font-size: 18px;
  text-align: center;
  display: block;
}

.bibar-headerSearch {
  float: right;
  /* margin-top: 15px; */
  line-height: 60px;
  height: 60px;
}

.bibar-headerSearch ul li {
  float: left;
  margin-left: 20px;
}

.bibar-headerSearchitem input {
  font-size: 12px;
  margin-top: 18px;
}

.headerActive {
  color: #0181ff !important;
}
</style>
