
from analyze.chat import *
from api.ana_url import split_url
from chatsentiment.pos_neg_spm import predict_pos_neg
from werkzeug.exceptions import BadRequest
from models.highlight import Predict
from settings.utils import api
from flask import Blueprint, jsonify
from api.tasks import *
import numpy
import math
import sys

sys.path.append('../')

app = Blueprint('predict', __name__, url_prefix='/api')

@app.route('/predict', methods=['GET'])
@api
def get_predict(data, db):
    url = data['url']
    isURLValid = split_url(url)

    if not isURLValid:
        raise BadRequest

    query = db.query(Predict).filter(
        Predict.url == url,
    ).first()

    if query:
        return query.predict_json

    result = analyze_chatlog_sentiment.apply_async(args=[isURLValid[0], isURLValid[1]])
    
    new_predict = Predict(
        url=url,
        posneg_json=result.get(),
    )
    db.add(new_predict)
    db.commit()
    return jsonify(result)
