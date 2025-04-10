from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime

# Get the Firebase credentials from the environment variable
firebase_credentials = os.environ.get("FIREBASE_CREDENTIALS")
if firebase_credentials is None:
    raise Exception("FIREBASE_CREDENTIALS environment variable is not set.")

# Initialize Firestore database
cred_info = json.loads(firebase_credentials)
cred = credentials.Certificate(cred_info)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Flask app
app = Flask(__name__)

# Index route that renders a Google Sheets-style view of intake data
@app.route('/')
def home():

    # Fetch all documents from the "intake" collection in Firestore
    try:
        docs = db.collection("intake").stream()

        # Convert each document to a dictionary
        patients = [doc.to_dict() for doc in docs]

        # Render the template with the data
        return render_template('index.html', patients=patients)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/store', methods=['POST'])
def store():

    # Receive a JSON response from the webhook request
    data = request.json

    # Extract captured variables from the response
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    ssn = data.get('ssn')
    insurance = data.get('insurance')
    additional_comments = data.get('additional_comments')
    phone_number = data.get('phone_number')

    # Parse PHQ-4 items as integers (default to 0 if missing)
    phq4_1_score = int(data.get('phq4_1', 0))
    phq4_2_score = int(data.get('phq4_2', 0))
    phq4_3_score = int(data.get('phq4_3', 0))
    phq4_4_score = int(data.get('phq4_4', 0))

    # Compute total PHQ-4 score
    phq4_total = phq4_1_score + phq4_2_score + phq4_3_score + phq4_4_score

    # Determine overall severity level
    if phq4_total >= 9:
        phq4_severity = "severe"
    elif phq4_total >= 6:
        phq4_severity = "moderate"
    elif phq4_total >= 3:
        phq4_severity = "mild"
    else:
        phq4_severity = "normal"

    # Scores suggest anxiety/depression if sum of first/last two items ≥ 3
    suggests_anxiety = (phq4_1_score + phq4_2_score) >= 3
    suggests_depression = (phq4_3_score + phq4_4_score) >= 3

    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create a new document in the "intake" collection in Firestore
    doc_ref = db.collection("intake").document()
    doc_ref.set({
        "date": current_date,
        "first_name": first_name,
        "last_name": last_name,
        "insurance": insurance,
        "phone_number": phone_number,
        "ssn": ssn,
        "additional_comments": additional_comments,
        "phq4_1": phq4_1_score,
        "phq4_2": phq4_2_score,
        "phq4_3": phq4_3_score,
        "phq4_4": phq4_4_score,
        "phq4_total": phq4_total,
        "phq4_severity": phq4_severity,
        "suggests_anxiety": suggests_anxiety,
        "suggests_depression": suggests_depression
    })

    # Return a success response
    return jsonify({"status": "success"}), 200
