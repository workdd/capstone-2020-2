import numpy
from models.highlight import Predict7

from Polymorphism.Chat import *
from Polymorphism.Platform import *
from Polymorphism.Utils import *
from werkzeug.exceptions import BadRequest
from sentiment7.sentiment7 import predict_7sentiment
from settings.utils import api
from flask import Blueprint, jsonify
import sys

sys.path.append('../')

app = Blueprint('predict7', __name__, url_prefix='/api')

def second_comment_spliiter(content):
    second, comment = [], []
    for i in range(0, len(content) - 1):
        splited_chat = content[i].split('\t')
        if len(splited_chat) < 3:
            continue
        second.append(splited_chat[0])
        comment.append(splited_chat[2])
    return second, comment


def second_comment_extractor(isURLValid):
    pt = Platform("")
    pt.platform_name = isURLValid[0]
    pt.video_id = isURLValid[1]
    chat = Chat(pt)
    chat.download()
    with open('./chatlog/{}/{}.txt'.format(isURLValid[0], isURLValid[1]), encoding='utf-8') as f:
        content = f.read().split('\n')
    second, comment = second_comment_spliiter(content)
    if len(second) < 1 or len(comment) < 1:
        raise BadRequest
    return second, comment


def prediction_unit_extractor(prediction, inc):
    predict_per_unitsecond = {
        'neutral': [], 'joy': [], 'love': [], 'fear': [],
        'surprise': [], 'sadness': [], 'anger': []}
    cnt_per_unitsecond = {
        'neutral': 0, 'joy': 0, 'love': 0, 'fear': 0,
        'surprise': 0, 'sadness': 0,'anger': 0}
    x = inc
    for p in prediction:
        if int(p[0]) > x:
            x += inc
            for key in cnt_per_unitsecond:
                predict_per_unitsecond[key].append(cnt_per_unitsecond[key])
                cnt_per_unitsecond[key] = 0
        cnt_per_unitsecond[p[1]] += 1
    return predict_per_unitsecond


@app.route('/predict7', methods=['GET'])
@api
def get_predict7(data, db):
    url = data['url']

    pt = Platform(url)
    cl = eval(url_to_parser(url))
    isURLValid = cl(pt).split_url()
    if not isURLValid:
        raise BadRequest

    query = db.query(Predict7).filter(Predict7.url == url,).first()
    if query:
        return query.sentiment7_json

    second, comment = second_comment_extractor(isURLValid)
    predict = numpy.transpose(
        [[s[1:-1] for s in second], predict_7sentiment(comment)])

    endSecond = int(second[-1][1:-1])
    inc = math.floor(endSecond / 100.0) if endSecond >= 100.0 else 1.0
    predict_per_unitsecond = prediction_unit_extractor(predict, inc)

    result = {'bin': inc, 'predict': predict_per_unitsecond}
    db.add(Predict7(url=url, sentiment7_json=result,))
    db.commit()
    return jsonify(result)
