#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
import json
import logging
import os
import random
import urllib
import urllib.request as urllib2
from pprint import pprint

import requests
import sys
import time
from wand.display import display
from wand.image import Image

logging.basicConfig(
    filename='monsterapi-img.log',
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(message)s'
)
api_key = '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i'
api_bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlhdCI6MTY4ODg5OTk5NSwic3ViIjo" \
             "iNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
prompt = " image of different frequencys operated by you" \
    # "yourself on the background, " \
# "high quality, two wires out via 4d axies"
seed = time.time_ns()
random.seed(seed)
guidance = 35.5
steps = 233

print(f'seed: {seed}')
print(f'guidance: {guidance}')
print(f'steps: {steps}')
print(f'api_key: {api_key}')
print(f'prompt: {prompt}')

# Prompt and payload
payload = {
    "model": "txt2img",
    "data": {
        "prompt": prompt,
        "negprompt": "lowres, worst quality, low quality, jpeg artifacts, bad quality, memes, body horror, doll like, doll",
        "samples": 1,
        "steps": steps,
        "aspect_ratio": "landscape",
        "guidance_scale": guidance,
        "seed": seed
    }
}

add_task_url = "https://api.monsterapi.ai/apis/add-task"
task_status_url = "https://api.monsterapi.ai/apis/task-status"
headers = {
    'x-api-key': api_key,
    'Authorization': f"Bearer {api_bearer}"
}

try:
    reply = requests.post(add_task_url, headers=headers, json=payload)
    reply.raise_for_status()  # Raise an exception if the request was unsuccessful
    process_id = reply.json().get('process_id')
except requests.exceptions.RequestException as e:
    print("Error adding task:", e)
    sys.exit(1)
if process_id is None:
    print(f'{reply["message"]}')
    sys.exit(1)

print(f'Process ID: {process_id}')
response = {}
payload = {"process_id": process_id}
what = prompt.split(' ')
what = what[random.randint(0, len(what) - 1)].strip(' ,')
print(f'Waiting {what} ', end='')
sec_start = time.time()

while response.get('response_data') is None or response["response_data"]["status"] != 'COMPLETED':
    print('.', end='')
    time.sleep(0.005)
    try:
        r = requests.post(task_status_url, headers=headers, json=payload)
        r.raise_for_status()  # Raise an exception if the request was unsuccessful
        response = r.json()
        if response["response_data"]["status"] == "FAILED":
            pprint(response)
    except Exception as e:
        print("\nError checking task status:", e)
        # pprint(response)
        sys.exit(1)

delta = int(time.time() - sec_start)
print(f' in {delta} secs')
# print(f'{type(response)} {response}')
image = response["response_data"]["result"]["output"][0]
print(f'image: {image}')
image_file = f'{what}_{time.time()}.png'
print(f'downloading as {image_file} ...')

try:
    re = urllib.request.urlopen(image)
    with Image(file=re) as img:
        print('size: ', img.size)
        display(img)
        img.save(filename=os.path.join('images', image_file))
except Exception as e:
    pprint(e)

credits_used = str(response["response_data"]["credit_used"])
print(f'credits_used: {credits_used}')
logging.info(
    f'what: {what} seed: {seed} prompt: {prompt} image: {image} credits_used: {credits_used} data[{json.dumps(response)}]')
