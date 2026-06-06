from flask import Flask, render_template, request , redirect , session
from models import db, User

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

    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)