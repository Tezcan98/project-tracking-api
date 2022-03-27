from flask import Blueprint, request, jsonify, session
from odm.schemas import *
# from app import Session
from flask_session import Session ## will be chanced

project_proc = Blueprint('project_proc', __name__)

@project_proc.route("/api/create-project", methods= ["POST"])
def create_project():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    project_name = request.json.get('name')
    new_project = Project(project_name)
    new_project.add_auth_user(session['user']['_id'])
    new_project.save()
    return jsonify({'response': 201, 'message': "Created successfully"} )

@project_proc.route("/api/change-project-activity/<project_id>/<activity>", methods= ["PUT"])
def change_project_activity(project_id, activity):
    project = Project.objects(_id = project_id)
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    if session['user']['_id'] in project.auth_users:
        project.update(status = eval(activity)) 
        return jsonify({'response': 200, 'message': "change activity successfull"})
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error."})
    
@project_proc.route("/api/get-project-activity/<project_id>", methods= ["GET"])
def get_project_activity(project_id):
    project = Project.objects(_id = project_id).first()
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    if session['user']['_id'] in project.auth_users:
        return jsonify(project.get_status())
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error."})

@project_proc.route("/api/add-auth-project/<project_id>/<user_id>", methods= ["PUT"])
def add_auth_project(project_id, user_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']

    project = Project.objects(_id = project_id)
    last_project = project.first()
    auth_list = last_project.auth_users 
    if logged_id in auth_list:
        auth_list.append(user_id)
        project.update(auth_users = auth_list)
        return jsonify({'response': 200, 'message': "successfull"})
    else:
        return jsonify({'response': 403, 'message': "To make assign authentication anyone, You must have an authentication. "})

@project_proc.route("/api/delete-auth-project/<project_id>/<user_id>", methods= ["DELETE"])
def delete_auth_project(project_id, user_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
        
    project = Project.objects(_id = project_id)
    last_project = project.first()
    auth_list = last_project.auth_users 
    if logged_id in auth_list:
        if user_id in auth_list:
            auth_list.remove(user_id)
            project.update(auth_users = auth_list)
            return jsonify({'response': 200})
        else:
            return jsonify({'response': 406 , 'message': "There is already no authenticaton for this account."})
    else:
        return jsonify({'response': 403, 'message': "To delete authentication for anyone, You must have an authentication. "})

@project_proc.route("/api/list-all-projects/", methods= ["GET"])
def list_all_projects():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message' :"Please Login."})
    logged_id = session['user']['_id']
    projects = Project.objects()
    if projects == '[]':
        return jsonify({'response': 406 , 'message': "There is no project for this account. "})
    project_list = []
    for project in projects:
        if project.check_auth(logged_id):
            project_json = Project_Schema().dump(project)
            project_list.append(project_json)
    return jsonify(project_list)
        

@project_proc.route("/api/list-project/<project_id>", methods= ["GET"])
def list_project(project_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    project = Project.objects(_id = project_id).first()
    if project is None:
        return jsonify({'response': 404 , 'message': "Project not found."})
    if logged_id in project.auth_users:
        project_json = Project_Schema().dump(project)
        return jsonify({'response': 200, 'message' : project_json })
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@project_proc.route("/api/delete-project/<project_id>", methods= ["DELETE"])
def delete_project(project_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id = session['user']['_id']
    project=  Project.objects(_id = project_id).first()
    if project is not None:
        if project.check_auth(logged_id):
            project.delete()
            return jsonify({'response': 200, 'message' : "succesfully deleted"})
        else:
            return jsonify({'response' : 403, 'message': "Authentication Error."})
@project_proc.route("/api/update-project-name/<project_id>/<new_name>", methods= ["PUT"])
def update_project(project_id, new_name):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    project = Project.objects(_id = project_id).first()
    if project is None:
        return jsonify({'response': 404 , 'message': "Project not found."})
    if logged_id in project.auth_users:
        project.update(name = new_name )
        return jsonify({'response': 200, 'message': "Update successfull"})
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error."})