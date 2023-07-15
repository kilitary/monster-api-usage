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
from monsterconfig import API_BEARER, API_KEY, PROMPT, NEGPROMPT, GUIDANCE, STEPS, SAMPLES, ASPECT

logging.basicConfig(
    filename='monsterapi-img.log',
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s|%(message)s'
)

SEED = time.time_ns()
random.seed(SEED)
prev_ee = 0


def get_image(prompt):
    prompt = prompt.strip(", \t\r\n~!@#$%^&*()_+=-`}{][|\":;\\?/")
    print(f'samples={SAMPLES} seed={SEED} guidance={GUIDANCE} steps={STEPS} api_key={API_KEY}')
    # print(f'bearer: {API_BEARER}')
    print(f'prompt: [{prompt}]')
    print(f'cprompt: [{NEGPROMPT}]')

    payload = {
        "model": "txt2img",
        "data": {
            "prompt": prompt,
            "negprompt": NEGPROMPT,
            "samples": SAMPLES,
            "steps": STEPS,
            "aspect_ratio": ASPECT,
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
    srcwhat = prompt.split(' ')
    dstwhat = srcwhat[random.randint(0, len(srcwhat) - 1)].strip(' ,')
    print(f'=> {dstwhat}-', end='')
    start_time = time.time()
    while status_response.get('response_data') is None or status_response["response_data"]["status"] != 'COMPLETED':
        def get_object_self():
            global prev_ee
            object0 = prev_ee
            while object0 == prev_ee or object0 == "" or object0 is None:
                object0 = srcwhat[random.randint(0, len(srcwhat) - 1)].strip(' ,')
            prev_ee = object0
            return object0

        object0 = get_object_self()
        print(f'{object0}', end='')
        if random.randint(0, 54) % 5 == 0:
            object0 = get_object_self()
            print(f"\n=> {object0}", end='')

        c = '+' if random.randint(0, 1) == 1 else '-'
        print(c, end='')

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
    credits_used = 0
    for image in status_response["response_data"]["result"]["output"]:
        print(f'image: {image}')
        image_file = f'{dstwhat}_{time.time_ns()}.png'
        print(f'downloading as {image_file} ...')

        try:
            image_request = urllib.request.urlopen(image)
            with Image(file=image_request) as img:
                print('size: ', img.size)
                display(img)
                os.makedirs(os.path.join('images', dstwhat), exist_ok=True)
                img.save(filename=os.path.join('images', dstwhat, image_file))
        except Exception as e:
            pprint(e)
        credits_used += status_response["response_data"]["credit_used"]
        logging.info(f"what: {dstwhat} seed: {SEED} prompt: {prompt} image: {image} "
                     f"data[{json.dumps(status_response)}]")
    print(f'credits_used: {credits_used}')


if __name__ == "__main__":
    get_image(PROMPT)
