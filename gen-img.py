#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
#
#
import os
import sys
import time
from pprint import pprint

import requests

api_key = '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i'
api_bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlhdCI6MTY4ODg5OTk5NSwic3ViIjoiNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
pid = os.getpid()
print(f'seed: {pid}')
print(f'key: {api_key}')
prompt = "massive black hole located near another dissapeared black hole with high entropy low vacuum field, no self in, high quality image"
print(f'prompt: {prompt}')

payload = {
    "model": "txt2img",
    "data": {
        "prompt": prompt,
        "negprompt": "lowres, worst quality, low quality, jpeg artifacts, bad quality, memes, body horror, doll like, doll",
        "samples": 1,
        "steps": 113,
        "aspect_ratio": "portrait",
        "guidance_scale": 31.5,
        "seed": pid
    }
}

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 python/requests"
headers = {
    'x-api-key': api_key,
    'Authorization': f"Bearer {api_bearer}"
}

url = "https://api.monsterapi.ai/apis/add-task"
reply = requests.post(url, headers=headers, json=payload)
reply = reply.json()
# pprint(reply, compact=True)
process_id = reply.get('process_id')

if process_id is None:
    print(f'{reply["message"]}')
    sys.exit()

print(f'process id: {process_id}')
response = {}
url = "https://api.monsterapi.ai/apis/task-status"
payload = {"process_id": process_id}
print(f'waiting picture ', end='')

while response.get('response_data') is None or response["response_data"]["status"] != 'COMPLETED':
    print('.', end='')
    time.sleep(1)

    r = requests.post(url, headers=headers, json=payload)
    response = r.json()

pprint(response, compact=True)
