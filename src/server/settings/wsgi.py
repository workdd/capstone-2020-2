from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import *

from api.download_chatlog import app as api_download_chatlog
from api.download_audio import app as api_download_audio
from api.chatlog_highlight import app as api_chatlog_highlight
from api.chatlog_keyword import app as api_chatlog_keyword
from api.sound_highlight import app as api_sound_highlight
from api.sound_normalize import app as api_sound_normalize
from api.predict_sentiments import app as api_predict_sentiments
from api.predict_emotions import app as api_predict_emotions
from api.account import app as api_account
from api.ana_url import app as api_analysis_url
from api.file import app as api_file
from api.login import app as api_login
from api.server import app as api_server
from api.test import app as api_test
from settings.logger import after_request, error_handler
from settings.settings import DEBUG, POSTGRESQL


def create_wsgi():
    # app settings
    app = Flask(__name__)
    app.debug = DEBUG  # debug mode
    app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL  # db connect
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.after_request(after_request)
    app.register_error_handler(InternalServerError, error_handler)

    # app connections
    app.register_blueprint(api_server)
    app.register_blueprint(api_test)
    app.register_blueprint(api_login)
    app.register_blueprint(api_chatlog_keyword)
    app.register_blueprint(api_sound_normalize)
    app.register_blueprint(api_analysis_url)
    app.register_blueprint(api_account)
    app.register_blueprint(api_predict_emotions)
    app.register_blueprint(api_predict_sentiments)
    app.register_blueprint(api_file)
    app.register_blueprint(api_sound_highlight)
    app.register_blueprint(api_chatlog_highlight)
    app.register_blueprint(api_download_chatlog)
    app.register_blueprint(api_download_audio)

    CORS(app)
    return app
