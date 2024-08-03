from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TeamHeadstarter'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tejeswar001@localhost/expenses_tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    
class users(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200),nullable=False)
    last_name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<users %r>' % self.cid

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/totalexpenses/<int:id>',methods=['GET'])
def total_expenses(id):
    return render_template('index.html')

@app.route('/direct_signup')
def direct_signup():
    return render_template('signup.html')
    
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        try:
            new_user = users(first_name=first_name,last_name=last_name,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('total_expenses',id=new_user.id)) 
        except:
            db.session.rollback()  # Rollback the session in case of error
            redirect(url_for('index'))# redirecting to login page 

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = users.query.filter_by(email=email).first()
    if user:
        if user.password == password:
            return redirect(url_for('total_expenses', id=user.cid))
        else:
            flash('Enter a valid Password!!','error')
            return redirect(url_for('index'))
    else:
        flash('Email not found. Sign up.','error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)