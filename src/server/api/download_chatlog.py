import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotAcceptable

from models.highlight import ChatHighlight
from models.chat import Keyword
from models.highlight import Predict7
from models.highlight import Predict

from settings.utils import api
from analyze.chat import *
from api.ana_url import split_url


app = Blueprint('download_chatlog', __name__, url_prefix='/api')


def get_url_with_error_check(data):
    if "url" not in data:
        raise BadRequest
    url_result = split_url(data['url'])
    if url_result == False:
        raise NotAcceptable  # 유효하지 않은 URL
    return url_result


def check_query(db, model, url=None, platform=None, videoid=None):
    if url is None:
        query = db.query(model).filter(
            model.platform == platform,
            model.videoid == videoid,
        ).first()
    else:
        query = db.query(model).filter(
            model.url == url,
        ).first()
    return query


@app.route('/download_chatlog', methods=['GET'])
@api
def get_chatlog(data, db):

    url_result = get_url_with_error_check(data)

    url = data['url']
    platform = url_result[0]
    videoid = url_result[1]

    highlight_query = check_query(db, ChatHighlight, platform=platform, videoid=videoid)
    keyword_query = check_query(db, Keyword, platform=platform, videoid=videoid)
    sentiment_query = check_query(db, Predict, url=url)
    emotion_query = check_query(db, Predict7, url=url)

    if highlight_query and keyword_query and sentiment_query and emotion_query:
        return True

    chat = Chat(platform, videoid)
    chat.download()

    result = {"platform": chat.platform ,"videoid": chat.video_id, "chatlog": chat.chatlog}

    return jsonify(result)