import re
import json
import urllib.request

import requests
from ast import literal_eval
from bs4 import BeautifulSoup

from Polymorphism.Utils import *


class Platform:
    def __init__(self, url):
        self.platform_name = ""
        self.video_id = -1
        self.url = url
        self.chatlog = []
        self.chat_data = ""
        self.section = []
        self.unit_of_time = 30

    def split_url(self):
        pass

    def get_analysis_url(self):
        pass

    def non_url(self):
        pass


class Twitch(Platform):
    def __init__(self, url):
        super().__init__(url)

    def non_url(self):
        url = 'https://api.twitch.tv/v5/videos/' + self.video_id
        client_id = "x7cy2lvfh9aob9oyset31dhbfng1tc"
        param = {"content_offset_seconds": 0}
        response = requests.get(url, params=param, headers={"Client-ID": client_id})
        # 없는 영상이면 http 에러코드, 아니면 recorded
        j = json.loads(response.text)

        if j['status'] == 'recorded':
            return ['Twitch', self.video_id]
        return False

    def split_url(self):
        if url_error_checker(self.url):
            return False

        if 'clip' in self.url:
            return False
        if type(self.url) != type(""):
            return False
        self.video_id = re.search(r"https://www.twitch.tv/videos/[0-9]+", self.url).group().split('/')[-1]
        # videoID길이가 9가 아니면 invalid
        # 없는 영상이면 http 에러코드, 아니면 recorded
        return self.non_url() if len(self.video_id) == 9 else False


class Youtube(Platform):
    def __init__(self, url):
        super().__init__(url)

    def non_url(self):
        url = f"https://www.youtube.com/watch?v={self.video_id}"
        dict_str = ""
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")

        # 상태가 담겨있는 script
        for scrp in soup.find_all("script"):
            if 'ytInitialPlayerResponse' in scrp.text:
                dict_str = scrp.text.split('["ytInitialPlayerResponse"] = ')[1].split('if (window.ytcsi)')[0]
                break

        # javascript 표기이므로 변형
        dict_str = dict_str.replace('false', 'False').replace('true', 'True').rstrip(' \n;()')
        # 사전 형식으로 변환
        dics = literal_eval(dict_str)
        if dics["playabilityStatus"]["status"] != 'Error' and dics['videoDetails']['isLiveContent'] == True:
            return ['Youtube', self.video_id]
        return False

    def split_url_youtube(self):
        if url_error_checker(self.url):
            return False

        if 'youtube' in self.url:
            self.video_id = re.search(r"https://www.youtube.com/watch\?v=[a-zA-Z0-_-]+", self.url).group().split('=')[
                -1]
        else:
            self.video_id = re.search(r"https://youtu.be/[a-zA-Z0-_-]+", self.url).group().split('/')[-1]
        # videoID길이가 11이 아니면 invalid
        # 오류나면 Error, 아니면 OK
        return self.non_url() if len(self.video_id) == 11 else False


class AfreecaTV(Platform):
    def __init__(self, url):
        super().__init__(url)

    def non_url(self):
        url = 'http://vod.afreecatv.com/PLAYER/STATION/' + self.video_id
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        # 아프리카는 동영상이 없으면 따로 페이지 없이 <script>한줄만 나타남(확인창?)
        # 오류시 길이 2, 오류 안나면 2초과

        if len(soup) > 2 and soup.find_all("body", class_='replay') != 0:
            return ['AfreecaTV', self.video_id]
        return False

    def split_url(self):
        if url_error_checker(self.url):
            return False

        if "afreecatv" in self.url:
            url = re.search(r"http://vod.afreecatv.com/PLAYER/STATION/[0-9]+", self.url).group()
        self.video_id = self.url.split('/')[-1]
        # videoID길이가 8이 아니면 invalid
        # 오류시 길이 2, 오류 안나면 2초과
        return self.non_url() if len(self.video_id) == 8 else False
