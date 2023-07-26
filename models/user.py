from exts import db
from datetime import datetime
from shortuuid import uuid
from enum import Enum
from werkzeug.security import generate_password_hash,check_password_hash
from shortuuid import uuid



#权限枚举类型
class PermissionEnum(Enum):
  BOARD = "板块"
  POST = "帖子"
  COMMENT = "评论"
  FRONT_USER = "前台用户"
  CMS_USER = "后台用户"

#权限表
class PermissionModel(db.Model):
  __tablename__ = "permission"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.Enum(PermissionEnum), nullable=False, unique=True)#权限名称，是枚举值，只能出现枚举里面的名称

#设置中间表，关联RoleModel和PermissionModel之间的多对多关系
role_permission_table = db.Table(
  "role_permission_table",
  db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
  db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"))
)

#角色表
class RoleModel(db.Model):
  __tablename__ = 'role'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)#角色名
  desc = db.Column(db.String(200), nullable=True)#备注
  create_time = db.Column(db.DateTime, default=datetime.now)
#添加关系模型
  permissions = db.relationship("PermissionModel", secondary=role_permission_table, backref="roles")



#用户表，这边id用uuid里面的字符串来表示，以避免自增的id不安全，容易被发现具体用户个数
class UserModel(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.String(100), primary_key=True, default=uuid)#默认使用uuid
  username = db.Column(db.String(50), nullable=False,unique=True)#用户名
  _password = db.Column(db.String(200), nullable=False)#密码，前面加_主要是命名习惯
  email = db.Column(db.String(50), nullable=False, unique=True)#邮箱
  avatar = db.Column(db.String(100))#头像，存储图片在服务器中保存的路径
  signature = db.Column(db.String(100))#签名
  join_time = db.Column(db.DateTime, default=datetime.now)#加入时间
  is_staff = db.Column(db.Boolean, default=False)#是否是员工，员工可进入后台
  is_active = db.Column(db.Boolean,default=True)#是否可用，用来限制登录

  # 外键
  role_id = db.Column(db.Integer, db.ForeignKey("role.id"))#外键，引用role的id字段
  role = db.relationship("RoleModel", backref="users")#关系属性

#密码管理，加密储存和密码验证
  def __init__(self, *args, **kwargs):#接受任意数量的位置参数和关键字参数
    if "password" in kwargs:#判断关键字参数中是否包含 "password"
      self.password = kwargs.get('password')#如果包含 "password"，就将其值赋给用户模型类的密码属性。
      kwargs.pop("password")#从关键字参数中删除 "password"，因为父类函数可能不处理这个参数
    super(UserModel, self).__init__(*args, **kwargs)#将未处理的参数传给父类

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, raw_password):
    self._password = generate_password_hash(raw_password)#密码加密

  def check_password(self, raw_password):
    result = check_password_hash(self.password, raw_password)#密码对比
    return result

  def has_permission(self, permission):
    return permission in [permission.name for permission in self.role.permissions]#权限判断是否符合





