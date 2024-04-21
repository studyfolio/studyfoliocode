from flask import request, Blueprint, jsonify
from .db import Database

admin = Blueprint('admin', __name__)


@admin.route('/add_teacher', methods=["POST"])
def add_teacher():
    if request.method == 'POST':
        data = request.json
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email')
        password = data.get('password')
        birthday = data.get('bdate')
        
        try:
            db = Database()
            success = db.add_teacher(firstname, lastname, email, password, birthday)
            
            if success:
                return jsonify({'message': 'Teacher added successfully'}), 201
            else:
                return jsonify({'message': 'Failed to add teacher'}), 400
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred'}), 500