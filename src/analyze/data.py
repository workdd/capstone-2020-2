import datetime

class Data:
    def __init__(self, platform, video_id):
        self.platform = platform
        self.video_id = video_id
        self.data = None # 단위 시간당 볼륨, 채팅량 카운드
        self.unit_of_time = 30
        self.point = None #하이라이트 지점
        self.section = None

    def analyze_highlight(self):
        count = []
        for i in range(len(self.data)):
            count.append([i * self.unit_of_time, self.data[i]])  # [시간, 채팅량 ]

        count.sort(key=lambda ele: ele[1], reverse=True)
        self.point = count[0:10]

        i = 0
        while i < len(self.point) - 1:
            j = i + 1
            while j < len(self.point):
                if abs(self.point[i][0] - self.point[j][0]) <= 300:  # 간격이 5분 이하이면 제거
                    del self.point[j]
                else:
                    j += 1
            i += 1

        if len(self.point) < 3:
            self.point = count[0:3]
        else:
            self.point = self.point[0:3]
        self.point.sort(key=lambda ele: ele[0])
        self.print_point_hhmmss()


    def print_point_hhmmss(self):
        for i in range(len(self.point)):
            print(datetime.timedelta(seconds=self.point[i][0]), self.point[i][1])


    def print_section_hhmmss(self):
        for i in range(len(self.section)):
            print("{:<3}".format(i + 1), end='\t')
            print("{:<15}".format(self.section[i][0]), end='\t')
            print("{:<15}".format(self.section[i][1]), end='\t')
            for j in range(0, len(self.section[i][2])):
                print(datetime.timedelta(seconds=int(self.section[i][2][j][0])), '-', datetime.timedelta(seconds=int(self.section[i][2][j][1])), end='\t')
            print()