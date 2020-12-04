import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest

from models.chat import Keyword
from settings.utils import api
from analyze.chat import *
from api.tasks import *


app = Blueprint('chatlog', __name__, url_prefix='/api')


def get_info_with_error_check(data):
    for i in ['platform', 'videoid']:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest
    return data['platform'], data['videoid']


@app.route('/chatlog', methods=['GET'])
@api
def get_chatlog(data, db):
    platform, videoid = get_info_with_error_check(data)

    query = db.query(Keyword).filter(
        Keyword.platform == platform,
        Keyword.videoid == videoid,).first()
    if query:
        return jsonify(query.keyword_json)

    section = analyze_chatlog_keyword.apply_async(args=[platform, videoid])

    result = {'keyword': section.get()}
    keyword = Keyword(
        platform=platform,
        videoid=videoid,
        keyword_json=result)

    db.add(keyword)
    db.commit()
    return jsonify(result)
