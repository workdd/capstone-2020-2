import youtube_dl
import numpy as np
from moviepy.editor import *
import matplotlib.pyplot as plt
import os

from Polymorphism.Utils import *
from Polymorphism.Data import *

class Audio(Data):
    def __init__(self, platform):
        super().__init__()
        self.platform = platform

    def download(self):
        dw_opts = {'format': 'worstaudio/worst', 'extractaudio': True, 'audioformat': "mp3",
                   'outtmpl': "audio/" + self.platform.platform_name + '/' + self.platform.video_id +\
                              '_' + '%(playlist_index)s' + ".mp3"}
        try:
            with youtube_dl.YoutubeDL(dw_opts) as ydl:
                ydl.download([self.platform.url])
        except Exception as e:
            print('error', e)

    def load_audio(self, filetype):
        files = []
        audio = None
        for i in os.listdir(f'./{filetype}/{self.platform.platform_name}/'):
            if self.platform.video_id in i:
                files.append(i)

        arr = []
        if filetype == "video":
            for filename in files:
                arr.append(VideoFileClip(f"video/{self.platform.platform_name}/{filename}"))
            video = concatenate_videoclips(arr)

            video.close()
        elif filetype == "audio":
            for filename in files:
                arr.append(AudioFileClip(f"./audio/{self.platform.platform_name}/{filename}"))  # 음성 파일 로드
            audio = concatenate_audioclips(arr)  # 음성 파일이 분할된 상태라면 이어붙임
        return audio

    def sound_extract(self, filetype="audio"):
        audio = self.load_audio(filetype)

        sr = audio.fps  # 샘플링 레이트
        cut = lambda x: audio.subclip(x, x + 1).to_soundarray(fps=sr)  # 1초에 해당하는 데이터를 뽑는 람다함수
        volume = lambda array: np.sqrt(((1.0 * array) ** 2).mean())  # 음압 -> 음량 변환하는 람다함수

        volumes = []
        for i in range(0, int(audio.duration - 2)):  # audio에 대해 람다함수 실행
            try:  # 간혹 분할되어 다운된 영상에 대해 발생하는 예외 처리..
                volumes.append(volume(cut(i)))
            except:
                volumes.append(0.0)

        self.data = []
        for i in range(0, len(volumes), self.platform.unit_of_time):  # time_range 초 단위로 쪼개서 단위 시간 내 가장 큰 값 추출
            end_slicing_index = len(volumes) if len(volumes) - i < self.platform.unit_of_time\
                else i + self.platform.unit_of_time
            self.data.append(max(volumes[i:end_slicing_index]))

        audio.close()

    def save_graph(self, AVG_20=0.221829165):  # AVG_20 = 유튜브 하이라이트 영상 20개에 대한 평균
        plt.switch_backend('Agg')
        fig, ax1 = plt.subplots()  # plot
        x = list(range(len(self.data)))
        for i in range(len(x)):
            x[i] *= self.platform.unit_of_time
        ax1.plot(x, self.data, color='b')
        plt.axhline(y=AVG_20, color='r', linewidth=1)
        ax1.set_ylabel("volume")  # y 축
        ax1.set_xlabel("second")  # x 축
        plt.title("Volumes of each second")  # 제목

        path = f"./audio/normalizeAudio/{self.platform}/"
        if not os.path.exists(path):
            os.makedirs(path)

        plt.savefig(path + f"{self.platform.video_id}.png")
