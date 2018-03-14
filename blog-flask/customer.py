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
    SelectField,
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


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

message_list = []


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



class NameForm(FlaskForm):
    id = StringField('What is your id?', validators=[InputRequired()])
    username = StringField('What is your username?', validators=[InputRequired()])
    email = StringField('What is your email?', validators=[InputRequired()])
    password = StringField('What is your password?', validators=[InputRequired()])
    #name_list = SelectField('What is your category type', choices = [(2, '2'), (5, '5')])
    submit = SubmitField('Submit')


    # def __init__(self, *args, **kwargs):
    #     # self.name_list.choices = [(obj.id, obj.name) for obj in User.query.order_by('name')]
    #     print('test ok')
    #     #self.name_list.choices = [ '1','2','3' ]

@app.route('/b_test', methods=['GET'])
def b_test():
    return render_template('index.html')



@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/show')
def message_show():

    customers = User.query.all()

    return render_template('show_test.html', customers=customers)

@app.route('/show_2')
def message_show2():

    return render_template('show_test2.html')

@app.route('/customer_detail', methods=['GET', 'POST'])
def customer_detail():
    name = None
    form = NameForm()
    customers = User.query.all()

    if request.method == "GET":
        return render_template('customer_detail.html', form=form,customers=customers)

    else:
        # form data handle
        id = form.id.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        # insert to db
        me = User()
        me.id = id
        # # me.username = 'Jen'
        me.username = username
        me.password = password
        me.email = email
        db.session.add(me)
        db.session.commit()
        test_a = User.query.filter_by(username=username).first()
        print(test_a.username)
        print(test_a.email)

        return render_template('customer_detail.html', form=form, id=id,username=username,password=password,email=email,customers=customers)




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

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    app.run(**config)

