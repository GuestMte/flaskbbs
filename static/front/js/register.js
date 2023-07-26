function captchaBtnClickEvent(event) {
  event.preventDefault();
  var $this = $(this);

  // 获取邮箱
  var email = $("input[name='email']").val();
  var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
  if (!email || !reg.test(email)) {
    alert("请输入正确格式的邮箱！");
    return;
  }

  zlajax.get({
    url: "/user/mail/captcha?mail=" + email
  }).done(function (result) {
    alert("验证码发送成功！");
  }).fail(function (error) {
    alert(error.message);
  })
}

$(function () {
  $('#captcha-btn').on("click",function(event) {//为id为captcha-btn的按钮添加了点击事件
    event.preventDefault();//阻止点击事件，防止点击发送验证码后，直接提交了表单信息，这样可以确保在AJAX请求完成之前，不会发生任何不必要的行为
    // 获取邮箱
    var email = $("input[name='email']").val();
    zlajax.get({//发送一个自定义的get请求
      url: "/user/mail/captcha?mail=" + email
    }).done(function (result) {
      alert("验证码发送成功！");
    }).fail(function (error) {
      alert(error.message);
    })
  });
});