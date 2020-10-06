from konlpy.tag import Okt
import operator


def print_point_hhmmss(point):
    for i in range(len(point)):
        seconds = point[i][0]
        hours = seconds // (60 * 60)
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60
        print("%02i:%02i:%02i" % (hours, minutes, seconds), point[i][1])


def print_section_hhmmss(section):
    for i in range(len(section)):
        print("{:<3}".format(i+1), end='\t')
        print("{:<15}".format(section[i][0]), end='\t')
        print("{:<15}".format(section[i][1]), end='\t')
        j = 0
        while j < len(section[i][2]):
            seconds = int(section[i][2][j][0])
            hours = seconds // (60 * 60)
            seconds %= (60 * 60)
            minutes = seconds // 60
            seconds %= 60
            print("%02i:%02i:%02i" % (hours, minutes, seconds), end='-')
            seconds = int(section[i][2][j][1])
            hours = seconds // (60 * 60)
            seconds %= (60 * 60)
            minutes = seconds // 60
            seconds %= 60
            print("%02i:%02i:%02i" % (hours, minutes, seconds), end='\t')
            j += 2
        print()


def analyze1_chatlog(data, unit_of_time=30):
    count_second = [0 for i in range(data[-1][0] + 1)]
    for i in range(len(data)):
        count_second[data[i][0]] += 1

    count_unit = []
    for i in range(0, len(count_second), unit_of_time):  # time_range 초 단위로 쪼개서 단위 시간 내 가장 큰 값 추출
        if len(count_second) - i < unit_of_time:
            count_unit.append(max(count_second[i:len(count_second)]))
        else:
            count_unit.append(max(count_second[i:i + unit_of_time]))

    count = []
    for i in range(len(count_unit)):
        count.append([i*unit_of_time, count_unit[i]]) # [시간, 채팅량 ]

    count.sort(key=lambda ele: ele[1], reverse=True)
    point = count[0:10]

    i = 0
    while i < len(point)-1:
        j = i+1
        while j < len(point):
            if abs(point[i][0]-point[j][0]) <= 300: # 간격이 5분 이하이면 제거
                del point[j]
            else:
                j += 1
        i += 1

    if len(point) < 3:
        point = count[0:3]
    else:
        point = point[0:3]
    point.sort(key=lambda ele: ele[0])
    print_point_hhmmss(point)
    return point


def analyze1_keyword(data, keyword):
    count = [0 for i in range(int(data[-1][0] / 60) + 1)]
    # 채팅 기록에서 특정 keyword가 포함된 채팅 시간 추출
    for i in range(len(data)):
        if keyword in data[i][2]:
            count[int(data[i][0] / 60)] += 1

    section = []
    max_value = max(count)
    for i in range(len(count)):
        if count[i] == max_value:
            section.append([str(i*60), str(i*60+60)])

    return section


def find_high_frequency_words(data):
    okt = Okt()
    freq = {}
    time = {}
    for i in range(len(data)):
        nouns = okt.nouns(data[i][2])
        nouns = set(nouns)
        for key in nouns:
            if len(key) < 2:
                continue
            elif key in freq.keys():
                freq[key] += 1
                time[key].append(data[i][0])
            else:
                freq[key] = 1
                time[key] = [data[i][0]]

    sorted_freq = sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

    section = {}
    for i in range(10): # 상위 10개
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
                        if key in section.keys():
                            section[key].append([str(start_time), str(end_time)])
                        else:
                            section[key] = [[str(start_time), str(end_time)]]
                    start_time = time[key][j]
                    count = 1
                else:
                    count += 1

            if key in section.keys(): # 구간 추출 성공
                break
            else: # 구간 추출 실패
                if n < 20.0:
                    n += 1.0
                    m -= 0.5
                else:
                    section[key] = analyze1_keyword(data, key)
                    break

    top_10 = []
    i = 0
    for key in section.keys():
        if i == 10:
            break
        else:
            top_10.append([key, str(freq[key]), section[key]])
            i += 1

    print_section_hhmmss(top_10)
    return top_10