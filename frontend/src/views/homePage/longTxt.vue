<template>
  <div class="longTxt">
   <!-- 富文本 -->
     <form action="" class="long-text-container">
       <input type="hidden">
       <textarea id="Longtitle" class="long-text-title" v-model="Longtitle" placeholder="请输入标题" @input='autoHeight()'></textarea>
       <div class="long-text-editor">
         <LongEditor :title='Longtitle'></LongEditor>
       </div>
     </form>
  </div>
</template>

<script>
import LongEditor from '../homePage/longEditor/longTextEditor.vue'
export default{
  data: function () {
    return {
      Longtitle: ''
    }
  },
  components: {
    LongEditor
  },
  mounted: function () {
  },
  methods: {
    autoHeight () {
      let obj = document.getElementById('Longtitle')
      obj.style.height = obj.scrollHeight + 'px'
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
    margin-top: 20px;
    padding: 2px 0;
    border: 0;
    outline: 0;
    line-height: 1.2;
    resize: none;
    /* overflow: auto; */
    overflow: hidden;
    height: 50px;
}
.w-e-text::-webkit-scrollbar{
  background:snow;
}
.long-text-editor>div>.report{right: 0; bottom: 20px; padding: 0;}
.long-text-editor>div>.editor{width: 100%;}
</style>
