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
    card = Card.objects(_id = card_id).first()
    if card.check_project_auth(logged_user['_id']):
        comment = Comment(content)
        comment.set_creator(creator_user)
        comment.set_ref(card)
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

@comment_proc.route("/api/update-comment/<comment_id>", methods= ["PUT"])
def update_comment(comment_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    new_content = request.json.get('content')
    comments = Comment.objects( _id = comment_id)
    selected_comments = comments.first()
    if selected_comments is not None:
        if selected_comments.check_project_auth(logged_id):
            comments.update(content = new_content)
            return jsonify({'response': 200, 'message': "Updated successfully"} )
        else:
            return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})
    else:
        return jsonify({'response': 404 , 'message': "There is no comment to update."})


@comment_proc.route("/api/list-comments/<card_id>", methods= ["GET"])
def get_comment(card_id):
    if not session.get('user'):
        return jsonify({'response' : 401, 'message':"Please Login."})
    logged_id  = session['user']['_id']
    card = Card.objects( _id = card_id).first()
    comments = Comment.objects(ref_card = card)
    comments_list = []
    if comments is not None:
        if card.check_project_auth(logged_id):
            for comment in comments:
                comment_json = Comment_Schema().dump(comment)
                comments_list.append(comment_json)
            return jsonify({'response': 200, 'message' : comments_list })
        else:
            return jsonify({'response' : 403, 'message': "Authentication Error, you do not have a permission"})
    else:   
        return jsonify({'response': 404 , 'message': "There is no comment to list."})

