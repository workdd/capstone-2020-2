import json
import math
import requests
import urllib.request
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import re
from ast import literal_eval
import ssl

context = ssl._create_unverified_context()

def url_to_parser(url):
    if "afree" in url:
        return 'AfreecaTV'
    elif "twitch" in url:
        return 'Twitch'
    elif "youtu" in url:
        return 'Youtube'
    return False

def url_error_checker(url):
    return urllib.request.urlopen(url,context=context).status != 200


def twitch_chat_downloader(platform):
    url = f'https://api.twitch.tv/v5/videos/{platform.video_id}/comments'
    client_id = "x7cy2lvfh9aob9oyset31dhbfng1tc"

    param = {"content_offset_seconds": 0}

    while True:
        # 처음에는 content_offset_seconds 파라미터를 이용
        # 이 후부터는 cursor 파라미터로 다음 받아올 값들을 추적
        response = requests.get(url, params=param, headers={"Client-ID": client_id})

        j = json.loads(response.text)

        for k in range(0, len(j["comments"])):
            time = math.trunc(float(j["comments"][k]["content_offset_seconds"]))
            user = j["comments"][k]["commenter"]["display_name"]
            comment = j["comments"][k]["message"]["body"].replace('\n', '')
            platform.chatlog.append([time, user, comment])

        if '_next' not in j:
            break

        param = {"cursor": j["_next"]}


def youtube_chat_downloader(platform):
    url = f"https://www.youtube.com/watch?v={platform.video_id}"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

    dict_str = ""
    next_url = ""
    session = requests.Session()
    headers = {'user-agent': user_agent}

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    # 채팅이 담겨있는 iframe
    for frame in soup.find_all("iframe"):
        if ("live_chat_replay" in frame["src"]):
            next_url = frame["src"]
            break

    while True:
        try:
            xml = session.get(next_url, headers=headers)
            soup = BeautifulSoup(xml.text, 'lxml')

            # next_url의 데이터가 있는 부분을 find_all에서 찾고 split로 쪼갠다
            for scrp in soup.find_all("script"):
                if 'responseContext' in scrp.text:
                    dict_str = scrp.text.split("] = ")[1]
                    break

            # javascript 표기이므로 변형
            dict_str = dict_str.replace('false', 'False').replace('true', 'True').rstrip(' \n;()')

            # 사전 형식으로 변환
            dics = literal_eval(dict_str)

            continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url

            # 코멘트 데이터의 목록. 선두는 노이즈 데이터이므로 [1 :]에서 저장
            dics2 = dics["continuationContents"]["liveChatContinuation"]["actions"][1:]

            for samp in enumerate(dics2):
                samp = samp[1]
                chat = ""
                de_chat = samp["replayChatItemAction"]["actions"][0]
                de_time = int(int(samp["replayChatItemAction"]["videoOffsetTimeMsec"]) / 1000)

                if "liveChatPlaceholderItemRenderer" in str(de_chat) or\
                   "addLiveChatTickerItemAction" in str(de_chat) or\
                   "liveChatPaidStickerRenderer" in str(de_chat) or\
                   "liveChatPaidMessageRenderer" in str(de_chat) or\
                   "liveChatMembershipItemRenderer" in str(de_chat):
                    continue

                chat_log = de_chat["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"]
                for i in range(len(chat_log)):
                    chat = chat + chat_log[i]["text"] if "emoji" not in chat_log[i] else chat
                chat_id = de_chat["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]

                if de_time > 0 and len(chat) != 0:
                    platform.chatlog.append([de_time, str(chat_id), str(chat).replace('\n', '')])

        # next_url를 사용할 수 없게되면 while문 종료
        except:
            break

def afreeca_chat_downloader(platform):  # 아프리카 채팅기록을 튜플로 추출하는 함수
    url = "http://vod.afreecatv.com/PLAYER/STATION/" + platform.video_id
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

    # StationNo(방송국 ID, 방송국에 여러 BJ 소속가능)와 nBbsNo(게시판 ID, 방송국 홈피에 여러 게시판 존재) 찾기
    html = requests.get(url, params=None, headers={'user-agent': user_agent})
    dom = BeautifulSoup(html.text, 'lxml')

    metatag = dom.select_one("meta[property='og:video']")['content']
    station_id = str(re.search(r"nStationNo=[0-9]+", metatag).group()[11:])
    bbs_id = str(re.search(r"nBbsNo=[0-9]+", metatag).group()[7:])
    info_url = "http://afbbs.afreecatv.com:8080/api/video/get_video_info.php?" + "nTitleNo=" + platform.video_id + "&nStationNo=" + station_id + "&nBbsNo=" + bbs_id

    # rowKey 찾기(동영상 하나에 1개 이상 존재)
    xml = requests.get(info_url, params=None, headers={'user-agent': user_agent})
    root = ElementTree.fromstring(xml.text)

    rowKey_list = []
    duration_list = [0]
    for file in root.iter('file'):
        if file.attrib.get('key') is not None:
            rowKey_list.append(file.attrib.get('key'))
            duration_list.append(int(file.attrib.get('duration')) + duration_list[-1])

    # 채팅 로그 추출하기
    url = "http://videoimg.afreecatv.com/php/ChatLoad.php"
    for idx, rowKey in enumerate(rowKey_list):
        i = 0
        while True:
            key = "rowKey=" + rowKey + "_c&startTime=" + str(3600 * i)
            xml = requests.get(url, params=key, headers={'user-agent': user_agent})
            try:
                xmltree = ElementTree.XML(xml.text)
            except ElementTree.ParseError:  # 더 이상의 채팅기록이 없어 에러가 발생하면 break
                break
            platform.chatlog.extend(
                zip(map(lambda x: math.trunc(float(x.text)) + duration_list[idx], xmltree.findall('chat/t')),
                    map(lambda x: x.text, xmltree.findall('chat/u')),
                    map(lambda x: x.text.replace('\n', ''), xmltree.findall('chat/m'))))
            i += 1


DOWN_LOADERS = {'Twitch':twitch_chat_downloader,
                'Youtube':youtube_chat_downloader,
                'AfreecaTV':afreeca_chat_downloader
                }
