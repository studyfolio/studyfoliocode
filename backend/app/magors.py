from flask import Blueprint, jsonify,request
from .db import Database
from .utils import generate_code,send_email

promos_api = Blueprint('promos_api', __name__)

@promos_api.route('/get_promos', methods=['GET'])
def get_promos():
    try:
        db= Database()
        promos = db.Get_Promos()
        promos_list = [{'id': promo.id, 'name': promo.name, 'year': promo.year} for promo in promos]
        return jsonify(promos_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch promos', 'details': str(e)}), 500

@promos_api.route('/get_groups', methods=['GET'])
def get_groups():
    try:
        db= Database()
        groups = db.Get_Groups()
        groups_list = [{'id': group.id, 'name': group.number, 'promo': {'id': group.promo.id, 'name': group.promo.name, 'year': group.promo.year}} for group in groups]
        return jsonify(groups_list), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch groups', 'details': str(e)}), 500
    

@promos_api.route('/get', methods=["GET"])
def get_all_data():
    try:
        db = Database()
        teachers = db.Get_Teachers()
        students = db.Get_Students()
        modules = db.Load_Modules()
        promos = db.Get_Promos()
        groups = db.Get_Groups()
        Roles = db.Get_Roles()
        studies = db.Get_Studies()
        
        teachers_json = [teacher.to_json() for teacher in teachers]
        students_json = [student.to_json() for student in students]
        modules_json = [module.to_json() for module in modules]
        promos_list = [{'id': promo.id, 'name': promo.name, 'year': promo.year} for promo in promos]
        groups_list = [{'id': group.id, 'name': group.number, 'promo': {'id': group.promo.id, 'name': group.promo.name, 'year': group.promo.year}} for group in groups]
        Roles_json = [role.to_json() for role in Roles]
        studies_json = [study.to_json() for study in studies]
        all_data = {
            'teachers': teachers_json,
            'students': students_json,
            'modules': modules_json,
            'promos': promos_list,
            'groups': groups_list,
            'roles' : Roles_json,
            'studies':studies_json
        }
        
        return jsonify(all_data), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch data', 'details': str(e)}), 500

@promos_api.route("get_ressource",methods=["POST"])
def get_ressource():
    try:
        db = Database()
        data = request.json
        id_module = data.get('id_module')
        sections = db.Get_Module_Sections(id_module)
        ressources_list = []
        for section in sections :
            ressources = [res.to_json() for res in db.Get_Ressources_By_Section(section.id)]
            activities = [act.to_json() for act in db.Get_Section_Activities(section.id)]
            infos={
                'id' : section.id,
                'name' : section.name,
                'module' : section.module.to_json(),
                'ressources' : ressources,
                'activities' : activities
            }
            ressources_list.append(infos)
        return jsonify({"data":ressources_list}),200
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred','details': str(e)}), 500

@promos_api.route("give_notation",methods=["POST"])
def give_notation():
    try:
        data=request.json
        id_student : str=data.get('id_student')
        id_activity : str=data.get('id_activity')
        mark : str=data.get('mark')
        observation = data.get('observation') if data.get('observation') is not None else None
        db=Database()
        notation=db.Give_Notation(id_student,id_activity,mark,observation)
        return jsonify({"notation":notation.to_json()}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@promos_api.route("/send_cc",methods=['POST'])
def send_code():
    try:
        data =request.json
        email= data.get('email')
        code= generate_code(6)
        subject="Reset password code"
        html = f"""
    <html>
    <head>

    </head>
    <body>
        <div class="content">
            <div class="header">
                <h1>StudyFolio</h1>
            </div>
            
            <div style="font-size:20px;">
            <h4>Hello,</h4>
            <h5>Password reset code :<b>{code}</b></h5>
            
            </div>
            <div class="footer">
                <p>&copy; 2024 study folio</p>
            </div>
        </div>
    </body>
    </html>
    """
        send_email(subject,message="",to_email=email,html=html)  
        return jsonify(code) ,200 
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@promos_api.route("/reset_password",methods=["POST"])
def reset_password():
    try:
        db= Database()
        data=request.json
        email= data.get('email')
        password = data.get('password')
        db.Reset_Password(email,password)
        return jsonify({}),200
    except Exception as e:    
        return jsonify({"error":str(e)}),500
