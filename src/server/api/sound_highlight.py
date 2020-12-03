import sys

sys.path.append('../')

from flask import Blueprint, jsonify, request, send_file
from werkzeug.exceptions import BadRequest, NotAcceptable, Conflict, NotFound

from models.highlight import SoundHighlight

from settings.utils import api
from Polymorphism.Platform import *
from Polymorphism.Audio import *
from Polymorphism.Utils import *

app = Blueprint('SNDhighlight', __name__, url_prefix='/api')


def upload_sound_highlight(data, db):
    query = db.query(SoundHighlight).filter(
        SoundHighlight.url == data['url'],
        SoundHighlight.highlight == data['highlight'],
    ).first()
    if query:  # 이미 존재하는 데이터
        raise Conflict

    new_highlight = SoundHighlight(
        url=data['url'],
        highlight=data['highlight']
    )
    db.add(new_highlight)
    db.commit()


@app.route('/SNDhighlight', methods=['GET'])
@api
def get_sound_highlight(data, db):
    req_list = ['url']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest

    url = data['url']

    query = db.query(SoundHighlight).filter(
        SoundHighlight.url == url
    ).first()
    if query:
        return jsonify(query.highlight_json)
    cl = eval(url_to_parser(url))
    url_result = cl(url).split_url()

    if url_result != False:
        pt = Platform("")
        pt.platform_name = url_result[0]
        pt.video_id = url_result[1]
        audio = Audio(pt)
        audio.download()
        audio.sound_extract()
        audio.analyze_highlight()

        result = {"highlight": audio.point}
        new_sound_highlight = SoundHighlight(
            url=url,
            highlight_json=result
        )
        db.add(new_sound_highlight)
        db.commit()
        return jsonify(result)
    else:
        raise NotAcceptable  # 유효하지 않은 URL
