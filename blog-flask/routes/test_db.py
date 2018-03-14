from flask import (
render_template,   # html页面渲染模板
    #处理请求
    # 重定向页面
    #动态路由
Blueprint, #蓝图
)

from models.cust_db import (
    Customer_info_db,
)

main = Blueprint ('cust_db',__name__)

@main.route("/")
def index():
    customers = Customer_info_db.query.all()

    return render_template('customer_index.html', customers=customers)
