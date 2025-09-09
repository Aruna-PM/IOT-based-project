from flask import Flask, render_template, request, redirect, session
import mysql.connector
#python -m pip install mysql-connector-python

app = Flask(__name__)

import secrets
secret_key = secrets.token_hex(24)
print(secret_key)
app.secret_key = secret_key

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="reward_system"
)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


#import random

#def generate_otp():
#    return random.randint(10000, 99999)  # Generate a 5-digit OTP

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("login")
    if request.method == 'POST':
        mobile_no = request.form['mobile_no']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM rewards WHERE mobile_no = %s", (mobile_no,))
        result = cursor.fetchall()
        print(result)
	# Check if a result was found
        if result:
            for x in result:
                print(x)
            print(mobile_no)
            session['mobile_no'] = mobile_no  # Set session
            print('mobile_no verified')		
            # Generate and store OTP in session
            #otp = generate_otp()
            #session['otp'] = otp
            #print(f"Generated OTP: {otp}")  # For testing purposes
            # Redirect to OTP verification page
            return redirect('/verify_otp')
            
            #return redirect('/reward')
            #return render_template('reward.html')
            #return f"Login successful. Session mobile_no: {session['mobile_no']}"
        else:
            print("No record found for this mobile number.")
            return "Mobile number not found"
    return render_template('login.html')


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        #stored_otp = session.get('otp')  # Get OTP from session

        #if entered_otp == str(stored_otp):  # OTPs are strings in forms
        print("OTP verified successfully")
        return redirect('/reward')  # Redirect to reward page
        #else:
            #return "Invalid OTP. Please try again."

    return render_template('verify_otp.html')


@app.route('/reward')
def reward():
    print('rewards')
    mobile_no = session.get('mobile_no')
    print(mobile_no)
    if not mobile_no:
        return redirect('/login')

    print(mobile_no)
    cursor = db.cursor()
    cursor.execute("SELECT date, time, reward_amount FROM rewards WHERE mobile_no = %s", (mobile_no,))
    rewards = cursor.fetchall()
    total_amount = sum([row[2] for row in rewards])
    #print(rewards)
    #print(total_amount)
    return render_template('reward.html', rewards=rewards, total=total_amount)

@app.route('/claim', methods=['GET', 'POST'])
def claim():
    if request.method == 'POST':
        bank_account = request.form['bank_account']
        upi_id = request.form['upi_id']
        # Implement reward claim processing here
        return "Reward claimed successfully!"
    return render_template('claim.html')

import threading
# Function to run the first app on port 8080
def run_app():
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()
