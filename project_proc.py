from flask import Blueprint, request, jsonify, session
from odm.schemas import *


project_proc = Blueprint('project_proc', __name__)

@project_proc.route("/api/create-project", methods= ["POST"])
def create_project():
    project_name = request.json.get('name')
    new_project = Project(project_name)
    new_project.save()

@project_proc.route("/api/add-auth-project/<project-name>/<activate>", methods= ["PUT"])
def change_project_activity(project_name, activate):
    project = Project.objects(name = project_name) 
    project.set_activity(activate)
    project.update() 

@project_proc.route("/api/add-auth-project/<project-name>/<email>", methods= ["PUT"])
def add_auth_project(project_name, add_email):
    project = Project.objects(name = project_name)
    user = User.objects(email = add_email)
    project.add_auth_user(user)
    project.update()

@project_proc.route("/api/add-auth-project/<project-name>/<email>", methods= ["PUT"])
def delete_auth_project(project_name, add_email):
    project = Project.objects(name = project_name)
    user = User.objects(email = add_email)
    project.delete_auth_user(user)
    project.update()

@project_proc.route("/api/list-all-projects/", methods= ["GET"])
def list_all_projects():
    return Project.objects()

@project_proc.route("/api/list-project/<name>", methods= ["GET"])
def list_projects(s_name):
    project = Project.objects(name = s_name)
    project_json = Project_Schema.dump(project)
    return project_json

@project_proc.route("/api/delete-project/<delete_with_email>", methods= ["DELETE"])
def delete_project(delete_with_email):
    return Project.objects(email= delete_with_email).delete()
