from datetime import timedelta
import os


class BaseConfig:
  SECRET_KEY = "your secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False#设定是否追踪sql语句修改

  PERMANENT_SESSION_LIFETIME = timedelta(days=7)#长时间的session设置7天过期

  UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__),"media")#设置图片保存目录为media

  PER_PAGE_COUNT = 10#设置一页展示多少帖子，这里设置为10
class DevelopmentConfig(BaseConfig):
#设置数据库
  HOSTNAME = "127.0.0.1"
  PORT = 3306
  USERNAME = ""
  PASSWORD = ""
  DATABASE = ''
  DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
  SQLALCHEMY_DATABASE_URI = DB_URI
#设置邮箱发送
  MAIL_SERVER = "smtp.qq.com"
  MAIL_PORT = 587  # 465端口不行可以换587
  MAIL_USE_TLS = True#是否加密传输，如果是TLS加密，则是587端口，如果是设置为SSL加密，则端口应该设置为465
  # MAIL_DEBUG = False
  MAIL_USERNAME = ""
  MAIL_PASSWORD = ""
  MAIL_DEFAULT_SENDER = ""
#设置redis缓存
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_HOST = "127.0.0.1"
  CACHE_REDIS_PORT = 6379
# Celery配置
# 格式：redis://:password@hostname:port/db_number
  CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"#任务队列url地址
  CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"#任务结果存储方式
#头像保存，路径为UPLOAD_IMAGE_PATH+avatars
  AVATARS_SAVE_PATH = os.path.join(BaseConfig.UPLOAD_IMAGE_PATH,"avatars")
 


class TestingConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"


class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"
