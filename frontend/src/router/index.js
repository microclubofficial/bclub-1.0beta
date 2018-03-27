/**
 * 项目工程的路由配置文件
 */
// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading
import Vue from 'vue'
import Router from 'vue-router'

/* Layout */
import bibarLayout from 'src/views/BibarFirst/main'
import homeLayout from 'src/views/community/commun'
import maintalk from 'src/views/maintalk/maintalk'
import cream from 'src/views/cream/cream'
import detail from 'src/views/details/details'
// 各种币详情
import mainDetail from 'src/views/details/mainDetails'

// 讨论详情
import talkDetail from 'src/views/community/talkDetail'
import talkBibar from 'src/views/community/talkdetail/talkBibar'
const _import = require('./_import_' + process.env.NODE_ENV)

Vue.use(Router)

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
 **/
export const constantRouterMap = [
  { path: '/login', component: _import('login/index'), hidden: true },
  { path: '/register', component: _import('login/register'), hidden: true },
  // { path: '/authredirect', component: _import('login/authredirect'), hidden: true },
  { path: '/404', component: _import('404'), hidden: true },
  // { path: '/401', component: _import('errorPage/401'), hidden: true },
  { path: '/bibarLayout',
    // name: 'main',
    component: bibarLayout,
    children: [
      {path: '', component: _import('BibarFirst/BibarList/all')},
      {
        path: 'all', component: _import('BibarFirst/BibarList/all')
      },
      {path: 'talk', component: _import('BibarFirst/BibarList/talk')},
      {path: 'works', component: _import('BibarFirst/BibarList/works')},
      {path: 'news', component: _import('BibarFirst/BibarList/news')},
      {path: 'trade', component: _import('BibarFirst/BibarList/trade')}
    ]
  },
  {
    path: '/mainDetail/:pageId', component: mainDetail
  },
  {
    path: '/talkDetail/:talkId',
    component: talkDetail,
    children: [
      {path: '', component: _import('community/talkdetail/recommend')},
      {
        path: 'tech',
        component: _import('community/talkdetail/recommend')
      },
      {
        path: 'future',
        component: _import('community/talkdetail/newSubject')
      }
    ]
  },
  {
    path: '/talkBibar/:tbId', component: talkBibar
  },
  {
    path: '/details/:id', component: detail
  },
  {
    path: '/maintalk', component: maintalk
  },
  {
    path: '/cream', component: cream
  },
  { path: '',
    // name: 'community',
    component: homeLayout,
    children: [
      {path: '', component: _import('community/CommunList/hot')},
      {path: 'hot', component: _import('community/CommunList/hot')},
      {path: 'market', component: _import('community/CommunList/market')},
      {path: 'analyst', component: _import('community/CommunList/analyst')},
      {path: 'depth', component: _import('community/CommunList/depth')},
      {path: 'baike', component: _import('community/CommunList/baike')}
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
