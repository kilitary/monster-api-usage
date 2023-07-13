#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
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
        "prompt":"multiple  unstable wires near massive black hole , only three objects loading and no  out or waves around  from self",
        "negprompt": "lowres, worst quality, low quality, jpeg artifacts, bad quality, memes, body horror, doll like, doll",
        "samples": 1,
        "steps": 500,
        "aspect_ratio": "portrait",
        "guidance_scale": 32.5,
        "seed": os.getpid()
    }
}

headers = {
    'x-api-key': 'PPlTUPyMiqakafycyHAPB9SmjX1mGVb4OTErRdS7',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE2NjQ2NTYsImlhdCI6MT"
                     "Y4OTA3MjY1Niwic3ViIjoiMTBhZjU0MWVmYmZhNGZkMTE4ZjNiNmFmMzVhN2UxZjAifQ.Lbm38b1oa"
                     "zO9buVxr-nXjqIEL0jVmquMZDEZkUyOtjI"
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
