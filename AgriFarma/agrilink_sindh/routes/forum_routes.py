from flask import Blueprint

forum = Blueprint('forum', __name__)

@forum.route('/forum')
def forum_home():
    return "Forum Home (Under Construction)"
