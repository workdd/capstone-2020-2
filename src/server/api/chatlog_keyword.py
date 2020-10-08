import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest

from models.chat import Keyword
from settings.utils import api
from analyze.chat import *


app = Blueprint('chatlog', __name__, url_prefix='/api')


@app.route('/chatlog', methods=['GET'])
@api
def get_chatlog(data, db):
    req_list = ['platform', 'videoid']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest
    platform = data['platform']
    videoid = data['videoid']

    query = db.query(Keyword).filter(
        Keyword.platform == platform,
        Keyword.videoid == videoid,
    ).first()
    if query:
        return jsonify(query.keyword_json)

    chat = Chat(platform, videoid)
    chat.download()
    chat.find_high_frequency_words()

    result = {'keyword': chat.section}

    keyword = Keyword(
        platform=platform,
        videoid=videoid,
        keyword_json=result
    )
    db.add(keyword)
    db.commit()

    return jsonify(result)
