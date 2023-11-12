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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('User successfully registered', 'success')
        return jsonify({"error":"",'message':'User successfully registered', 'userID':new_user.id})
    return jsonify({"error":"GET method not allowed", "message":"", "data":""})

@app.route('/api/users/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            # flash('Login successful', 'success')
            # return redirect(url_for('dashboard'))
            return jsonify({"error":"",'message':'Login successful', 'userID':user.id})
        else:
            flash('Invalid username or password', 'error')
            return jsonify({"error":"Invalid username or password", "message":"", "data":""})

    return jsonify({"error":"GET method not allowed", "message":"", "data":""})