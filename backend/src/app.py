from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    return jsonify({'message':'File uploaded successfully', 'data':data})

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    return jsonify({'message':'Transcription successful', 'data':data})