from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
)

from flask_wtf import FlaskForm,CsrfProtect
#如果输入的是字符串那么就用StringField,如果是整数那么就用IntegerField
from wtforms import (
     StringField,
     IntegerField,
     SubmitField,
     )
#验证方式
from wtforms.validators import     (
     Length,
     EqualTo,
     InputRequired,
     )

import time
import json
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# 先要初始化一个 Flask 实例
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
# message_list 用来存储所有的 message
message_list = []

# 用 log 函数把所有输出写入到文件，这样就能很方便地掌控全局了
# 即便你关掉程序，也能再次打开来查看，这就是个时光机
def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    # 中文 windows 平台默认打开的文件编码是 gbk 所以需要指定一下
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        # 通过 file 参数可以把输出写入到文件 f 中
        # 需要注意的是 **kwargs 必须是最后一个参数
        print(dt, *args, file=f, **kwargs)

class User(db.Model):
    __tablename__ = 's_admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class RequestForm(FlaskForm):
    username = StringField(validators=[Length(min=3,max=10,message=u"用户名长度有问题")])
    password = StringField(validators=[Length(min=6,max=20)])
    age = IntegerField(validators=[InputRequired()])

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[InputRequired()])
    age = StringField('What is your age?', validators=[InputRequired()])
    birthday = StringField('What is your birthday?', validators=[InputRequired()])
    cellphone = StringField('What is your cellphone?', validators=[InputRequired()])
    submit = SubmitField('Submit')


# 定义路由和路由处理函数的方式如下
# ==========================
# 用 app.route 函数定义路由，参数是一个 path 路径
# 下一行紧跟着的函数是处理这个请求的函数
# @ 是一个叫装饰器的东西, 现在无必要知道具体的原理, 只要用它就好了
# 注意 methods 参数是一个 list，它规定了这个函数能接受的 HTTP 方法
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello !!!!'

@app.route('/show')
def message_show():
    #Customer_all=User.all()
    #id=User.id
    #return render_template('message_index.html', Customers=Customer_all)
    #return 'show test ok'

    customers = User.query.all()

    return render_template('show_test.html', customers=customers)

@app.route('/show_2')
def message_show2():
    #Customer_all=User.all()
    #id=User.id
    #return render_template('message_index.html', Customers=Customer_all)
    #return 'show test ok'

    customers = User.query.all()
    #data = [{title:'book1',author:'tom'},{title:'book2',author:'tom'}]
    #data = ['1', '2']
    #data = [
    #      {'name': 'Fruit', 'items': ['Apple', 'Orange', 'Banana']},
    #      {'name': 'Vegetables', 'items': ['Celery', 'Corn', 'Spinach']}
    # ]

    # for cu_json in customers:
    #     a=cu_json.__dict__
    #     #print('1111'+format(a))
    #     #dictret = dict(cu_json.__dict__)
    #     a.pop('_sa_instance_state', None)
    #     print('2222' + format(a))
    #print(format(type(customers)))  --> <class 'list'>
    a = json.loads(customers)
    return render_template('show_test2.html', data=a)

@app.route('/customer_detail', methods=['GET', 'POST'])
def customer_detail():
    name = None
    form = NameForm()
    #customers = User.query.all()

    if request.method == "GET":
        return render_template('customer_detail.html', form=form)

    else:
        name = form.name.data
        age = form.age.data
        birthday = form.birthday.data
        cellphone = form.cellphone.data

        print(name)
        print(age)
        print(birthday)
        print(cellphone)
        me = User()
        me.id = '0001'
        me.username = 'Jen'
        me.password = '********'
        me.email = 'abc@163.com'
        db.session.add(me)
        db.session.commit()
        test_a=User.query.filter_by(username='Jen').first()
        print(test_a.username)
        print(test_a.email)

        return render_template('customer_detail.html', form=form, name=name,age=age,birthday=birthday,cellphone=cellphone)




# 这是访问 /message 的请求
# methods 默认是 ['GET'] 因此可以省略
@app.route('/message')
def message_view():
    # 打印请求的方法 GET 或者 POST
    log('请求方法', request.method)


    # request.args 是 flask 保存 URL 中的参数的属性
    # 访问 http://127.0.0.1:2000/message?a=1
    # 会打印如下输出 (ImmutableMultiDict 是 flask 的自定义类型, 意思是不可以改变的字典)
    # request ImmutableMultiDict([('a', '1')])
    log('request, query 参数', request.args)

    # render_template 是一个 flask 内置函数
    # 它的作业是读取并返回 templates 文件夹中的模板文件
    # messages 是传给模板的参数，这样就能在模板中使用这个变量了
    return render_template('message_index.html', messages=message_list)


# 这个路由函数只支持 POST 方法
@app.route('/message/add', methods=['POST'])
def message_add():
    # 打印请求的方法 GET 或者 POST
    log('message_add 请求方法', request.method)

    # request.form 是 flask 保存 POST 请求的表单数据的属性
    log('request, POST 的 form 表单数据', request.form)
    # 把数据生成一个 dict 存到 message_list 中去
    msg = {
        'content': request.form.get('msg_post', ''),
    }
    message_list.append(msg)

    # 这和我们写过的函数是一样的
    return redirect('/message')
    # 一般来说，我们会用 url_for 生成路由，如下
    # 注意, url_for 参数是路由函数的名字（格式为字符串）
    # return redirect(url_for('message_view'))


# 运行服务器
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    app.run(**config)
    # app.run() 开始运行服务器
    # 所以你访问下面的网址就可以打开网站了
    # http://127.0.0.1:2000/
