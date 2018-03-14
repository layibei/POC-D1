import time
from models import Model


class Customer_info(Model):
    def __init__(self, form):
        self.customer_id=None
        self.customer_name=form.get('customer_name','')
        self.balance=form.get('balance','')
        self.status=form.get('status','')


class Customer_facility(Model):
    def __init__(self, form):
        self.customer_id = form.get('customer_id','')
        self.facility_id=form.get('facility_id','')
        self.facility_balance=form.get('facility_balance','')
        self.facility_status=form.get('facility_status','')

