from flask import Flask, request, render_template, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TeamHeadstarter'

# Initialize Firebase Admin SDK
cred = credentials.Certificate('expenses-management-bae32-firebase-adminsdk-lxpip-774d41f36d.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/totalexpenses/<string:id>', methods=['GET'])
def total_expenses(id):
    return render_template('index.html', user_id=id)

@app.route('/direct_signup')
def direct_signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        try:
            # Create the user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=f'{first_name} {last_name}'
            )

            # Store additional user data in Firestore
            db.collection('users').document(user.uid).set({
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'created_at': firestore.SERVER_TIMESTAMP
            })

            # Redirect to total expenses page
            return redirect(url_for('total_expenses', id=user.uid))
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'error')
            return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        # Authenticate the user using Firebase Authentication
        user = auth.get_user_by_email(email)

        # Verify user password (this is usually done on the client-side)
        # You should handle authentication on the client-side and send the token to the server
        # For this example, we'll assume that if the user exists, the login is successful

        # Redirect to total expenses page
        return redirect(url_for('total_expenses', id=user.uid))
    except Exception as e:
        flash(f'Invalid email or password: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
