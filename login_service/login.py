
from flask import Blueprint, redirect, render_template, request, jsonify, url_for,session
from datetime import datetime
from botocore.exceptions import ClientError
from login_service.database import *



login_bp = Blueprint('login', __name__)


@login_bp.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("sign-up.html")

@login_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
       
        # Check user credentials
        user_exists = check_user_credentials(email, password)
        user_role = get_user_role(email)  # Get the user's role from the database

        if user_exists and user_role == "admin":
            # User exists and is an admin, perform login action
            session['authenticated'] = True  # Set the 'authenticated' session variable
            session['email'] = email  # Optionally, store user-specific data in the session
            session['role'] = user_role  # Store the user's role in the session
            return redirect(url_for('events.Bulletinadmin'))
        
        elif user_exists and user_role == "user":
            session['authenticated'] = True  # Set the 'authenticated' session variable
            session['email'] = email
            session['role'] = user_role
            return redirect(url_for('events.Bulletinuser'))
        else:
            # User doesn't exist or credentials are incorrect
            error_message = "Invalid email or password. Please try again."
            return render_template("login.html", error=error_message)
        
    return render_template("login.html")



@login_bp.route('/register', methods=['POST'])
def register():
    # Get form data from the request
    email = request.form['email']
    # Make sure you have corresponding 'name' attributes in your HTML form
    password = request.form['password']

    # Initialize the DynamoDB client

    # Add the data to your DynamoDB table
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    response = table.put_item(
        Item={
            'email': email,
            'password': password,
            'role':'user',
            # Add other attributes as needed
        }
    )

    # You can handle the response or redirect to a success page
    return "Sign-up successful!"