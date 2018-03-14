from app_db import db


class Customer_info_db(db.Model):

    __tablename__ = 's_cust'
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), unique=True)
    balance = db.Column(db.String(320), unique=True)
    status = db.Column(db.String(32), nullable=False)

    def __init__(self, form):
        self.customer_id=None
        self.customer_name=form.get('customer_name','')
        self.balance=form.get('balance','')
        self.status=form.get('status','')

class Customer_facility_db(db.Model):
    __tablename__ = 's_fcty'
    customer_id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.String(80), unique=True)
    facility_balance = db.Column(db.String(320), unique=True)
    facility_status = db.Column(db.String(32), nullable=False)

    def __init__(self, form):
        self.customer_id = form.get('customer_id','')
        self.facility_id=form.get('facility_id','')
        self.facility_balance=form.get('facility_balance','')
        self.facility_status=form.get('facility_status','')

