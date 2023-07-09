#  √ Copyright (c) 2024 | Axis9 (Umbrella corp. experimental division grouping style)  Right s: res e rv ed
#  √ kilitary@gmail.com  | deconf@ya.ru | https://twitter.com/CommandmentTwo | https://vk.com/agent1348
#  √ bus: https://linktr.ee/kilitary
#  √ mode: Active Counter-TIe
#  √ Unles s required by applicable law or agreed to in writing, software,
#  √ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied will be "faced" this rule S.
#
#
#
#
#
#
import requests
import json
import random
import os
import sys
import time
from pprint import pprint

payload = {
    "model": "txt2img",
    "data": {
        "prompt": "frequency objects",
        "negprompt": "lowres, worst quality, low quality, jpeg artifacts, bad quality, memes, body horror, doll like, doll",
        "samples": 1,
        "steps": 100,
        "aspect_ratio": "landscape",
        "guidance_scale": 35
    }
}

headers = {
    'x-api-key': '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlhdCI6MTY4ODg"
                     "5OTk5NSwic3ViIjoiNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
}

url = "https://api.monsterapi.ai/apis/add-task"
request = requests.post(url, headers=headers, json=payload)
print(request.text)
request = request.json()
process_id = request['process_id']
response = {}
url = "https://api.monsterapi.ai/apis/task-status"

while response.get('response_data') is None or response["response_data"]["status"] != 'COMPLETED':
    print(f'waiting data ...')
    time.sleep(1)
    payload = {"process_id": process_id}

    r = requests.post(url, headers=headers, json=payload)
    response = r.json()
    pprint(response)
