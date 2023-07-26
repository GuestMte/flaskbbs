$(function (){
  //  创建一个富文本编辑器，wangEditor编辑器对象，并将其绑定到ID为editor的元素上
  var editor = new window.wangEditor("#editor");
  //配置wangEditor编辑器的图片上传功能。uploadImgServer属性指定了图片上传的服务器地址
  editor.config.uploadImgServer  = "/upload/image";
  //uploadFileName属性指定了上传图片的文件名
  editor.config.uploadFileName = "image";
  editor.create();


  // 提交按钮点击事件
  $("#submit-btn").click(function (event) {
      event.preventDefault();//阻止表单的默认提交行为，让JavaScript代码来处理表单的提交操作，否则表单数据无法通过AJAX方式发送到服务器。

      var title = $("input[name='title']").val();
      var board_id = $("select[name='board_id']").val();
      //获取编辑器中html内容
      var content = editor.txt.html();

      zlajax.post({
        url: "/post/public",
        data: {title,board_id,content}
      }).done(function(data){
          setTimeout(function (){
              window.location = "/";
          },2000);//如果请求成功，代码会使用setTimeout方法延迟2秒钟，并在延迟后将浏览器重定向到主页。如果请求失败，代码会弹出一个错误提示框，显示错误信息
      }).fail(function(error){
          alert(error.message);
      });
  });
});