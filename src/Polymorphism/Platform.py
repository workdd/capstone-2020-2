import re
import json
import requests


class Platform():
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
        super(Platform, self).__init__(url)

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
        if 'clip' in self.url:
            return False
        self.video_id = re.search(r"https://www.twitch.tv/videos/[0-9]+", self.url).group().split('/')[-1]
        # videoID길이가 9가 아니면 invalid
        # 없는 영상이면 http 에러코드, 아니면 recorded
        return self.non_url() if len(self.video_id) == 9 else False
