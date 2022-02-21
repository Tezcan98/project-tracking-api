from email import message
from errno import errorcode
from urllib import response
from flask import Blueprint, request, jsonify, session
from odm.schemas import *
from app import Session

project_proc = Blueprint('project_proc', __name__)

@project_proc.route("/api/create-project", methods= ["POST"])
def create_project():
    if session['user'].equals("401"):
        return jsonify({response : 401, message:"Please Login."})

    project_name = request.json.get('name')
    new_project = Project(project_name)
    new_project.add_auth_user(session['user']['_id'])
    new_project.save()
    return jsonify({response: 201, message: "Created successfully"} )

@project_proc.route("/api/change-project-activity/<project_id>/<activity>", methods= ["PUT"])
def change_project_activity(project_id, activity):
    project = Project.objects(_id = project_id)
    if session['user'].equals("401"):
        return jsonify({response : 401, message:"Please Login."})
    if session['user']['_id'] in project.auth_users:
        project.update(status = eval(activity)) 
    else:
        return jsonify({response : 403, message: "Authentication Error."})
    
@project_proc.route("/api/get-project-activity/<project_id>", methods= ["GET"])
def get_project_activity(project_id):
    project = Project.objects(_id = project_id).first()
    if session['user'].equals("401"):
        return jsonify({response : 401, message:"Please Login."})
    if session['user']['_id'] in project.auth_users:
        return jsonify(project.get_status())
    else:
        return jsonify({response : 403, message: "Authentication Error."})

@project_proc.route("/api/add-auth-project/<project_id>/<user_id>", methods= ["PUT"])
def add_auth_project(project_id, user_id):
    if session['user'].equals("401"):
        return jsonify({response : 401, message:"Please Login."})
    project = Project.objects(_id = project_id)
    last_project = project.first()
    auth_list = last_project.auth_users 
    if session['user']['_id'] in auth_list:
        auth_list.append(user_id)
        project.update(auth_users = auth_list)
        return jsonify({response: 200, message: "successfull"})
    else:
        return jsonify({response: 403, message: "To make assign authentication anyone, You must have an authentication. "})

@project_proc.route("/api/delete-auth-project/<project_id>/<user_id>", methods= ["DELETE"])
def delete_auth_project(project_id, user_id):
    project = Project.objects(_id = project_id)
    last_project = project.first()
    auth_list = last_project.auth_users 
    if session['user']['_id'] in auth_list:
        if user_id in auth_list:
            auth_list.remove(user_id)
            project.update(auth_users = auth_list)
            return jsonify({response: 200})
        else:
            return jsonify("There is already no authenticaton for this account.")
    else:
        return jsonify({response: 403, message: "To delete authentication for anyone, You must have an authentication. "})

@project_proc.route("/api/list-all-projects/<user_id>", methods= ["GET"])
def list_all_projects(user_id):
    account_id = session['user']['_id']
    projects = Project.objects()
    project_list = []
    for project in projects:
        if account_id in project.auth_users:
            project_json = Project_Schema().dump(project)
            project_list.append(project_json)
    return jsonify(project_list)


@project_proc.route("/api/list-project/<user_id>/<project_id>", methods= ["GET"])
def list_projects(user_id, project_id):
    account_id = session['user']['_id']
    project = Project.objects(_id = project_id).first()
    if account_id in project.auth_users:
        project_json = Project_Schema().dump(project)
        return project_json
    else:
        return jsonify({response : 403, message: "Authentication Error, you do not have a permission"})


@project_proc.route("/api/delete-project/<delete_with_email>", methods= ["DELETE"])
def delete_project(delete_with_email):
    return Project.objects(email= delete_with_email).delete()
