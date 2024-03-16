from flask import request,Blueprint,jsonify
from app.db import Database
auth = Blueprint('login',__name__)


@auth.route('/login',methods=["POST","GET"])
def login():    
    if request.method == 'POST':
        data = request.json 
        email = data.get('email')
        password = data.get('password')
        try:
            auth = Database()
            success, account = auth.Authentificate(email,password)
            if success:
                return jsonify(account.to_json()), 200
            else:
                return jsonify({}), 401
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred'}), 500