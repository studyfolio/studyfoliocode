from flask import request,Blueprint,jsonify
from .db import Database
from .cloud import upload_file
from .drive_uploading import upload_ressource
student = Blueprint('student',__name__)


@student.route('/get_modules', methods=["POST"])
def get_modules():
    try:
        db = Database()
        data = request.json
        promo_id = data.get('id_promo')
        modules = db.Get_Promo_Modules(promo_id)
        module = [module.to_json() for module in modules]
        return jsonify(module),200
    except Exception as e:
        return jsonify({'message': 'An unexpected error occurred','details': str(e)}), 500
    
@student.route("/change_student_profile",methods=["POST"])
def change_student_profile():
    try:
        db=Database()
        student_id= request.form.get("student_id")
        picture_File=request.files['file']
        secure_url = upload_file(picture_File)
        db.Modify_Student_Profile_Picture(student_id,secure_url)
        return jsonify(secure_url),200
    except Exception as e:
        return jsonify({"error":str(e)}),500


@student.route("/add_submission",methods=["POST"])
def add_submission():
    try:
        db=Database()
        student_id= request.form.get("student_id")
        student_name = request.form.get("student_name")
        id_activity= request.form.get("activity_id")
        mark = request.form.get("note") if request.form.get("note") else None
        observation =None
        solution=request.files['file'] if request.files else None
        drive_link = upload_ressource(solution,student_name) if solution is not  None else None
        data=db.Add_Submission(student_id,id_activity,mark,observation,drive_link)    
        return jsonify(data.to_json()),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

@student.route("/get_submission",methods=["POST"])
def get_submission():
    try:
        db=Database()
        student_id= request.get("student_id")
        data=[sub.to_json for sub in db.Get_Students_Submissions(student_id)]    
        return jsonify(data),200
    except Exception as e:
        return jsonify({"error":str(e)}),500