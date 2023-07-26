from flask import Blueprint, request, render_template, jsonify, current_app, url_for, send_from_directory, g, abort, redirect,flash
from werkzeug.utils import secure_filename
import os
from models.post import PostModel, BoardModel, CommentModel
from exts import csrf, db
from forms.post import PublicPostForm, PublicCommentForm
from utils import restful
from decorators import login_required
from flask_paginate import Pagination

bp=Blueprint("front",__name__,url_prefix="")


@bp.route("/")
def index():
 # posts=PostModel.query.all()

  boards = BoardModel.query.filter_by(is_active=True).all()

  # 获取页码参数，默认是1，即从第一页开始
  page = request.args.get("page", type=int, default=1)
  # 获取板块参数
  board_id = request.args.get("board_id", type=int, default=0)

  # 当前page下的起始位置，因为页码默认是1，所有一开始是从id为1开始
  start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
  # 当前page下的结束位置
  end = start + current_app.config.get("PER_PAGE_COUNT")

  # 查询对象
  query_obj = PostModel.query.filter_by(is_active=True).order_by(PostModel.create_time.desc())
  # 过滤帖子
  if board_id:
    query_obj = query_obj.filter_by(board_id=board_id)
  # 总共有多少帖子
  total = query_obj.count()

  # 当前page下id范围的帖子列表
  posts = query_obj.slice(start, end)

  # 分页对象，bs_version=4代表使用 Bootstrap 4 样式的分页导航栏，page=page表示当前页码，即需要在分页导航栏中高亮显示的页码
  # total=total 表示总记录数，即需要分页的记录总数
  # outer_window=0 表示在分页导航栏中显示的页码范围，即当前页码左右各显示几个页码（不包括第一页和最后一页）。这里设置为 0，表示只显示当前页码和第一页、最后一页
  # inner_window=2 表示在分页导航栏中显示的页码范围，即当前页码左右各多少个页码。这里设置为 2，表示当前页码左右各显示两个页码。
  # alignment="center" 表示分页导航栏的对齐方式，这里设置为居中对齐。
  pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment="center")
  context = {
    "posts": posts,
    "boards": boards,
    "pagination": pagination,
    "current_board": board_id
  }
  current_app.logger.info("index页面被请求了")
  return render_template("front/index.html", **context)


#发布帖子页面
@bp.route("/post/public", methods=['GET', 'POST'])
@login_required#添加修饰器，检测是否登录，登录才能发布帖子
def public_post():
  if request.method == 'GET':
    boards = BoardModel.query.all()#获取所有板块
    return render_template("front/public_post.html", boards=boards)
  else:
    form = PublicPostForm(request.form)
    if form.validate():
      title = form.title.data
      content = form.content.data
      board_id = form.board_id.data
      post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
      db.session.add(post)
      db.session.commit()
      return restful.ok()
    else:
      message = form.messages[0]
      return restful.params_error(message=message)



@bp.route('/image/<path:filename>')
def uploaded_image(filename):
  path = current_app.config.get("UPLOAD_IMAGE_PATH")
  return send_from_directory(path, filename)

# @bp.route('/media/<path:filename>')
# def media_image(filename):
#   path = current_app.config.get("UPLOAD_IMAGE_PATH")
#   return send_from_directory(path, filename)

@bp.post("/upload/image")
@csrf.exempt#取消CSRF保护，图片上传用不到
@login_required
def upload_image():
  f = request.files.get('image')
  extension = f.filename.split('.')[-1].lower()#获取上传文件的扩展名，并将其转换为小写字母
  if extension not in ['jpg', 'gif', 'png', 'jpeg']:#检查是否为图片文件
    return jsonify({
      "errno": 400,
      "data": []
    })
  filename = secure_filename(f.filename)#secure_filename安全保存图片名字
  # print(filename)
  # print(current_app.config.get("UPLOAD_IMAGE_PATH"))
  f.save(os.path.join(current_app.config.get("UPLOAD_IMAGE_PATH"),filename))#将上传的文件保存到服务器的文件系统中
  url = url_for('front.uploaded_image', filename=filename)
  return jsonify({
    "errno": 0,
    "data": [{
      "url": url,
      "alt": "",
      "href": ""
    }]
  })

#动态加载帖子
@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
  post = PostModel.query.get(post_id)
  if not post.is_active:
    return abort(404)
  post.read_count += 1#阅读数加1
  db.session.commit()
  return render_template("front/post_detail.html",post=post)


@bp.post("/post/<int:post_id>/comment")
@login_required
def public_comment(post_id):
  form = PublicCommentForm(request.form)
  if form.validate():
    content = form.content.data
    comment = CommentModel(content=content, post_id=post_id, author=g.user)
    db.session.add(comment)
    db.session.commit()
  else:
    for message in form.messages:
      flash(message)

  return redirect(url_for("front.post_detail", post_id=post_id))


@bp.route("/search")
def search():
    # /search？q=flask
    # /search/<q>
    # post,request.form
    q=request.args.get("q")#获取参数 q
    questions=PostModel.query.filter(PostModel.title.contains(q)).all()#过滤查找,把名字中包含关键字q的都搜索出来
    return render_template("front/index1.html",posts=questions)