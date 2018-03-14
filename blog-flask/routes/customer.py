from flask import (
render_template,   # html页面渲染模板
request,  #处理请求
redirect,# 重定向页面
url_for, #动态路由
Blueprint, #蓝图
)

from models.customer import (
Customer_info,
Customer_facility,
)

'''
from models.cust_db import (
Customer_info_db,
Customer_facility_db,
)
'''

main = Blueprint('customer',__name__)

@main.route("/")
def index():
    all_customer = Customer_info.all()
    return render_template("customer_index.html",customers=all_customer)

@main.route("/<int:customer_id>",methods =["GET"])
def view(customer_id):
        all_fcty = Customer_facility.find_all(customer_id=customer_id)
        all_customer = Customer_info.all()
        return render_template("customer_index.html",fctys=all_fcty,customers=all_customer)

@main.route("/cust_db")
def show_all():
    all_customer = Customer_info_db.all()
    return render_template("customer_index.html", customers=all_customer)