<style lang="scss" scoped>
.wrap-width {
    width: 1190px;
    margin: 0 auto;
}

.member-center {
    margin-top: 40px;
}

.personal-info {
    background-color: #fefefe;
    border: 1px solid #eee;
    display: flex;
    display: -webkit-flex;
    align-items: center;
}

.breadcrumb {
    .hover:hover {
        color: #1e8fff;
    }
}

//加入样式
.nav-width {
    width: 236px;
    height: 580px;
    background: #fff;
    float: left;
    border-bottom: none;
    margin-right: 14px;

    .tx-box {
        width: 236px;
        height: 80px;
        margin-top: 30px;
    }
    .tx {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        overflow: hidden;
        margin: 0 auto;
        >img {
            width: 100%;
            height: 100%;
        }
    }
    .name {
        font-size: 16px;
        font-weight: bold;
        padding: 10px 0;
    }
    .grade {
        margin-bottom: 10px;
        span {
            font-size: 14px;
            color: #fff;
            background: #ffce0a;
            padding: 4px 12px;
            border-radius: 10px;
        }
    }
    li {
        width: 236px;
        height: 48px;
        line-height: 48px;
        display: block;
        text-align: center;
        border: none;
        &.active {
            a {
                border: 0;
                height: 48px;
                line-height: 48px;
                background: #f6f6f6;
            }
        }
        &:hover {
            width: 236px;
            border: none;
            
        }

        a {
            margin: 0;
            padding: 0;
            height: 48px;
            font-size: 14px;
            border: none;
            line-height: 48px;

            &:hover {
                border: none;
            }
        }
    }
}

.info-border {
    border-bottom: solid 1px #dfdfdf;
}

.right-width {
    width: 840px;
    float: left;
}
</style>

<template>
    <div>
        <MainHeader></MainHeader>
        <div class="member-center">
            <div class="wrap-width">
                <ol class="breadcrumb">
                    <li>
                        <router-link to='/'>
                            <i class="iconfont" style="margin-right:10px;">&#xe65a;</i>{{$t('editProfile.index')}}</router-link>
                    </li>
                    <li class="active">
                        <router-link class="hover" :to="{path:'/memberCenter'}">{{$t('personalCenter.personal')}}</router-link>
                    </li>
                </ol>
                <ul class="nav  nav-tabs nav-width">
                    <li class="tx-box">
                        <div class="tx">
                            <img src="../../assets/img/tx.png" />
                        </div>
                    </li>
                    <li class="name">楚人长侠</li>
                    <li class="grade">
                        <span>星级达人</span>
                    </li>
                    <li v-for="(item,index) in infoList" :class="{active:item.name === $route.name}" @click="routerGo(index)" :key="index">
                        <a href="javascript:void(0)">{{item.cnName}}</a>
                    </li>
                </ul>
                <div class="personal-info right-width">
                    <router-view></router-view>
                </div>
                <section>
                    <div class="main-list">

                    </div>
                </section>
            </div>
        </div>
    </div>
</template>
<script>
// import {post} from '../utils/http'
import MainHeader from '../common/header.vue'
export default {
    data() {
        return {
            infoList: [
                { 'name': 'editInfo', 'cnName': this.$t('editProfile.profile'), 'path': 'editInfo' },
                { 'name': 'editAvatar', 'cnName': this.$t('editProfile.avatar'), 'path': 'editAvatar' },
                { 'name': 'editPassword', 'cnName': this.$t('editProfile.password'), 'path': 'editPassword' },
                { 'name': 'bindEmail', 'cnName': this.$t('editProfile.email'), 'path': 'bindEmail' }
            ],
            nowIndex: 0,
            personalUser: []
        }
    },
    components: {
        MainHeader
    },
    methods: {
        routerGo(index) {
            this.$router.push(`/personalInfo/${this.infoList[index].path}`)
        }
    }
}
</script>
<style>
.breadcrumb {
    border-bottom: 1px solid #efefef;
    background: #F2F2F2;
}

.breadcrumb li:first-child a {
    color: #2DA2FF;
}
</style>
