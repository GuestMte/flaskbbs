from functools import wraps
from flask import redirect, url_for, g, abort, flash


def login_required(func):
  @wraps(func)
  def inner(*args, **kwargs):
    if not hasattr(g, "user"):
      return redirect(url_for("user.login"))#无登录对象，重定向到登录页面
    elif not g.user.is_active:
      flash("该用户已被禁用！")
      return redirect(url_for("user.login"))
    else:
      return func(*args, **kwargs)

  return inner


def permission_required(permission):
  def outer(func):
    @wraps(func)
    def inner(*args, **kwargs):
      if hasattr(g,"user") and g.user.has_permission(permission):#判断用户是否登录以及是否拥有此权限
        return func(*args, **kwargs)
      else:
        return abort(403)
    return inner
  return outer