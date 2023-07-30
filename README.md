# flaskbbs
对部分功能做了优化，原来项目有些功能有问题，比如图片显示不了，权限不好修改，等等

#celery启动命令
celery -A app.celery worker -P gevent -l info

#数据库同步命令
#ORM模块映射成表的三步，同步数据库,默认是执行app.py文件
1.flask db init 执行一次
2.flask db migrate 识别ORM模型的改变，生成迁移脚本
3.flask db upgrade 运行迁移脚本，同步到数据库中
