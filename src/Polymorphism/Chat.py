import os

from Polymorphism.Utils import *
from Polymorphism.Data import *

from konlpy.tag import Okt
class Chat(Data):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform

    def download(self):
        if not os.path.exists(f"./chatlog/{self.platform.platform_name}"):
            os.makedirs(f"./chatlog/{self.platform.platform_name}")

        if self.platform.video_id + ".txt" in os.listdir(f"./chatlog/{self.platform.platform_name}"):
            print('This chatlog file has already been requested.')
            with open(f"./chatlog/{self.platform.platform_name}/{self.platform.video_id}.txt", encoding='utf-8') as f:
                line = f.read().split('\n')
            for i in range(0, len(line) - 1):
                splited_line = line[i].split('\t')
                if len(splited_line) < 3:
                    continue
                self.platform.chatlog.append([int(splited_line[0][1:-1]), splited_line[1][1:-1], splited_line[2]])
        else:
            DOWN_LOADERS[self.platform.platform_name](self.platform)
            self.array_to_file()

        count = [0 for i in range(self.platform.chatlog[-1][0] + 1)]
        for i in range(len(self.platform.chatlog)):
            count[self.platform.chatlog[i][0]] += 1

        for i in range(0, len(count), self.platform.unit_of_time):  # time_range 초 단위로 쪼개서 단위 시간 내 가장 큰 값 추출
            end_slicing_index = len(count) if len(count) - i < self.platform.unit_of_time else i + self.platform.unit_of_time
            self.data.append(max(count[i:end_slicing_index]))
        return self.platform.chatlog

    def data_getter(self):
        pass

    def array_to_file(self):
        file_name = f'./chatlog/{self.platform.platform_name}/{self.platform.video_id}.txt'
        chat_log = self.platform.chatlog
        with open(file_name, 'w', encoding="utf-8") as f:
            for i in range(0, len(chat_log)):
                f.write(f"[{chat_log[i][0]}]\t({chat_log[i][1]})\t{chat_log[i][2]}\n")

    def analyze_keyword(self, keyword):
        count = [0 for _ in range((self.platform.chatlog[-1][0] // 60) + 1)]
        for i in range(len(self.platform.chatlog)):
            if keyword in self.platform.chatlog[i][2]:
                count[self.platform.chatlog[i][0] // 60] += 1

        points = []
        max_value = max(count)
        for i in range(len(count)):
            if count[i] == max_value:
                points.append([str(i * 60), str(i * 3600)])
        return points

    def find_high_frequency_words(self):
        okt = Okt()
        freq, time = {}, {}
        for data in self.platform.chatlog:
            for key in set(okt.nouns(data[2])):
                if len(key) < 2:
                    continue
                elif key in freq.keys():
                    freq[key] += 1
                    time[key].append(data[0])
                else:
                    freq[key] = 1
                    time[key] = [data[0]]
                # if key not in freq:
                #     freq[key] = 0
                #     time[key] = []
                # freq[key] += 1
                # time[key].append([data[0]])

        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

        section_dic = {}
        for i in range(10):
            n = 10
            m = 10
            key = sorted_freq[i][0]
            while True:
                start_time = time[key][0]
                count = 1
                for j in range(1, len(time[key])):
                    if time[key][j] - time[key][j - 1] > n:
                        if count >= m:
                            end_time = time[key][j - 1]
                            if key not in section_dic:
                                section_dic[key] = []
                            section_dic[key].append([str(start_time), str(end_time)])
                        start_time = time[key][j]
                        count = 1
                    else:
                        count += 1
                if key in section_dic:
                    break
                elif n < 20:
                    n += 1
                    m -= 0.5
                else:
                    section_dic[key] = self.analyze_keyword(key)
                    break

        for key in list(section_dic.keys())[:10]:
            self.platform.section.append([key, str(freq[key]), section_dic[key]])
        self.print_section_hhmmss()
