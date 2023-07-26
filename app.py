from flask import Flask
import config
from exts import db,mail,cache,csrf,avatars
from models.user import RoleModel,PermissionEnum,PermissionModel
from blueprints.cms import  bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
from flask_migrate import Migrate
from bbs_celery import make_celery
from models import user
import filters
import click
from flask_wtf import CSRFProtect
import commands
import hooks




app = Flask(__name__)

#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
migrate=Migrate(app,db)
#随机生成头像
avatars.init_app(app)
#CSRF保护
#CSRFProtect(app)
csrf.init_app(app)
#register.html 中可以使用 csrf_token() 生成一个csrf令牌
#构建celery,异步框架
celery=make_celery(app)


#注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)
app.register_blueprint(media_bp)




#添加命令,分别为create-permission和create-role，主要是将每个权限添加到数据库中，以及每个角色有哪些权限关联好，添加到数据库中
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-test-front")(commands.create_test_user)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)
#添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

# 添加模板过滤器
app.template_filter("email_hash")(filters.email_hash)
# #添加命令行命令
# @app.cli.command("create-permission")
# def create_permission():
#     for permission_name in dir(PermissionEnum):#dir(PermissionEnum) 函数获取 PermissionEnum 中定义的所有属性名
#         if permission_name.startswith("__"):#使用 if permission_name.startswith() 这个条件判断语句来跳过__为前缀的属性如__class__，__tablename__
#             continue
#         permission=PermissionModel(name=getattr(PermissionEnum,permission_name))
#         db.session.add(permission)
#     db.session.commit()
#     click.echo("权限添加成功")






if __name__ == '__main__':
    app.run()
