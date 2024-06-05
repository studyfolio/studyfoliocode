from flask import request, Blueprint, jsonify
from .db import Database
from .csv_ import add_csv
from .cloud import upload_file
from .utils import generate_code,send_email

admin = Blueprint('admin', __name__)

@admin.route('/add_teacher', methods=["POST","GET"])
def add_teacher():
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
            data=db.Add_Teacher(firstname, lastname,email, password,birthday,phone,None)
            if isinstance(data,str):
                return jsonify({'message': data}), 400
            else:
                subject="StudyFolio Account"
                html = f"""
    <html>
    <head>

    </head>
    <body>
        <div class="content">
            <div class="header">
                <h1>StudyFolio Account Information</h1>
            </div>
            
            <div style="font-size:20px;">
            <h4>Hello,</h4>
            <h5>Email :<b>{email}</b></h5>
            <h5>Password :<b>{password}</b></h5>
            </div>
            <div class="footer">
                <p>&copy; 2024 study folio</p>
            </div>
        </div>
    </body>
    </html>
    """
                send_email(subject,message='',to_email=email,html=html)
                return  jsonify({'message': 'teacher added successfully','teacher':data.to_json()}), 200
        except Exception as e:
            return jsonify({'message': 'An unexpected error occurred','details': str(e)}), 500


@admin.route('/delete_teachers', methods=['POST'])
def delete_teachers():
    data = request.get_json()
    teacher_ids = data.get('ids')
    if not teacher_ids:
        return jsonify({'error': 'No teacher IDs provided'}), 400
    db = Database()
    db.Delete_Teachers(teacher_ids) 
    return jsonify({'message': 'Requested teachers deleted successfully'}), 200


@admin.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    firstname = data.get('fname')
    lastname = data.get('lname')
    email = data.get('email')
    password = data.get('password')  
    birthday = data.get('birthday')
    phone = data.get('phone')
    group_id= data.get('group_id')
    try:
        db = Database()            
        data=db.Add_Student(firstname, lastname,email, password,birthday,phone,group_id,None)
        if isinstance(data,str):
            return jsonify({'message': data}), 400
        else:
            subject="StudyFolio Account"
            html = f"""
    <html>
    <head>

    </head>
    <body>
        <div class="content">
            <div class="header">
                <h1>StudyFolio Account Information</h1>
            </div>
            
            <div style="font-size:20px;">
            <h4>Hello,</h4>
            <h5>Email :<b>{email}</b></h5>
            <h5>Password :<b>{password}</b></h5>
            </div>
            <div class="footer">
                <p>&copy; 2024 study folio</p>
            </div>
        </div>
    </body>
    </html>
    """
            send_email(subject,message='',to_email=email,html=html)
            return  jsonify({'message': 'student added successfully','student':data.to_json()}), 200
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred'}), 500

@admin.route('/add_student_csv', methods=['POST'])
def upload_csv():
    file = request.files['file']
    group_id = request.form.get('group_id',None)
    if file and file.filename.endswith('.csv'):
        try:
            data = add_csv(file,group_id)
            if isinstance(data,str):
                return jsonify({"error": data}),400
            else:
                return jsonify({'message': 'File processed successfully',"students":data}), 200
        except Exception as e:
            return jsonify({'error': 'Failed to process file', 'details': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


@admin.route('/delete_students', methods=['POST'])
def delete_students():
    data = request.get_json()
    student_ids = data.get('ids')
    if not student_ids:
        return jsonify({"error": "No student IDs provided"}), 400
    try:
        db= Database()
        db.Delete_Students(student_ids)
        return jsonify({"message": "Students deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin.route('/delete_promo', methods=['POST'])
def delete_promo():
    data = request.get_json()
    if not data or 'id_promo' not in data:
        return jsonify({"error": "Missing 'id_promo' in request body"}), 400
    
    id_promo = data['id_promo']
    
    try:
        db= Database()
        db.Delete_Promo(id_promo)
        return jsonify({"message": "Promotion deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin.route('/modify_group', methods=['POST'])
def modify_group():
    data = request.get_json()
    student_ids = data.get('student_ids')
    new_group = data.get('new_group')
    
    if not student_ids or not new_group:
        return jsonify({"error": "Missing 'student_ids' or 'new_group' in request body"}), 400
    
    try:
        db= Database()
        students=db.Modify_Group(student_ids, new_group)
        
        students_json = [student.to_json() for student in students]

        return jsonify({"message": "Group modified successfully","students":students_json}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin.route('/get_teachers',methods=["GET"])
def get_teachers():
    try:
        db = Database()
        teachers = db.Get_Teachers()
        teachers_json = [teacher.to_json() for teacher in teachers]
        return teachers_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch teachers', 'details': str(e)}), 500

@admin.route('/get_students',methods=["GET"])
def get_students():
    try:
        db = Database()
        students = db.Get_Students()
        students_json = [student.to_json() for student in students]
        return students_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch students', 'details': str(e)}), 500

@admin.route('/add_promo_with_groups', methods=['POST'])
def add_promo_with_groups():
    data = request.json
    name = data.get("name")
    year = data.get('year')
    number_of_groups = data.get('number_of_groups') 
    group_json= []
    db= Database()
    promo_result = db.Add_Promo(name,year)
    if promo_result:
        promo_id = promo_result.id
        for i in range(int(number_of_groups)):
            group_number = i+1 
            group=db.Add_Group(group_number, promo_id)
            group_json.append(group.to_json())
        
        return jsonify({"success": True, "message": "Promo and groups added successfully","promo":promo_result.to_json(),"groups":group_json}), 201
    else:
        return jsonify({"success": False, "message": "Failed to add promo"}), 400
    
@admin.route('/add_module', methods=['POST'])
def add_module():
    name = request.form.get('name')
    acronym = request.form.get('acronym')
    description = request.form.get('description')
    coefficient = request.form.get('coefficient')  
    file = request.files['file']
    secure_url = upload_file(file)

    try:
        db = Database()
        data = db.Add_Module(name, acronym, description, coefficient, secure_url)
        return jsonify({'message': 'module added successfully',"data":data.to_json()}), 201
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500



@admin.route('/get_modules',methods=["GET"])
def get_modules():
    try:
        db = Database()
        modules = db.Load_Modules()
        modules_json = [module.to_json() for module in modules]
        return modules_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Modules', 'details': str(e)}), 500


@admin.route('/assign_role', methods=['POST'])
def assign_role():
    data = request.json
    id_teacher = data.get('id_teacher')
    id_module = data.get('id_module')
    type_charge = data.get('type_charge')
    permission = data.get('permission')  

    try:
        db = Database()
        db.Assign(id_teacher, id_module, type_charge, permission)
        return jsonify({'message': 'Role assigned successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred', 'error': str(e)}), 500
    
@admin.route('/get_teacher_roles',methods=["POST"])
def get_teacher_roles():
    data = request.json
    id_teacher = data.get('id_teacher')
    try:
        db = Database()
        roles = db.Get_Teacher_Roles(id_teacher)
        roles_json = [role.to_json() for role in roles]
        return roles_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Roles', 'details': str(e)}), 500
    
@admin.route('/get_roles_by_module_id',methods=["POST"])
def get_roles_by_id():
    data = request.json
    id_module = data.get('id_module')
    try:
        db = Database()
        roles = db.Get_Roles_By_Module(id_module)
        roles_json = [role.to_json() for role in roles]
        return roles_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Roles', 'details': str(e)}), 500


@admin.route('/add_module_promo',methods=["POST"])
def add_module_promo():
    data = request.json
    id_promo = data.get('id_promo')
    id_module = data.get('id_module')
    shown = data.get('shown')
    semester = data.get('semester')
    try:
        db = Database()
        data=db.Add_Study_Link(id_promo,id_module,shown,semester)
        return jsonify({'message': 'Module assigned successfully',"data":data.to_json()}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add module', 'details': str(e)}), 500

@admin.route('/delete_module_promo',methods=["POST"])
def delete_module_promo():
    data = request.json
    id_promo = data.get('id_promo')
    id_modules = data.get('id_modules')
    try:
        db = Database()
        db.Remove_Study_Link(id_promo,id_modules)
        return jsonify({'message': 'Module delete successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to delete modules', 'details': str(e)}), 500


@admin.route('/get_promo_modules',methods=["POST"])
def get_promo_modules():
    data = request.json
    id_promo = data.get('id_promo')
    try:
        db = Database()
        modules = db.Get_Promo_Modules(id_promo)
        modules_json = [module.to_json() for module in modules]
        return modules_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch modules', 'details': str(e)}), 500

@admin.route('/get_roles',methods=["GET"])
def get_roles():
    try:
        db = Database()
        Roles = db.Get_Roles()
        Roles_json = [role.to_json() for role in Roles]
        return Roles_json, 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch modules', 'details': str(e)}), 500
    
@admin.route('/show_module',methods=["POST"])
def show_module():
    data = request.json
    id_promo = data.get('id_promo')
    id_module = data.get('id_module')
    try:
        db = Database()
        data=db.Show_Module(id_module,id_promo)
        data_json = [study.to_json() for study in data]
        return jsonify({'message': 'Module shown successfully','data':data_json}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to show module', 'details': str(e)}), 500

@admin.route('/hide_module',methods=["POST"])
def hide_module():
    data = request.json
    id_promo = data.get('id_promo')
    id_module = data.get('id_module')
    try:
        db = Database()
        data=db.Hide_Module(id_module,id_promo)
        data_json = [study.to_json() for study in data]
        return jsonify({'message': 'Module hidden successfully','data':data_json}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to hide module', 'details': str(e)}), 500

@admin.route('/delete_module',methods=["POST"])
def delete_module():
    data = request.json
    id_module = data.get('id_module')
    try:
        db = Database()
        db.Delete_Module(id_module)
        return jsonify({'message': 'Module deleted successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to deleted module', 'details': str(e)}), 500
    