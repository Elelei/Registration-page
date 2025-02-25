from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['contact_app']
users_collection = db['users']
contacts_collection = db['contacts']

# Flask-Mail configuration (for Gmail example)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'manuellelei750@gmail.com')  # Use environment variable
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'qqwr cvuv jwro oyqm')  # Use environment variable
mail = Mail(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email already exists
        if users_collection.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('signup'))
        if users_collection.find_one({'email': email}):
            flash('Email already exists')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        users_collection.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash('Registration successful! Please log in.')
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users_collection.find_one({'username': username})

    if user and check_password_hash(user['password'], password):
        flash('Login successful!')
        return redirect(url_for('contact_form'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = users_collection.find_one({'email': email})
        if user:
            # Generate a reset token
            reset_token = secrets.token_urlsafe(32)
            reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
            users_collection.update_one({'email': email}, {'$set': {'reset_token': reset_token, 'reset_token_expiry': reset_token_expiry}})
            
            try:
                # Send reset password email
                msg = Message('Password Reset', sender='manuellelei750@gmail.com', recipients=[email])
                reset_link = url_for('reset_password', token=reset_token, _external=True)
                msg.body = f'Please click the link to reset your password: {reset_link}'
                mail.send(msg)
                flash('Password reset link sent to your email')
            except Exception as e:
                flash(f'Failed to send email: {str(e)}')
        else:
            flash('Email not found')
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = users_collection.find_one({'reset_token': token})
    if user and user['reset_token_expiry'] > datetime.utcnow():
        if request.method == 'POST':
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if new_password == confirm_password:
                # Hash the new password
                hashed_password = generate_password_hash(new_password)
                users_collection.update_one({'reset_token': token}, {'$set': {'password': hashed_password}, '$unset': {'reset_token': '', 'reset_token_expiry': ''}})
                flash('Password reset successful! Please log in.')
                return redirect(url_for('index'))
            else:
                flash('Passwords do not match')
        return render_template('reset_password.html', token=token)
    else:
        flash('Invalid or expired reset link')
        return redirect(url_for('index'))

@app.route('/contact_form', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        reg_number = request.form['reg_number']
        contacts_collection.insert_one({
            'mobile': mobile,
            'email': email,
            'address': address,
            'reg_number': reg_number
        })
        flash('Contact details saved successfully')
        return redirect(url_for('contact_form'))
    return render_template('contact_form.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        contact = contacts_collection.find_one({'reg_number': reg_number})
        if contact:
            return render_template('search_results.html', contact=contact)
        else:
            flash('No contact found with that registration number')
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=False)  # Disable debug mode