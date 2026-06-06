from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Vendor(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(200))

    email = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    gst_number = db.Column(db.String(50))

    category = db.Column(db.String(100))

    status = db.Column(db.String(50))

class RFQ(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200))

    description = db.Column(db.Text)

    quantity = db.Column(db.Integer)

    deadline = db.Column(db.Date)

    status = db.Column(db.String(50))

    created_by = db.Column(db.Integer)

class Quotation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(db.Integer)

    vendor_id = db.Column(db.Integer)

    price = db.Column(db.Float)

    delivery_days = db.Column(db.Integer)

    notes = db.Column(db.Text)

    status = db.Column(db.String(50))



class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))

    role = db.Column(db.String(50))


class Approval(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(db.Integer)

    quotation_id = db.Column(db.Integer)

    status = db.Column(db.String(50))

    remarks = db.Column(db.String(200))

class PurchaseOrder(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    po_number = db.Column(db.String(50))

    vendor_id = db.Column(db.Integer)

    quotation_id = db.Column(db.Integer)

    amount = db.Column(db.Float)

    status = db.Column(db.String(50))