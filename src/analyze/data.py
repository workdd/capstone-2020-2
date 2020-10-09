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

    def convert_from_seconds_to_time_stamp(self, seconds):
        """
        Input
        - seconds
            type : Int
            default : None
        Output
        - hours, minutes, seconds
            type : int, int, int
        """
        hours = seconds // (60 * 60)
        seconds %= (60 * 60)
        minutes = seconds // 60
        seconds %= 60

        return hours, minutes, seconds

    def extract_time_information(self, index, sub_index=0, time_type="point"):
        """
        Input
        - point
            type : TimeStamp
            default : None
        - time_type
            type : string
            default : point
            else: section
        - index
            type : Integer
            default : 0
            else : time point to analyze
        - sub_index
            type : Integer
            default : 0
            else : 1
        Output
        - time-stamp
            time_type == point
                hours, minutes, seconds
                    hours : int
                    minutes : int
                    seconds : int
            time_type == section
                section [start_time_point, end_time_point]
        """

        if time_type == 'point':
            hours, minutes, seconds = self.convert_from_seconds_to_time_stamp(self.point[index][0])
            return hours, minutes, seconds

        elif time_type == 'section':
            points = []
            for i in range(2):
                points.append(self.convert_from_seconds_to_time_stamp(int(self.section[index][2][sub_index][i])))
            return points

    def print_point_hhmmss(self):

        for i in range(len(self.point)):
            hours, minutes, seconds = self.extract_time_information(index = i, time_type='point')
            print("%02i:%02i:%02i" % (hours, minutes, seconds), self.point[i][1])

    def print_section_hhmmss(self):
        for i in range(len(self.section)):
            print("{:<3}".format(i + 1), end='\t')
            print("{:<15}".format(self.section[i][0]), end='\t')
            print("{:<15}".format(self.section[i][1]), end='\t')
            for j in range(0, len(self.section[i][2]), 2):
                points = self.extract_time_information(index=i, sub_index=j, time_type='section')
                print("%02i:%02i:%02i-%02i:%02i:%02i" % (points[0][0], points[0][1], points[0][2],
                                                         points[1][0], points[1][1], points[1][2]), end='\t')
            print()