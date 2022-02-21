from flask import Blueprint, request, jsonify, session
from odm.schemas import *

card_list_procs = Blueprint('card_list_procs', __name__)


@card_list_procs.route("/api/create-card", methods= ["POST"])
def create_card():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    card_topic = request.json.get('topic')
    project_id = request.json.get('project')
    new_card = Card_List(card_topic, project_id)
    # new_card.save()
    return jsonify({'response': 201, 'message': "Created successfully"} )
