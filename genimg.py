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

API_KEY = '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i'
API_BEARER = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlhdCI6MTY4ODg5OTk5NSwic3ViIjo" \
             "iNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
PROMPT = " picture of unlimited self on the background wnile frequencies operating in you" \
    # "yourself on the background, " \
# "high quality, two wires out via 4d axies"
SEED = time.time_ns()
random.seed(SEED)
GUIDANCE = 45
STEPS = 250
SAMPLES = 1


def get_image(prompt):
    print(f'samples={SAMPLES} seed={SEED} guidance={GUIDANCE} steps={STEPS} api_key={API_KEY}')
    print(f'prompt: [{prompt.strip()}]')

    # Prompt and payload
    payload = {
        "model": "txt2img",
        "data": {
            "prompt": prompt,
            "negprompt": "collage, tables, rows, columns, lowres, worst quality, low quality, jpeg artifacts, bad quality, memes, body horror, doll like, doll, charts",
            "samples": SAMPLES,
            "steps": STEPS,
            "aspect_ratio": "landscape",
            "guidance_scale": GUIDANCE,
            "seed": SEED
        }
    }

    ADD_TASK_URL = "https://api.monsterapi.ai/apis/add-task"
    TASK_STATUS_URL = "https://api.monsterapi.ai/apis/task-status"
    headers = {
        'x-api-key': API_KEY,
        'Authorization': f"Bearer {API_BEARER}"
    }

    try:
        response = requests.post(ADD_TASK_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        process_id = response.json().get('process_id')
    except requests.exceptions.RequestException as e:
        print("Error adding task:", e)
        sys.exit(1)
    if process_id is None:
        print(f'{response["message"]}')
        sys.exit(1)

    print(f'ID: {process_id}')
    status_response = {}
    status_payload = {"process_id": process_id}
    what = PROMPT.split(' ')
    what = what[random.randint(0, len(what) - 1)].strip(' ,')
    print(f'Waiting {what} ', end='')
    start_time = time.time()

    while status_response.get('response_data') is None or status_response["response_data"]["status"] != 'COMPLETED':
        print('.', end='')
        time.sleep(0.5)
        try:
            status_request = requests.post(TASK_STATUS_URL, headers=headers, json=status_payload)
            status_request.raise_for_status()  # Raise an exception if the request was unsuccessful
            status_response = status_request.json()
            if status_response["response_data"]["status"] == "FAILED":
                pprint(status_response)
                sys.exit()
        except Exception as e:
            print("\nError checking task status:", e)
            sys.exit(1)

    delta = int(time.time() - start_time)
    print(f' √ in {delta} secs')
    for image in status_response["response_data"]["result"]["output"]:
        print(f'image: {image}')
        image_file = f'{what}_{time.time_ns()}.png'
        print(f'downloading as {image_file} ...')

        try:
            image_request = urllib.request.urlopen(image)
            with Image(file=image_request) as img:
                print('size: ', img.size)
                display(img)
                img.save(filename=os.path.join('images', image_file))
        except Exception as e:
            pprint(e)

    credits_used = str(status_response["response_data"]["credit_used"])
    print(f'credits_used: {credits_used}')
    logging.info(f'what: {what} seed: {SEED} prompt: {PROMPT} image: {image} '
                 f"credits_used: {credits_used} data[{json.dumps(status_response)}]")
