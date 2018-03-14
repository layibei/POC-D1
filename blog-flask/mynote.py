# 做了新的customer页面
# 包括customer route  --> 路由页面，结合app.blueprint
# customer model  --〉数据模型
# customer json data  --〉数据文件
# customer index html  --〉页面模板
#
# 下一步
# 1 css js 美化页面--〉前端教程
# 2 增加其他功能
# 2.1点击customer 展示 facility  --> blog案例
# 2.2customer 搜索
# 2.3连接数据库

'''
新做了 messge
需要注意
1 config 要 注入数据库配置，不注入的话它默认连 sqllite，会有 表找不到的报错。
2 app 注入 SQLAlchemy

下一步
做url for --罗列详细信息
拆分代码模块  -- 方便后续扩展
css js 美化页面 bootstrasp框架 ？？
做多线程
写log


项目结构
    |-flasky
      |-app/    Flask 程序一般都保存在名为 app 的程序包中
        |-templates/    templates 和 static 文件夹是程序包的一部分
        |-static/
        |-main/ 程序包中创建了一个子包，用于保存蓝本。/main/__init__.py脚本的末尾导入views.py & errors.py,避免循环导入依赖
        |-__init__.py   程序工厂函数 create_app()，注册蓝本
        |-errors.py 错误处理路由. 注册程序全局的错误处理程序，必须使用 app_errorhandler
        |-forms.py  表单对象
        |-views.py  路由。蓝本中的全部端点会加上一个命名空间，如 url_for('main.index')
      |-__init__.py
      |-email.py    电子邮件支持函数
      |-models.py   数据库模型
      |-migrations/ 数据库迁移脚本
      |-tests/  单元测试
        |-__init__.py  文件可以为空，因为 unittest 包会扫描所有模块并查找测试
        |-test*.py
      |-venv/ 虚拟环境
      |-requirements.txt    列出了所有依赖包，便于在其他电脑中重新生成相同的虚拟环境
      |-config.py   存储配置。开发、测试和生产环境要使用不同的数据库
      |-manage.py   用于启动程序以及其他的程序任务


拆分代码模块化 --
1 路由
2 数据model
3 html template
4 app注册路由蓝图


'''