from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf import CSRFProtect
from flask_avatars import Avatars

db=SQLAlchemy()#数据库服务
mail=Mail()#邮箱服务
cache=Cache()#缓存服务
csrf = CSRFProtect()#防csrf攻击
avatars=Avatars()#随机生成头像