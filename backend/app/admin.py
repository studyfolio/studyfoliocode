from flask import request, Blueprint, jsonify
from .db import Database

admin = Blueprint('admin', __name__)

@admin.route('/add_teacher', methods=["POST","GET"])
def add_teacherer():
    if request.method == 'POST':
        data = request.json
        firstname = data.get('fname')
        lastname = data.get('lname')
        email = data.get('email')
        password = data.get('password')
        birthday = data.get('bdate')
        phone= data.get('phone')
        
        try:
            db = Database()            
            db.Add_Teacher(firstname, lastname,email, password,birthday,phone)
            
            if firstname and lastname and email and password and birthday and phone:
                return jsonify({'message': 'Teacher added successfully'}), 201
            else:
                return jsonify({'message': 'Failed to add teacher'}), 400
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred'}), 500

@admin.route('/get_teachers',methods=["GET"])
def get_teachers():
    if request.method == 'GET':
        db = Database()
        teachers=db.Get_Teachers()
        teachers_json = []
        for teacher in teachers:
            teachers_json.append(teacher.to_json())
        return teachers_json
    
    