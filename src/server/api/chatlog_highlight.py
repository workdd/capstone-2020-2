import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotAcceptable

from models.highlight import ChatHighlight
from settings.utils import api
from Polymorphism.Platform import *
from Polymorphism.Chat import *
from Polymorphism.Utils import *

app = Blueprint('chatlog_highlight', __name__, url_prefix='/api')


def get_url_with_error_check(data):
    if "url" not in data:
        raise BadRequest

    url = data['url']
    pt = Platform(url)
    cl = eval(url_to_parser(url))
    url_result = cl(pt).split_url()
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

    pt = Platform()
    pt._platform_name = url_result[0]
    pt._video_id = url_result[1]
    chat = Chat(pt)
    chat.download()
    chat.analyze_highlight()

    result = {"highlight": chat.point}
    db.add(ChatHighlight(
        platform=url_result[0],
        videoid=url_result[1],
        highlight_json=result))
    db.commit()
    return jsonify(result)
