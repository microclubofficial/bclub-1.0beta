<style lang="scss" scoped>
.personal-info {
    background-color: #fefefe;
    border: 1px solid #eee;
    padding: 20px;
    display: flex;
    display: -webkit-flex;
    align-items: center;
}
</style>

<template>
    <div class="member-center">
        <div class="container">
            <ol class="breadcrumb">
                <li>
                    <a href="/">首页</a>
                </li>
                <li class="active">个人中心</li>
            </ol>
            <ul class="nav nav-tabs">
                <li v-for="(item,index) in infoList" :class="{active:item.name==$route.name}" @click="routerGo(item)" :key="index">
                    <a href="#">{{item.name}}</a>
                </li>
            </ul>
            <div class="personal-info">
                <router-view></router-view>
            </div>
            <section>
                <div class="main-list">

                </div>
            </section>
        </div>

    </div>
</template>
<script>
// import {post} from '../utils/http'
export default {
  data () {
    return {
      infoList: [
        { 'name': '个人资料', 'path': '/personalInfo/editInfo' },
        { 'name': '修改头像', 'path': '/personalInfo/editAvatar' },
        { 'name': '修改密码', 'path': '/personalInfo/editPassword' },
        { 'name': '绑定邮箱', 'path': '/personalInfo/bindEmail' }
      ]
    }
  },
  methods: {
    routerGo (item) {
      this.$router.push({ path: item.path });
    }
  }
}
</script>
