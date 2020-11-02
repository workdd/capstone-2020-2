import urllib.request
import re
from api.Non_url import *
from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest
from settings.utils import api


def split_url_afreeca(url):
    if "afreecatv" in url:
        url = re.search(r"http://vod.afreecatv.com/PLAYER/STATION/[0-9]+", url).group()
    videoID = url.split('/')[-1]
    # videoID길이가 8이 아니면 invalid
    # 오류시 길이 2, 오류 안나면 2초과
    return non_url_afreeca(videoID) if len(videoID) == 8 else False


def split_url_twitch(url):
    if 'clip' in url:
        return False
    videoID = re.search(r"https://www.twitch.tv/videos/[0-9]+", url).group().split('/')[-1]
    # videoID길이가 9가 아니면 invalid
    # 없는 영상이면 http 에러코드, 아니면 recorded
    return non_url_twitch(videoID) if len(videoID) == 9 else False


def split_url_youtube(url):
    if 'youtube' in url:
        videoID = re.search(r"https://www.youtube.com/watch\?v=[a-zA-Z0-_-]+", url).group().split('=')[-1]
    else:
        videoID = re.search(r"https://youtu.be/[a-zA-Z0-_-]+", url).group().split('/')[-1]
    # videoID길이가 11이 아니면 invalid
    # 오류나면 Error, 아니면 OK
    return non_url_youtube(videoID) if len(videoID) == 11 else False


def split_url(url):
    try:
        # 작동하는 url인지 확인
        if urllib.request.urlopen(url).status != 200:
            return False

        if "afree" in url:
            return split_url_afreeca(url)
        elif "twitch" in url:
            return split_url_twitch(url)
        elif "youtu" in url:
            return split_url_youtube(url)
        return False

    except ValueError:
        return False


app = Blueprint('analysis_url', __name__, url_prefix='/api')


@app.route('/analysis_url', methods=['GET'])
@api
def get_analysis_url(data, db):
    req_list = ['url']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest
    url = data['url']
    result = split_url(url)
    return jsonify({'result':result})