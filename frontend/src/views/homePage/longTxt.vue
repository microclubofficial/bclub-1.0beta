<template>
  <div class="longTxt">
   <!-- 富文本 -->
     <form action="" class="long-text-container">
       <input type="hidden">
       <div class="expandingArea " id="textarea">
        <pre><span></span><br></pre>
        <textarea maxlength="50" @input="descInput" v-model="Longtitle" placeholder="请输入标题" ></textarea>
      </div>
      <span class="area-lth">{{remnant}}/50</span>
       <!--<textarea id="Longtitle" class="long-text-title" v-model="Longtitle" placeholder="请输入标题" @input='autoHeight()'></textarea>-->
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
      Longtitle: '',
      remnant: 50
    }
  },
  components: {
    LongEditor
  },
  mounted: function () {
    let areas = document.querySelectorAll('.expandingArea')
    let l = areas.length
    while (l--) {
      this.makeExpandingArea(areas[l])
    }
  },
  methods: {
    // 自适应高度
    makeExpandingArea (container) {
      let area = container.querySelector('textarea')
      let span = container.querySelector('span')
      if (area.addEventListener) {
        area.addEventListener('input', function () {
          span.textContent = area.value
        }, false)
        span.textContent = area.value
      } else if (area.attachEvent) {
      // IE8 compatibility
        area.attachEvent('onpropertychange', function () {
          span.innerText = area.value
        })
        span.innerText = area.value
      }
      container.className += 'active'
    },
    // 字数统计
    descInput () {
      let txtVal = this.Longtitle.length
      this.remnant = 50 - txtVal
    }
  }
}
</script>

<style>
.area-lth{
    color: #d4d4d4;
    float: right;
}
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

textarea, pre {
  margin: 0;
  padding: 0;
  outline: 0;
  border: 0;
}
.expandingArea {
  position: relative;
  background: #fff;
  min-height: 70px;
}
.expandingArea > textarea,
.expandingArea > pre {
  padding: 5px;
  background: transparent;
  font: 500 28px helvetica, arial, sans-serif;
  /* Make the text soft-wrap */
  white-space: pre-wrap;
  word-wrap: break-word;
  padding-top: 20px;
}
.expandingArea > textarea {
  /* The border-box box model is used to allow
   * padding whilst still keeping the overall width
   * at exactly that of the containing element.
   */
  -webkit-box-sizing: border-box;
     -moz-box-sizing: border-box;
      -ms-box-sizing: border-box;
          box-sizing: border-box;
  width: 100%;
  /* This height is used when JS is disabled */
  height: 70px;
}
.expandingArea.active > textarea {
  /* Hide any scrollbars */
  overflow: hidden;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  /* Remove WebKit user-resize widget */
  resize: none;
}
.expandingArea > pre {
  display: none;
}
.expandingArea.active > pre {
  display: block;
  /* Hide the text; just using it for sizing */
  visibility: hidden;
}
</style>
