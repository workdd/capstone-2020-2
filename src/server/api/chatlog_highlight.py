import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotAcceptable

from models.highlight import ChatHighlight
from settings.utils import api
from analyze.chat import *
from api.ana_url import split_url


app = Blueprint('chatlog_highlight', __name__, url_prefix='/api')


def get_url_with_error_check(data):
    if "url" not in data:
        raise BadRequest
    url_result = split_url(data['url'])
    if url_result == False:
        raise NotAcceptable  # 유효하지 않은 URL
    return url_result


@app.route('/chatlog_highlight', methods=['GET'])
@api
def get_chatlog_highlight(data, db):
    url_result = get_url_with_error_check(data)

    query = db.query(ChatHighlight).filter(
        ChatHighlight.platform == url_result[0],
        ChatHighlight.videoid == url_result[1],
    ).first()
    if query:
        return jsonify(query.highlight_json)

    chat = Chat(url_result[0], url_result[1])
    chat.download()
    chat.analyze_highlight()

    result = {"highlight": chat.point}
    db.add(ChatHighlight(
        platform=url_result[0],
        videoid=url_result[1],
        highlight_json=result))
    db.commit()
    return jsonify(result)
