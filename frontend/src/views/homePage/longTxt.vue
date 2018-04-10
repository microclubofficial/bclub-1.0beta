<template>
  <div class="longTxt">
   <!-- 富文本 -->
     <form action="" class="long-text-container">
       <input type="hidden">
       <textarea id="Logintitle" class="long-text-title" style="min-height:37px;" placeholder="请输入标题" oninput="autoHeight(this)"></textarea>
       <div class="long-text-editor">
         <TalkEditor></TalkEditor>
       </div>
     </form>
  </div>
</template>

<script>
import TalkEditor from '../homePage/longEditor/longTextEditor.vue'
export default{
  data: function () {
    return {

    }
  },
  components: {
    TalkEditor
  },
  mounted: function () {
    let ele = document.getElementById('Logintitle')
    this.autoHeight(ele)
  },
  methods: {
    autoHeight (o) {
      o.style.height = o.scrollTop + o.scrollHeight + 'px'
    }
  }
}
</script>

<style>
.longTxt{background: #fff;}
.long-text-container {
    width: 800px;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    overflow: hidden;
    height: 100%;
    /* margin-bottom: 20px; */
    padding-bottom: 50px;
}
.long-text-title {
    width: 100%;
    font-size: 28px;
    margin: 21px 0;
    padding: 2px 0;
    border: 0;
    outline: 0;
    line-height: 1.2;
    resize: none;
    /* overflow: auto; */
    overflow: visible;
}
.w-e-text::-webkit-scrollbar{
  background:snow;
}
.long-text-editor>div>.report{float: right;}
</style>
