from flask import Flask, render_template, request , redirect , session
from models import db, User , Vendor , RFQ , Quotation , Approval
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'vendorbridge123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendorbridge.db'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        user = User(
            name=name,
            email=email,
            password=password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return "User Registered Successfully"

    return render_template('signup.html')


@app.route('/users')
def users():

    all_users = User.query.all()

    result = ""

    for user in all_users:
        result += f"{user.name} | {user.email} | {user.role}<br>"

    return result


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session['user_id'] = user.id
            session['role'] = user.role

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    total_vendors = Vendor.query.count()
    total_rfqs = RFQ.query.count()
    total_quotes = Quotation.query.count()

    return render_template(
        'dashboard.html',
        total_vendors=total_vendors,
        total_rfqs=total_rfqs,
        total_quotes=total_quotes
    )



@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():

    if request.method == 'POST':

        vendor = Vendor(
            company_name=request.form['company_name'],
            email=request.form['email'],
            phone=request.form['phone'],
            gst_number=request.form['gst_number'],
            category=request.form['category'],
            status='Active'
        )

        db.session.add(vendor)
        db.session.commit()

        return "Vendor Added Successfully"

    return render_template('add_vendor.html')


@app.route('/vendors')
def vendors():

    all_vendors = Vendor.query.all()

    return render_template(
        'vendors.html',
        vendors=all_vendors
    )

@app.route('/create_rfq', methods=['GET', 'POST'])
def create_rfq():

    if request.method == 'POST':

        rfq = RFQ(
            title=request.form['title'],
            description=request.form['description'],
            quantity=request.form['quantity'],
            deadline=datetime.strptime(
                request.form['deadline'],
                '%Y-%m-%d'
            ).date(),
            status='Open',
            created_by=1
        )

        db.session.add(rfq)
        db.session.commit()

        return "RFQ Created Successfully"

    return render_template('create_rfq.html')

@app.route('/rfqs')
def rfqs():

    all_rfqs = RFQ.query.all()

    return render_template(
        'rfqs.html',
        rfqs=all_rfqs
    )


@app.route('/submit_quotation/<int:rfq_id>',
           methods=['GET', 'POST'])
def submit_quotation(rfq_id):

    if request.method == 'POST':

        quotation = Quotation(
            rfq_id=rfq_id,
            vendor_id=request.form['vendor_id'],
            price=request.form['price'],
            delivery_days=request.form['delivery_days'],
            notes=request.form['notes'],
            status='Submitted'
        )

        db.session.add(quotation)
        db.session.commit()

        return "Quotation Submitted Successfully"

    vendors = Vendor.query.all()

    return render_template(
        'submit_quotation.html',
        vendors=vendors
        )

@app.route('/quotations')
def quotations():

    all_quotes = Quotation.query.all()

    return render_template(
        'quotations.html',
        quotations=all_quotes
    )
@app.route('/compare/<int:rfq_id>')
def compare(rfq_id):

    quotations = Quotation.query.filter_by(
        rfq_id=rfq_id
    ).all()
    recommended = min(
        quotations,
        key=lambda x: x.price
    )
    vendors = Vendor.query.all()

    vendor_map = {}

    for v in vendors:
        vendor_map[v.id] = v.company_name

    lowest_price = None

    if quotations:
        lowest_price = min(q.price for q in quotations)

    return render_template(
        'compare.html',
        quotations=quotations,
        lowest_price=lowest_price,
        vendor_map=vendor_map ,
        recommended=recommended
    )


@app.route('/approve/<int:quotation_id>')
def approve(quotation_id):

    approval = Approval(
        rfq_id=1,
        quotation_id=quotation_id,
        status="Approved",
        remarks="Best quotation selected"
    )

    db.session.add(approval)
    db.session.commit()

    return "Quotation Approved Successfully"


@app.route('/approvals')
def approvals():

    all_approvals = Approval.query.all()

    return render_template(
        'approvals.html',
        approvals=all_approvals
    )

@app.route('/generate_po/<int:quotation_id>')
def generate_po(quotation_id):

    quotation = Quotation.query.get(quotation_id)

    po = PurchaseOrder(
        po_number=f"PO-{quotation.id}",
        vendor_id=quotation.vendor_id,
        quotation_id=quotation.id,
        amount=quotation.price,
        status="Generated"
    )

    db.session.add(po)
    db.session.commit()

    return "Purchase Order Generated"

if __name__ == "__main__":
    app.run(debug=True)