#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
#
#

import os
import time
from pprint import pprint

import requests

pid = os.getpid()
print(f'seed: {pid}')

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

headers = {
    'x-api-key': 'PPlTUPyMiqakafycyHAPB9SmjX1mGVb4OTErRdS7',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE2NjQ2NTYsImlhdCI6MT"
                     "Y4OTA3MjY1Niwic3ViIjoiMTBhZjU0MWVmYmZhNGZkMTE4ZjNiNmFmMzVhN2UxZjAifQ.Lbm38b1oa"
                     "zO9buVxr-nXjqIEL0jVmquMZDEZkUyOtjI"
}

url = "https://api.monsterapi.ai/apis/add-task"
reply = requests.post(url, headers=headers, json=payload)
reply = reply.json()
pprint(reply, compact=True)
process_id = reply['process_id']
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
