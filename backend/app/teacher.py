from flask import request, Blueprint, jsonify
from .db import Database
from .cloud import upload_file
from .drive_uploading import upload_ressource,upload_json,download_json
from datetime import datetime, timedelta
import json

end_data = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
teacher=Blueprint("teacher",__name__)

@teacher.route('/add_resource', methods=['POST'])
def add_resource_to_section():
    id_section = request.form.get('id_section')
    resource_name = request.form.get('resource_name')
    id_teacher = str(request.form.get('id_teacher'))
    id_module = str(request.form.get('id_module'))
    section_name = str(request.form.get('section_name'))
    file = request.files['file'] if request.files else None
    resource_type = request.form.get("type")
    description = ""
    link= request.form.get("link")
    
    file_extension = file.filename.split('.')[-1] if request.files else None
    try:
        db= Database()
        if id_section == "null" or id_section is None :
            section=db.Add_Section(section_name,id_module)
            if resource_type == "MOOC":
                data=db.Add_Activity(resource_name,description,resource_type,link,section.id,end_data)
                return jsonify({'message': 'Resource and Section added successfully','section':section.to_json(),"data":data.to_json()}), 200
            else:
                link=upload_ressource(file,resource_name)
                data=db.Add_Ressource(resource_name,file_extension,resource_type,link,id_teacher,str(section.id))
                return jsonify({'message': 'Resource and Section added successfully','section':section.to_json(),'data':data.to_json()}), 200
        else:
            if resource_type == "MOOC":
                data=db.Add_Activity(resource_name,description,resource_type,link,id_section,end_data)
                return jsonify({'message': 'Resource and Section added successfully',"data":data.to_json()}), 200
            else:
                link=upload_ressource(file,resource_name)
                data=db.Add_Ressource(resource_name,file_extension,resource_type,link,id_teacher,id_section)
                return jsonify({'message': 'Resource added successfully','data':data.to_json()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@teacher.route("/add_test",methods=["POST"])
def add_test():
    name =request.form.get('name')
    description =request.form.get('description')
    type =request.form.get('type')
    id_module = str(request.form.get('id_module'))
    file =request.files["file"] if request.files else None
    section_name = request.form.get('section_name')
    id_section =request.form.get('id_section')
    try:
        if id_section == "null" or id_section is None:
            db =Database()
            section=db.Add_Section(section_name,id_module)
            if file == "null" or file is  None:
                link=None
            else:
                link=upload_ressource(file,name)
            Activity=db.Add_Activity(name,description,type,link,section.id,end_data)
            return jsonify({"message":"test added succesfuly","data":Activity.to_json(),"section":section.to_json()}),200
        else:
            db=Database()
            if file == "null" or file is  None:
                link=None
            else:
                link=upload_ressource(file,name)
            Activity=db.Add_Activity(name,description,type,link,id_section,end_data)
            return jsonify({"message":"test added succesfuly","data":Activity.to_json()}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500
    

@teacher.route("/add_quizz",methods=["POST"])
def add_quizz():
    data =request.json
    name =data.get('name')
    type ="quizz"
    id_module = str(data.get('id_module'))
    quiz_json =data.get("quizz") 
    quizz_link=upload_json(quiz_json,name)
    section_name = data.get('section_name')
    id_section =data.get('id_section')
    try:
        if id_section == "null" or id_section is None:
            db =Database()
            section=db.Add_Section(section_name,id_module)
            Activity=db.Add_Activity(name,None,type,quizz_link,section.id,end_data)
            return jsonify({"message":"quizz added succesfuly","data":Activity.to_json(),"section":section.to_json()}),200
        else:
            db=Database()
            Activity=db.Add_Activity(name,None,type,quizz_link,id_section,end_data)
            return jsonify({"message":"quizz added succesfuly","data":Activity.to_json()}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500
        
        
    
@teacher.route('/get_module_sections', methods=['POST'])
def get_module_sections():
    data = request.json
    id_module = data.get("id_module")
    try:
        db=Database()
        sections=db.Get_Module_Sections(id_module)
        section = [section.to_json() for section in sections]
        return section,200
    except Exception as e :
        return jsonify({'error': 'Failed to fetch sections', 'details': str(e)}),500
    
@teacher.route('/delete_section', methods=['POST'])
def delete_section():
    data = request.json
    sections = data.get("sections")
    try:
        db=Database()
        db.Remove_Sections(sections)
        return jsonify({'message': 'Section deleted successfully'}), 200
    except Exception as e :
        return jsonify({'error': 'Failed to delete sections', 'details': str(e)}),500

@teacher.route('/get_section_resources', methods=['POST'])
def get_section_resources():
    data = request.json
    id_section = data.get("id_section")
    try:
        db=Database()
        resources=db.Get_Ressources_By_Section(id_section)
        resource = [resource.to_json() for resource in resources]
        return resource,200
    except Exception as e :
        return jsonify({'error': 'Failed to fetch sections', 'details': str(e)}),500
    
@teacher.route('/get_section_Activities', methods=['POST'])
def get_section_Activities():
    data = request.json
    id_section = data.get("id_section")
    try:
        db=Database()
        activities=db.Get_Section_Activities(id_section)
        activity = [activity.to_json() for activity in activities]
        return activity,200
    except Exception as e :
        return jsonify({'error': 'Failed to fetch activity', 'details': str(e)}),500
    
@teacher.route("/get_activities",methods=["GET"])
def get_activities():
    try:
        db=Database()
        activities= db.Get_Activities()
        activity= [activity.to_json() for activity in activities]
        return activity,200
    except Exception as e :
        return jsonify({"error":str(e)}),500

@teacher.route("/delete_resource",methods=["POST"])
def delete_resource():
    try:
        data = request.get_json()
        resources = data.get('id')
        db=Database()
        db.Delete_Ressource([resources])
        return jsonify({'message': 'Resources deleted successfully'}), 200
    except Exception as e :
        return jsonify({"error":str(e)}),500
    
@teacher.route("/delete_activity",methods=["POST"])
def delete_activity():
    try:
        data = request.get_json()
        activity = data.get('id')
        db=Database()
        name= db.Get_Activity_By_ID(activity).name
        db.Delete_Activity(activity)
        return jsonify({'message': f'{name} deleted successfully'}), 200
    except Exception as e :
        return jsonify({"error":str(e)}),500
    
@teacher.route("/get_activity",methods=["POST"])
def get_activity():
    try:
        data = request.get_json()
        activity = data.get('id')
        db = Database()
        Activtity=db.Get_Activity_By_ID(activity)
        if Activtity.type =="quizz":
            driveLink= Activtity.drive_link
            json = download_json(driveLink)
            return jsonify({'data':json,'type':"quizz"}),200
        else:
            return jsonify({"data":Activtity.to_json(),"type":"test"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
@teacher.route("/change_teacher_profile",methods=["POST"])
def change_teacher_profile():
    try:
        db=Database()
        teacher_id= request.form.get("teacher_id")
        picture_File=request.files['file']
        secure_url = upload_file(picture_File)
        db.Modify_Teacher_Profile_Picture(teacher_id,secure_url)
        return jsonify(secure_url),200
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}),500
    
@teacher.route("/get_submissions",methods=["POST"])
def get_submissions():
    try:
        db=Database()
        activity=  request.get_json()
        activity_id= activity.get("activity_id")
        data = [act.to_json() for act in db.Get_Activity_Submissions(activity_id)]

        return jsonify(data),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

@teacher.route("/get_module_by_teacher",methods=["POST"])
def Get_Module_By_Teacher():
    try:
        db=Database()
        activity=  request.get_json()
        teacher_id= activity.get("teacher_id")
        data = [module.to_json() for module in db.Get_Module_By_Teacher(teacher_id)]

        return jsonify(data),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

