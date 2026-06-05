from flask import Flask, render_template, request, redirect, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/submit_donation', methods=['POST'])
def submit_donation():
    """
    Handle donation submission with image URL from Cloudinary.
    Expects JSON payload with:
    - donor_name: str
    - food_type: str
    - quantity: int/float
    - expiry: str (date in YYYY-MM-DD format)
    - notes: str (optional)
    - image_url: str (Cloudinary image URL)
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        # Extract and validate required fields
        donor_name = data.get('donor_name', '').strip()
        food_type = data.get('food_type', '').strip()
        quantity = data.get('quantity', '')
        expiry = data.get('expiry', '').strip()
        notes = data.get('notes', '').strip()
        image_url = data.get('image_url', '').strip()

        # Validation
        if not donor_name:
            return jsonify({'error': 'Donor name is required'}), 400
        if not food_type:
            return jsonify({'error': 'Food type is required'}), 400
        if not quantity:
            return jsonify({'error': 'Quantity is required'}), 400
        if not expiry:
            return jsonify({'error': 'Expiry date is required'}), 400

        # Convert quantity to float for storage
        try:
            quantity = float(quantity)
        except ValueError:
            return jsonify({'error': 'Quantity must be a valid number'}), 400

        # Prepare donation object
        donation_data = {
            "donor_name": donor_name,
            "food_type": food_type,
            "quantity": quantity,
            "expiry": expiry,
            "notes": notes,
            "image_url": image_url,  # Cloudinary image URL stored here
            "status": "Pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        # Save to Firestore (including image_url)
        db.collection('donations').add(donation_data)

        print(f"Donation recorded: {donation_data}")  # For debugging

        return jsonify({'message': 'Donation submitted successfully', 'data': {
            **donation_data,
            "created_at": donation_data["created_at"].isoformat(),
            "updated_at": donation_data["updated_at"].isoformat()
        }}), 200

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400
    except Exception as e:
        print(f"Error submitting donation: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/ngo_dashboard')
def ngo_dashboard():
    """
    Fetch all donations from Firestore and display in NGO dashboard.
    Displays donor name, food type, quantity, expiry date, image URL, and status.
    """
    try:
        donations = []

        donations_stream = db.collection('donations').stream()
        for donation in donations_stream:
            donation_dict = donation.to_dict()
            donation_dict['id'] = donation.id  # Include document ID for reference
            donations.append(donation_dict)

        return render_template(
            'ngo_dashboard.html',
            donations=donations
        )
    except Exception as e:
        print(f"Error fetching donations: {str(e)}")
        return render_template('ngo_dashboard.html', donations=[]), 500


@app.route('/donation/<donation_id>')
def get_donation(donation_id):
    """
    Get a specific donation by ID including the image URL.
    Returns the full donation object with image_url field.
    """
    try:
        donation_ref = db.collection('donations').document(donation_id)
        donation = donation_ref.get()
        if donation.exists:
            donation_dict = donation.to_dict()
            donation_dict['id'] = donation.id
            return jsonify(donation_dict), 200
        else:
            return jsonify({'error': 'Donation not found'}), 404

    except Exception as e:
        print(f"Error fetching donation: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/claim_donation/<donation_id>', methods=['POST'])
def claim_donation(donation_id):
    """
    Mark a donation as claimed by an NGO.
    """
    try:
        db.collection('donations').document(donation_id).update({
            'status': 'Claimed',
            'updated_at': datetime.now()
        })

        return jsonify({'message': 'Donation claimed successfully'}), 200
    except Exception as e:
        print(f"Error claiming donation: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)