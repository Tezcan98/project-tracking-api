from flask import Blueprint, request, jsonify, session
from odm.schemas import *
from app import Session


comment_proc = Blueprint('comment_proc', __name__)

@comment_proc.route("/api/create-comment", methods= ["POST"])
def create_project():
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_user = session['user']
    creator_user = User_Schema().load(logged_user)
    content = request.json.get('content')
    card_id = request.json.get('card_id')
    card = Card.objects(_id = card_id)
    if card.only('topic','ref_project').get().check_project_auth(logged_user['_id']):
        comment = Comment(content)
        comment.set_creator(creator_user)
        comment.set_ref(card.first())
        comment.save()
        return jsonify({'response': 201, 'message': "Created successfully"} )
    else:
        return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})

@comment_proc.route("/api/delete-comment/<comment_id>", methods= ["DELETE"])
def delete_comment(comment_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id = session['user']['_id']
    comment=  Comment.objects(_id = comment_id).first()
    if comment is not None:
        if comment.check_project_auth(logged_id):
            comment.delete()
            return jsonify({'response': 200, 'message' : "succesfully deleted"})
        else:
            return jsonify({'response' : 403, 'message': "Authentication Error."})
    return jsonify({'response': 404 , 'message': "Comment not found."})