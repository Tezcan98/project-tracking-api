from flask import Blueprint, request, jsonify, session
from odm.schemas import *
from app import Session
from datetime import datetime
card_procs = Blueprint('card_procs', __name__)


@card_procs.route("/api/create-card", methods= ["POST"])
def create_card():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    card_topic = request.json.get('topic')
    project_id = request.json.get('project')
    project = Project.objects(_id = project_id).first()
    new_card = Card(card_topic)
    new_card.add_ref(project)
    new_card.save()
    return jsonify({'response': 201, 'message': "Created successfully"} )

@card_procs.route("/api/fill-card/<card_id>", methods= ["PUT"])
def fill_card(card_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    typed_content = request.json.get('content')
    card = Card.objects( _id = card_id)
    this_card = card.first()
    card.update(content = typed_content)
    return jsonify({'response': 200, 'message': "Updated successfully" , "project" : this_card} )

@card_procs.route("/api/assign-card/<card_id>/<user_id>", methods= ["PUT"])
def assign_card(card_id, user_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    card = Card.objects( _id = card_id)
    user = User.objects(_id = user_id).first()
    card.update( assignment = user)
    return jsonify({'response': 200, 'message': "Assignment successful" })

@card_procs.route("/api/set-time-card/<card_id>", methods= ["PUT"])
def set_time_card(card_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    card = Card.objects( _id = card_id)
    start_time = request.json.get('start')
    try:
        start_time_format = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        end_time = request.json.get('end')
        end_time_format = datetime.strptime(end_time, '%Y-%m-%d %H:%M')
    except:
        return jsonify({'response': 417, 'message': "Date format must as %Y-%m-%d %H:%M" })
    card.update(starting_date = start_time, complated_date = end_time, status = 1 )

    return jsonify({'response': 200, 'message': "Time setted" })

@card_procs.route("/api/set-status/<card_id>/<new_status>", methods= ["PUT"])
def set_status(card_id, new_status):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    card = Card.objects( _id = card_id)
    card.update(status= new_status)
    return jsonify({'response': 200, 'message': "Status updated" })

@card_procs.route("/api/get-cards-with_status/<status>", methods= ["GET"])
def get_cards_with_status(status):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    cards = Card.objects( status = status)
    card_list = []
    if cards is None:
        return jsonify({'response': 404 , 'message': "Card not found."})
    for card in cards:
        card_json = Project_Schema().dump(card)
        card_list.append(card_json)
    return jsonify(card_list)
    
@card_procs.route("/api/list-all-cards/", methods= ["GET"])
def list_all_cards():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    cards = Card.objects()
    card_list = []
    if cards is None:
        return jsonify({'response': 404 , 'message': "Card not found."})
    for card in cards:
        card_json = Project_Schema().dump(card)
        card_list.append(card_json)
    return jsonify(card_list)
    