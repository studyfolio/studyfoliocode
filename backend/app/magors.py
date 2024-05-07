from flask import Blueprint, jsonify
from .db import Database

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
