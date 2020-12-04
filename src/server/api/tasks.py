import sys

sys.path.append('../')

from server.worker import celery, celery_logger
from analyze.chat import *
from analyze.audio import *
from sentiment7.sentiment7 import predict_7sentiment
from chatsentiment.pos_neg_spm import predict_pos_neg
import numpy
import math

logger = celery_logger

def second_comment_spliiter(content):
    second, comment = [], []
    for i in range(0, len(content) - 1):
        splited_chat = content[i].split('\t')
        if len(splited_chat) < 3:
            continue
        second.append(splited_chat[0])
        comment.append(splited_chat[2])
    return second, comment


def second_comment_extractor(platform, videoid):
    chat = Chat(platform, videoid)
    chat.download()
    with open('./chatlog/{}/{}.txt'.format(platform, videoid), encoding='utf-8') as f:
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


@celery.task
def download_chatlog(platform, videoid):
    logger.info('{}({})의 채팅 다운로드 called'.format(platform, videoid))

    chat = Chat(platform, videoid)
    chat.download()

    logger.info('{}({}) 채팅 다운로드 done'.format(platform, videoid))

    return chat.chatlog


@celery.task
def analyze_chatlog_highlight(platform, videoid):
    logger.info('{}({})의 채팅 하이라이트 분석 called'.format(platform, videoid))

    chat = Chat(platform, videoid)
    chat.download()
    chat.analyze_highlight()

    logger.info('{}({})의 채팅 하이라이트 분석 done'.format(platform, videoid))

    return chat.point


@celery.task
def analyze_chatlog_keyword(platform, videoid):
    logger.info('{}({})의 채팅 키워드 분석 called'.format(platform, videoid))

    chat = Chat(platform, videoid)
    chat.download()
    chat.find_high_frequency_words()

    logger.info('{}({})의 채팅 키워드 분석 done'.format(platform, videoid))

    return chat.section


@celery.task
def download_audio(platform, videoid, url):
    logger.info('{}({})의 오디오 다운로드 called'.format(platform, videoid))

    audio = Audio(platform, videoid, url)
    audio.download()
    audio.sound_extract()

    logger.info('{}({})의 오디오 다운로드 done'.format(platform, videoid))

    return audio.data


@celery.task
def analyze_audio_highlight(platform, videoid, url):
    logger.info('{}({})의 오디오 하이라이트 분석 called'.format(platform, videoid))

    audio = Audio(platform, videoid, url)
    audio.download()
    audio.sound_extract()
    audio.analyze_highlight()

    logger.info('{}({})의 오디오 하이라이트 분석 done'.format(platform, videoid))

    return audio.point


@celery.task
def analyze_audio_normalize(platform, videoid, url):
    logger.info('{}({})의 오디오 평준화 그래프 called'.format(platform, videoid))

    audio = Audio(platform, videoid, url)
    audio.download()
    audio.sound_extract()
    audio.save_graph()

    image = {'url': url, 'name': f"./audio/normalizeAudio/{platform}/{videoid}.png"}

    logger.info('{}({})의 오디오 평준화 그래프 done'.format(platform, videoid))

    return image


@celery.task
def analyze_chatlog_emotions(platform, videoid):
    logger.info('{}({})의 채팅 7가지 감정 분석 called'.format(platform, videoid))

    second, comment = second_comment_extractor(platform, videoid)
    predict = numpy.transpose(
        [[s[1:-1] for s in second], predict_7sentiment(comment)])

    endSecond = int(second[-1][1:-1])
    inc = math.floor(endSecond / 100.0) if endSecond >= 100.0 else 1.0
    predict_per_unitsecond = prediction_unit_extractor(predict, inc)

    result = {'bin': inc, 'predict': predict_per_unitsecond}

    logger.info('{}({})의 채팅 7가지 감정 분석 done'.format(platform, videoid))

    return result


@celery.task
def analyze_chatlog_sentiments(platform, videoid):
    logger.info('{}({})의 채팅 긍정/부정 분석 called'.format(platform, videoid))

    chat = Chat(platform, videoid)
    chat.download()

    with open('./chatlog/{}/{}.txt'.format(platform, videoid), encoding='utf-8') as f:
        content = f.read().split('\n')

    second = []
    comment = []
    for i in range(0, len(content) - 1):
        splited_chat = content[i].split('\t')
        if len(splited_chat) < 3:
            continue
        second.append(splited_chat[0])
        comment.append(splited_chat[2])

    predict = numpy.transpose(
        [[s[1:-1] for s in second], predict_pos_neg(comment)])

    endSecond = int(second[-1][1:-1])
    inc = math.floor(endSecond / 100.0) if endSecond >= 100.0 else 1.0

    predict_per_unitsecond = {
        'pos': [],
        'neg': []
    }
    x = inc
    pos = 0
    neg = 0
    for p in predict:
        if int(p[0]) > x:
            x += inc
            predict_per_unitsecond['pos'].append(pos)
            predict_per_unitsecond['neg'].append(neg)
            pos = 0
            neg = 0
        if int(p[1]) == 1:
            pos += 1
        elif int(p[1]) == 0:
            neg += 1

    result = {
        'bin': inc,
        'predict': predict_per_unitsecond
    }

    logger.info('{}({})의 채팅 긍정/부정 분석 done'.format(platform, videoid))

    return result