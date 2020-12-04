import numpy
from models.highlight import Predict7
from analyze.chat import *
from api.ana_url import split_url
from werkzeug.exceptions import BadRequest
from sentiment7.sentiment7 import predict_7sentiment
from settings.utils import api
from flask import Blueprint, jsonify
from api.tasks import *
import sys

sys.path.append('../')

app = Blueprint('predict7', __name__, url_prefix='/api')


@app.route('/predict7', methods=['GET'])
@api
def get_predict7(data, db):
    url = data['url']
    isURLValid = split_url(data['url'])
    if not isURLValid:
        raise BadRequest

    query = db.query(Predict7).filter(Predict7.url == url,).first()
    if query:
        return query.sentiment7_json

    result = analyze_chatlog_emotions.apply_async(args=[isURLValid[0], isURLValid[1]])

    db.add(Predict7(url=url, sentiment7_json=result.get(),))
    db.commit()
    return jsonify(result)
