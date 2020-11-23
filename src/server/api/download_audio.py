import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotAcceptable, Conflict

from models.highlight import SoundHighlight
from models.file import File

from settings.utils import api
from analyze.audio import *
from api.ana_url import split_url


app = Blueprint('download_audio', __name__, url_prefix='/api')


def get_url_with_error_check(data):
    if "url" not in data:
        raise BadRequest
    url_result = split_url(data['url'])
    if url_result == False:
        raise NotAcceptable  # 유효하지 않은 URL
    return url_result


def check_query(db, model, url):
    query = db.query(model).filter(
        model.url == url,
    ).first()
    return query


@app.route('/download_audio', methods=['GET'])
@api
def get_chatlog(data, db):

    url_result = get_url_with_error_check(data)

    url = data['url']
    platform = url_result[0]
    videoid = url_result[1]

    highlight_query = check_query(db, SoundHighlight, url)
    file_query = check_query(db, File, url)

    if highlight_query and file_query:
        return True

    audio = Audio(platform, videoid, url)
    audio.download()
    audio.sound_extract()

    result = {"platform": audio.platform ,"videoid": audio.video_id, "url":url, "audio": audio.data}

    return jsonify(result)