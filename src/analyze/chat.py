import requests
import json
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from ast import literal_eval
import math
import os
import re
from analyze.data import Data
from konlpy.tag import Okt
import operator


class Chat(Data):
    def __init__(self, platform, video_id):
        self.platform = platform
        self.video_id = video_id
        self.data = []
        self.chatlog = []
        self.unit_of_time = 30
        self.point = []
        self.section = []

    def download(self):
        if not os.path.exists(f"./chatlog/{self.platform}"):
            os.makedirs(f"./chatlog/{self.platform}")

        if self.video_id + ".txt" in os.listdir(f"./chatlog/{self.platform}"):
            print('This chatlog file has already been requested.')
            with open(f"./chatlog/{self.platform}/{self.video_id}.txt", encoding='utf-8') as f:
                line = f.read().split('\n')
            for i in range(0, len(line) - 1):
                splited_line = line[i].split('\t')
                if len(splited_line) < 3:
                    continue
                self.chatlog.append([int(splited_line[0][1:-1]), splited_line[1][1:-1], splited_line[2]])
        else:
            if self.platform == "AfreecaTV":
                self.afreeca()
            elif self.platform == "Twitch":
                self.twitch()
            elif self.platform == "Youtube":
                self.youtube()
            self.array_to_file()

        count = [0 for i in range(self.chatlog[-1][0] + 1)]
        for i in range(len(self.chatlog)):
            count[self.chatlog[i][0]] += 1

        for i in range(0, len(count), self.unit_of_time):  # time_range 초 단위로 쪼개서 단위 시간 내 가장 큰 값 추출
            end_slicing_index = len(count) if len(count) - i < self.unit_of_time else i + self.unit_of_time
            self.data.append(max(count[i:end_slicing_index]))
        return self.chatlog


    def afreeca(self):  # 아프리카 채팅기록을 튜플로 추출하는 함수
        url = "http://vod.afreecatv.com/PLAYER/STATION/" + self.video_id
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"

        # StationNo(방송국 ID, 방송국에 여러 BJ 소속가능)와 nBbsNo(게시판 ID, 방송국 홈피에 여러 게시판 존재) 찾기
        html = requests.get(url, params=None, headers={'user-agent': user_agent})
        dom = BeautifulSoup(html.text, 'lxml')

        metatag = dom.select_one("meta[property='og:video']")['content']
        station_id = str(re.search(r"nStationNo=[0-9]+", metatag).group()[11:])
        bbs_id = str(re.search(r"nBbsNo=[0-9]+", metatag).group()[7:])
        info_url = "http://afbbs.afreecatv.com:8080/api/video/get_video_info.php?" + "nTitleNo=" + self.video_id + "&nStationNo=" + station_id + "&nBbsNo=" + bbs_id

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
                self.chatlog.extend(
                    zip(map(lambda x: math.trunc(float(x.text)) + duration_list[idx], xmltree.findall('chat/t')),
                        map(lambda x: x.text, xmltree.findall('chat/u')),
                        map(lambda x: x.text.replace('\n', ''), xmltree.findall('chat/m'))))
                i += 1

    def twitch(self):  # 트위치 채팅기록을 리스트로 추출하는 함수
        url = 'https://api.twitch.tv/v5/videos/' + self.video_id + '/comments'
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
                self.chatlog.append([time, user, comment])

            if '_next' not in j:
                break

            param = {"cursor": j["_next"]}

    def youtube(self):
        url = "https://www.youtube.com/watch?v=" + self.video_id
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

                    if "liveChatPlaceholderItemRenderer" or "addLiveChatTickerItemAction" or "liveChatPaidStickerRenderer" or "liveChatPaidMessageRenderer" or "liveChatMembershipItemRenderer" in str(de_chat):
                        continue

                    chat_log = de_chat["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"]
                    for i in range(len(chat_log)):
                        chat = chat + chat_log[i]["text"] if "emoji" not in chat_log[i] else chat
                    chat_id = de_chat["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["authorName"]["simpleText"]

                    if de_time > 0 and len(chat) != 0:
                        self.chatlog.append([de_time, str(chat_id), str(chat).replace('\n', '')])

            # next_url를 사용할 수 없게되면 while문 종료
            except:
                break

    def array_to_file(self):  # 배열을 텍스트 파일로 저장하는 함수
        file_name = f"./chatlog/{self.platform}/{self.video_id}.txt"
        with open(file_name, 'w', encoding="utf-8") as f:
            for x in range(0, len(self.chatlog)):
                f.write('[')
                f.write(str(self.chatlog[x][0]))
                f.write(']')
                f.write('\t')
                f.write('(')
                f.write(str(self.chatlog[x][1]))
                f.write(')')
                f.write('\t')
                f.write(str(self.chatlog[x][2]))
                f.write("\n")
        f.close()

    def analyze_keyword(self, keyword):
        count = [0 for i in range(int(self.chatlog[-1][0] / 60) + 1)]
        # 채팅 기록에서 특정 keyword가 포함된 채팅 시간 추출
        for i in range(len(self.chatlog)):
            if keyword in self.chatlog[i][2]:
                count[int(self.chatlog[i][0] / 60)] += 1

        points = []
        max_value = max(count)
        for i in range(len(count)):
            if count[i] == max_value:
                points.append([str(i * 60), str(i * 60 + 60)])

        return points

    def find_high_frequency_words(self):
        okt = Okt()
        freq = {}
        time = {}
        for i in range(len(self.chatlog)):
            for key in set(okt.nouns(self.chatlog[i][2])):
                if len(key) < 2:
                    continue
                elif key in freq.keys():
                    freq[key] += 1
                    time[key].append(self.chatlog[i][0])
                else:
                    freq[key] = 1
                    time[key] = [self.chatlog[i][0]]

        sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

        section_dic = {}
        for i in range(10):  # 상위 10개
            n = 10.0
            m = 10.0
            key = sorted_freq[i][0]
            while True:
                start_time = time[key][0]
                count = 1
                for j in range(1, len(time[key])):
                    if time[key][j] - time[key][j - 1] > n:
                        if count >= m:
                            end_time = time[key][j - 1]
                            if key in section_dic.keys():
                                section_dic[key].append([str(start_time), str(end_time)])
                            else:
                                section_dic[key] = [[str(start_time), str(end_time)]]
                        start_time = time[key][j]
                        count = 1
                    else:
                        count += 1

                if key in section_dic.keys():  # 구간 추출 성공
                    break
                elif n < 20.0:
                    n += 1.0
                    m -= 0.5
                else:
                    section_dic[key] = self.analyze_keyword(key)
                    break

        i = 0
        for key in section_dic.keys():
            if i == 10:
                break
            self.section.append([key, str(freq[key]), section_dic[key]])
            i += 1
        self.print_section_hhmmss()