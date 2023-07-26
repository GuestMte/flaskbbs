from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, session, g, send_from_directory
from exts import cache,db
import random
import string
from utils import restful
from forms.user import RegisterForm, LoginForm, EditProfileForm
from models.user import UserModel
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from decorators import login_required
import os

bp=Blueprint("user",__name__,url_prefix="/user")


@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)#验证表单是否有效
        if form.validate():#如果有效，写入数据库
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))#回到登录页面
        else:
            for message in form.messages:
                flash(message)#用flash方式显示错误信息
            return redirect(url_for("user.register"))#如果无效，报告错误信息，返回到注册页面


@bp.route("/mail/captcha")
def mail_captcha():
    #测试视图函数是否正常执行
    try:
        email = request.args.get(("mail"))
        # 验证码
        # string.digits*4 0123456789012345678901234567890123456789
        # source = string.digits + string.ascii_letters  # 数字加大小26字母
        # source = source * 4
        # captacha = random.sample(source, 6)  # 返回一个列表
        # # 列表变成字符串
        # captacha = "".join(captacha)
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        captacha = "".join(random.sample(digits, 4))
        subject = "验证码"
        body = f"您的验证码是:{captacha},请不要告诉别人"
        #message = Message(subject="验证码", recipients=[email], body=f"您的验证码是:{captacha},请不要告诉别人")
        current_app.celery.send_task("send_mail",(email,subject,body))#使用Celery任务队列来异步发送电子邮件
        cache.set(email,captacha,timeout=100)#将email放置在缓存中，缓存过期时间为100秒
        return restful.ok()
    except Exception as e:
        print(e)
        return restful.server_error()

@bp.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template("front/login.html")
  else:
    form = LoginForm(request.form)
    if form.validate():
      email = form.email.data
      password = form.password.data
      remember = form.remember.data
      user = UserModel.query.filter_by(email=email).first()
      if user and user.check_password(password):
        if not user.is_active:
          flash("该用户已被禁用！")
          return redirect(url_for("user.login"))
        session['user_id'] = user.id#id存储在session中，因为是加密的
        if remember:
          session.permanent = True#remember表示用户是否勾选了“记住我”的选项。如果用户勾选了“记住我”，则会话数据会被保存为永久会话，否则为临时会话
        return redirect("/")
      else:
        flash("邮箱或者密码错误！")
        return redirect(url_for("user.login"))
    else:
      for message in form.messages:
        flash(message)
      return render_template("front/login.html")


@bp.get('/logout')
def logout():
  session.clear()
  return redirect("/")


@bp.get("/profile/<string:user_id>")
def profile(user_id):
  user = UserModel.query.get(user_id)
  is_mine = False
  if hasattr(g,"user") and g.user.id == user_id:
    is_mine = True
  context = {
    "user": user,
    "is_mine": is_mine
  }
  #print(user)
  return render_template("front/profile.html",**context)


@bp.post("/profile/edit")
@login_required
def edit_profile():
  form = EditProfileForm(CombinedMultiDict([request.form,request.files]))
  if form.validate():
    username = form.username.data
    avatar = form.avatar.data
    signature = form.signature.data

    # 如果上传了头像
    if avatar:
      # 生成安全的文件名
      filename = secure_filename(avatar.filename)
      # print(filename)
      # 拼接头像存储路径
      avatar_path = os.path.join(current_app.config.get("AVATARS_SAVE_PATH"), filename)
      # 保存文件
      avatar.save(avatar_path)
      # 设置头像的url
      filepath= os.path.join("avatars",filename)
      #设置图片地址传到数据库中
      g.user.avatar = filepath.replace(os.path.sep, "/")
      # print(g.user.avatar)
    g.user.username = username
    g.user.signature = signature
    db.session.commit()
    return redirect(url_for("user.profile",user_id=g.user.id))
  else:
    for message in form.messages:
      flash(message)
    return redirect(url_for("user.profile",user_id=g.user.id))




