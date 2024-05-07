from flask import request, Blueprint, jsonify
from .db import Database
from .cloud import upload_file
from .drive_uploading import upload_ressource,upload_json
from datetime import datetime, timedelta
import json

end_data = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
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
    try:
        file =request.json
        link=upload_json(file,"fsfr")
        return jsonify({"link":link}),200

    except Exception as e:
        return jsonify({'error': str(e)}),500
        
        
    
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
    
