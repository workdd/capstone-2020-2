import json
import math
import requests


def twitch_downloader(platform):
    url = 'https://api.twitch.tv/v5/videos/' + platform.video_id + '/comments'
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


DOWN_LOADERS = {'twitch':twitch_downloader}
