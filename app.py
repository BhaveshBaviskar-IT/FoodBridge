from flask import Flask, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore
app = Flask(__name__)
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/donate')
def donate():
    return render_template('donate.html')
@app.route('/submit_donation', methods=['POST'])
def submit_donation():
    donor_name = request.form['name']
    food_type = request.form['food_type']
    quantity = request.form['quantity']
    expiry = request.form['expiry']
    db.collection('donations').add({
        "donor_name": donor_name,
        "food_type": food_type,
        "quantity": quantity,
        "expiry": expiry,
        "status": "Pending"
    })
    return redirect('/')
@app.route('/ngo_dashboard')
def ngo_dashboard():
    donations = db.collection('donations').stream()
    donation_list = []
    for donation in donations:
        donation_list.append(donation.to_dict())
    return render_template(
        'ngo_dashboard.html',
        donations=donation_list
    )
if __name__ == '__main__':
    app.run(debug=True)