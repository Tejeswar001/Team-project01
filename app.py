from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tejeswar2006@localhost/expenses_tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
    
class expenses(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(200),nullable=True)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Expenses %r>' % self.cid

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/totalexpenses/<int:id>',methods=['GET'])
def total_expenses(id):
    pass

@app.route('/signup')
def signup():
    return render_template('signup.html')
    

if __name__ == "__main__":
    app.run(debug=True)
