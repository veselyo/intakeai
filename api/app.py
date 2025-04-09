from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Get the Firebase credentials from the environment variable and parse it
firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
if firebase_credentials is None:
    raise Exception("FIREBASE_CREDENTIALS environment variable is not set.")

# cred_info = json.loads(firebase_credentials)
# cred = credentials.Certificate(cred_info)
# firebase_admin.initialize_app(cred)

# # Initialize Firestore database
# db = firestore.client()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/store', methods=['POST'])
def store():
    # Receive the JSON payload from the webhook request
    data = request.json

    # Extract your captured variables from the payload
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    ssn = data.get('ssn')
    insurance = data.get('insurance')
    additional_comments = data.get('additional_comments')
    phone_number = data.get('phone_number')
    phq4_1 = data.get('phq4_1')
    phq4_2 = data.get('phq4_2')
    phq4_3 = data.get('phq4_3')
    phq4_4 = data.get('phq4_4')


    # # Create a new document in the "intake" collection
    # doc_ref = db.collection("intake").document()
    # doc_ref.set({
    #     "first_name": first_name,
    #     "last_name": last_name,
    #     "insurance": insurance,
    #     "phone_number": phone_number,
    #     "ssn": ssn,
    #     "additional_comments": additional_comments,
    #     "phq4_1": phq4_1,
    #     "phq4_2": phq4_2,
    #     "phq4_3": phq4_3,
    #     "phq4_4": phq4_4
    # })

    # Return a success response to the webhook
    return jsonify({"status": "success"}), 200