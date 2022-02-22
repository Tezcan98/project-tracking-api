from flask import Blueprint, request, jsonify, session
from odm.schemas import *
from app import Session
from datetime import datetime
card_procs = Blueprint('card_procs', __name__)


@card_procs.route("/api/create-card", methods= ["POST"])
def create_card():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    card_topic = request.json.get('topic')
    project_id = request.json.get('project')
    project = Project.objects(_id = project_id).first()
    if logged_id in project.auth_users:
        new_card = Card(card_topic)
        new_card.add_ref(project)
        new_card.save()
        return jsonify({'response': 201, 'message': "Created successfully"} )
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@card_procs.route("/api/fill-card/<card_id>", methods= ["PUT"])
def fill_card(card_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    typed_content = request.json.get('content')
    card = Card.objects( _id = card_id)
    if card.only('topic','ref_project').get().check_project_auth(logged_id):
        this_card = card.first()
        card.update(content = typed_content)
        return jsonify({'response': 200, 'message': "Updated successfully"} )
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@card_procs.route("/api/assign-card/<card_id>/<user_id>", methods= ["PUT"])
def assign_card(card_id, user_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    
    card = Card.objects( _id = card_id)
    if card.only('topic','ref_project').get().check_project_auth(logged_id):
        user = User.objects(_id = user_id).first()
        card.update( assignment = user)
        return jsonify({'response': 200, 'message': "Assignment successful" })
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@card_procs.route("/api/set-time-card/<card_id>", methods= ["PUT"])
def set_time_card(card_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']

    card = Card.objects( _id = card_id)
    if card.only('topic','ref_project').get().check_project_auth(logged_id):
        try:
            start_time = request.json.get('start')
            start_time_format = datetime.strptime(start_time, '%d-%m-%Y %H:%M')  #TODO : hours not seen
            end_time = request.json.get('end')
            end_time_format = datetime.strptime(end_time, '%d-%m-%Y %H:%M')
        except:
            return jsonify({'response': 417, 'message': "Error, Date format must as %d-%m-%Y %H:%M" })
        card.update(starting_date = start_time_format, complated_date = end_time_format, status = 1 )

        return jsonify({'response': 200, 'message': start_time_format })
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@card_procs.route("/api/set-status/<card_id>/<new_status>", methods= ["PUT"])
def set_status(card_id, new_status):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    card = Card.objects( _id = card_id)
    if card.only('topic','ref_project').get().check_project_auth(logged_id):
        card.update(status= new_status)
        return jsonify({'response': 200, 'message': "Status updated" })
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@card_procs.route("/api/get-cards-with_status/<status>", methods= ["GET"])
def get_cards_with_status(status):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    cards = Card.objects( status = status) 
    card_list = []
    for card in cards:
        card_json = Card_Schema().dump(card)
        if cards.only('topic','ref_project').get(_id = card._id ).check_project_auth(logged_id):
            card_list.append(card_json)
    if cards == []:
        return jsonify({'response': 404 , 'message': "There is no card to list."})
    return jsonify(card_list)
    
@card_procs.route("/api/list-all-cards/", methods= ["GET"])
def list_all_cards():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    cards = Card.objects()
    card_list = []
    if cards is None:
        return jsonify({'response': 404 , 'message': "Card not found."})
    for card in cards:
        if cards.only('topic','ref_project').get(_id = card._id).check_project_auth(logged_id):
            card_json = Card_Schema().dump(card)
            card_list.append(card_json)
    return jsonify({'response': 200, 'message' : card_list })
