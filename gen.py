#     ■ Copyright (c) 2024 | Axis9 (Umbrella corp. experimental division grouping style)  Right s: res e rv ed
#     ■ kilitary@gmail.com  | deconf@ya.ru | https://twitter.com/CommandmentTwo | https://vk.com/agent1348
#     ■ bus: https://linktr.ee/kilitary
#     ■ mode: Active Counter-TIe
#     ■ Unles s required by applicable law or agreed to in writing, software,
#     √ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied will be "faced" this rule S.
#

import requests
import json
import random
import os
import sys
import time
from pprint import pprint

url = "https://api.monsterapi.ai/apis/add-task"

payload = json.dumps({
    "model": "txt2img",
    "data": {
        "prompt": "image of different frequency operations between self",  # theory where is no such effect like
        "negprompt": "lowres, worst quality, low quality, jpeg artifacts",
        # "negprompt": "lowres, signs, memes, labels, text, food, text, error, mutant, cropped, worst quality, low quality, normal " \
        #             "quality, jpeg artifacts, signature, watermark, username, blurry, made by children, caricature, ugly, boring, sketch, lacklustre, repetitive, cropped, (long neck), facebook, youtube, body horror, out of frame, mutilated, tiled, frame, border, porcelain skin, doll like, doll, bad quality, cartoon, lowres, meme, low quality, worst quality, ugly, disfigured, inhuman",
        "samples": 1,
        "steps": 50,
        "aspect_ratio": "landscape",
        "guidance_scale": 12.5,
        "seed": random.randint(0, 99999999)
    }
})

headers = {
    'x-api-key': 'pZJENJoUJi9CoHBFJ6di93Ay1LS5eZhr3dWtB5Km',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0NDc2OTMsImlhdCI6MTY4ODg1NTY5"
                     "Mywic3ViIjoiZmViNTVhMmQ0NmY2MWRlMzE5NzQ3NGI3NTcwZWM2YTMifQ.wWse12KVmq2yONKj5a5dEYmg7ApwHBi86ZVvzTmU4PE",
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

print(f'waiting to data ...')

time.sleep(20)
url = "https://api.monsterapi.ai/apis/task-status"

response = json.loads(response.text)
pprint(response)
payload = json.dumps({
    "process_id": response['process_id']
})
headers = {
    'x-api-key': 'pZJENJoUJi9CoHBFJ6di93Ay1LS5eZhr3dWtB5Km',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0NDc2OTMsImlhdCI6MTY4ODg1NTY5"
                     "Mywic3ViIjoiZmViNTVhMmQ0NmY2MWRlMzE5NzQ3NGI3NTcwZWM2YTMifQ.wWse12KVmq2yONKj5a5dEYmg7ApwHBi86ZVvzTmU4PE",
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)