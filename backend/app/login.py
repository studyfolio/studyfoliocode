from flask import request,Blueprint,jsonify
from .db import Database
from .utils import generate_reset_token,send_email

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
            if success :
                return jsonify(account.to_json()), 200

            else:
                return jsonify({"message":"Account not exist"}), 401
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred'}), 500

@auth.route('/reset_password', methods=["POST"])
def reset_password():
    try:
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400 
        #db = Database()
        #user = db.get_user_by_email(email)
        #if not user:
            #return jsonify({'error': 'User not found'}), 404
        reset_token = generate_reset_token(33)
        reset_url = f'http://example.com/reset-password/{reset_token}'  # Replace with your reset password page URL
        body = f'Hello aliyoucef,\n\nTo reset your password, click on the following link: {reset_url}'
        send_email("reset password",body,email)
        return jsonify({'message': 'Reset password email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to send reset password email', 'details': str(e)}), 500   