import requests
import json
from re import search
import wget
from cda import common
from cda.exceptions import CdaDownloadUrlError


def get_video_data(url: str) -> dict:
    r = requests.get(url, headers=common.HEADERS)
    match = search(r"player_data='(?P<data>.+)' tab", r.text)
    return json.loads(match.group('data'))


def get_video_url(player_data: dict, resolution) -> str:
    send_data = {
        "jsonrpc": "2.0",
        "method": "videoGetLink",
        "params": [
            f"{player_data['video']['id']}",
            f"{resolution}",
            player_data['video']['ts'],
            f"{player_data['video']['hash2']}"
        ],
        "id": 1
    }

    r = requests.post("https://www.cda.pl/", headers=common.HEADERS, data=json.dumps(send_data))
    data = r.json()
    if r.status_code == 200:
        return data['result']['resp']
    else:
        raise CdaDownloadUrlError


def download_video(url, filename):
    wget.download(url, filename)
