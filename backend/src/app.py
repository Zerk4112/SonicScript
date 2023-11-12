from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
import os

load_dotenv() # This loads the environment variables from the .env file

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

CORS(app) # This will enable CORS for all routes

class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data=request.json
        return 'Hello, {}!'.format(data['name'])
    return 'Hello, World!'

@app.route('/api/files/upload', methods=['POST'])
def upload():
    data = request.json
    return jsonify({'message':'File uploaded successfully', 'data':data})

@app.route('/api/transcriptions/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    return jsonify({'message':'Transcription successful', 'data':data})

@app.route('/api/users/register', methods=['POST'])
def register():
    """
    Registers a new user by creating a new User object and adding it to the database.

    Returns:
        A JSON response containing an error message (if any), a success message, and the ID of the newly created user.
    """
    if request.method == 'POST':
        # Get user input from the request form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        email = User.query.filter_by(email=email).first()
        # print("{} / {}".format(user.id, user.email))
        if user:
            # If the username already exists, return an error message
            return jsonify({"error":"Username already in use.", "message":"", "data":""}), 409
        
        if email:
            # If the email already exists, return an error message
            return jsonify({"error":"Email already used for a different account, Please use a different one.", "message":"", "data":""}), 409

        # Hash the password using pbkdf2:sha256 method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new User object with the hashed password
        new_user = User(username=username, email=email, password=hashed_password)
        # Add the new user to the database and commit the changes

        # try:
        db.session.add(new_user)
        db.session.commit()
        
        # except Exception as e:
        #     # If there is an error, rollback the changes and return an error message
        #     db.session.rollback()
        #     return jsonify({"error":"Error occurred during registration. Please contact an administrator.", "message":"", "data":""})

        # Return a success message and the ID of the newly created user
        return jsonify({"error":"",'message':'User successfully registered', 'userID':new_user.id}), 201
    
    # If the request method is not POST, return an error message
    return jsonify({"error":"GET method not allowed", "message":"", "data":""}), 405

@app.route('/api/users/login', methods=['POST'])
def login():
    """
    This function handles user login requests.

    Returns:
    JSON response containing error message, login message and user ID.
    """
    if request.method == 'POST':
        # Get username and password from the request form
        username = request.form['username']
        password = request.form['password']

        # Query the User table for the given username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            # Set the user ID in the session
            session['user_id'] = user.id
            # Return a JSON response with success message and user ID
            return jsonify({"error":"",'message':'Login successful', 'userID':user.id})
        else:
            # If the user doesn't exist or the password is incorrect, return an error message
            flash('Invalid username or password', 'error')
            return jsonify({"error":"Invalid username or password", "message":"", "data":""}), 401

    # If the request method is not POST, return an error message
    return jsonify({"error":"GET method not allowed", "message":"", "data":""}), 405