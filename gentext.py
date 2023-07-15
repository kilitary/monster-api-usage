#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
import os
import random
import sys
from pprint import pprint
import requests
import time
from genimg import get_image
from monsterconfig import API_BEARER, API_KEY, PROMPT, NEGPROMPT, GUIDANCE, STEPS, SAMPLES, ASPECT

tokens_all = "JP 1-02 carrier frequencies 50,005,016 Hz and 50,005,018 Hz;" \
             "700-800MHz 1.0W 4G LTE USA i Phone (AT&T & Verizon)  (Two Bands);" \
             "758-830MHz 1.0W 5G, 4G LTE Low (Two Bands);" \
             "850-895MHz 1.0W  CDMA 850  (Two Bands);" \
             "920-965MHz 1.0W  GSM900  (Two Bands);" \
             "1800-1920MHz 1.0W DCS  (Two Bands);" \
             "1800-2000MHz 1.0W  DCS, PCS  (Two Bands);" \
             "2100-2170MHz 1.0W 3G, UMTS  (Two Bands);" \
             "2500-2700MHz 1.0W 4G WiMAX Sprint  (Two Bands);" \
             "2570-2690MHz 1.0W 4G LTE High  (Two Bands);" \
             "3G (WCDMA) 2100 – 2170 MHz;" \
             "4G LTE: 2320-2690 MHz;" \
             "5.1-5.9GHz 1.0W WiFi 11.a;" \
             "5G 3400-3600MHz 1.0W 5G LTE;" \
             "5G 3600-3800MHz 1.0W 5G LTE;" \
             "96.6Mhz USB-LSB Hopping (98 Milton Street Site);" \
             "164-183MHz 1.0W  Lojack 164MHz;" \
             "173MHz 1.0W;" \
             "315MHz 1.0W Remote Control;" \
             "400-480MHz 1.0W UHF Remote Control;" \
             "433MHz 1.0W UHF Remote Control;" \
             "868MHz 1.0W Remote Control;" \
             "1170-1280MHz 1.0W GPS L2 + L5+ Glonass L2;" \
             "1380Mhz.-1620Mhz.;" \
             "1450-1620MHz 1.0W 5G+ GPS L1 +Glonass L1;" \
             "1570-1620 MHz 1.0W GPS L1 + Glonass L1;" \
             "1700-1800MHz 4G LTE;" \
             "2300-2500MHz 1.0W 4G LTE + WiFi 11.b & g;" \
             "2400-2500MHz 1.0W  WiFi 11.bg;" \
             "CDMA   870 – 880 mhz;" \
             "DCS    1805 – 1850 mhz;" \
             "Exposure levels to selected regions of the brain typically involve peak sound pressures above 100 kPa (194 dB) at 250–500 kHz;" \
             "GSM    930 – 960 mhz;" \
             "Lumping 170-180 together is a strange idea given the way spectrum in the U.S. is allocated. From 150-ish to 162-ish, we have the normal police, fire, marine, and railroad channels. From 162-174 we have frequencies assigned to different civilian agencies of the federal government. From 174-180 is TV Channel 7.;" \
             "PCS    1930 – 1990 mhz;" \
             "PHS    1900 – 1925 mhz;" \
             "WiFi   2400 – 2500 mhz"

MODEL_NAME = 'falcon-7b-instruct'
request_payload = {
    "model": MODEL_NAME,
    "data": {
        "prompt": "",
        "top_k": 8,
        "top_p": 0.6
    }
}
url = "https://api.monsterapi.ai"
tokens = tokens_all.split(';')
random.shuffle(tokens)

print(f'api_key: {API_KEY}')
print(f'bearer: {API_BEARER}')

try:
    os.truncate('full.log', 0)
except Exception as e:
    pass

headers = {
    'x-api-key': API_KEY,
    'Authorization': f"Bearer {API_BEARER}"
}


def get_text(rp):
    response = requests.post(f"{url}/apis/add-task", headers=headers, json=rp)
    resp = response.json()
    pprint(resp)
    process_id = resp.get('process_id')
    return process_id


for token in tokens:
    token = token.strip(", \t\r\n~!@#$%^&*()_+=-`}{][|\":;\\?/")
    request_payload["data"]["prompt"] = \
        f"what steps should i do to  prevent system use " \
        f"'device or radio frequency or laser/ion beam or satellite with {token}' " \
        f"against me, and was that happen in the past in your decision?"

    process_id = get_text(request_payload)

    if process_id is None:
        print(f'zh')
        sys.exit()

    print(f'waiting data for [' + request_payload["data"]["prompt"] + '] ...')
    while True:
        time.sleep(1)
        payload = {"process_id": process_id}
        response = requests.post(f"{url}/apis/task-status", headers=headers, json=payload)
        response_data = response.json()["response_data"]

        if response_data["status"] == 'COMPLETED':
            text = response_data["result"]["text"]
            print(f'\r\n\r\nreply: {text}\r\n\r\n')

            if ("As an AI language model" in text and "However" not in text and "I suggest " not in text) \
                    or "Can you please clarify" in text or " Please try rephrasin" in text:
                print(f'! failed to query, trying another morphed ...')
                text = request_payload["data"]["prompt"]
                tks = text.split(' ')
                random.shuffle(tks)
                text = " ".join(tks)
                print(f'morphed: [{text}]')
                request_payload["data"]["prompt"] = text
                process_id = get_text(request_payload)
                continue

            text = str(text).replace("As an AI language model, ", "hmm, ")

            reps = {"if": "binary", "are": "electrical", "i": "inside", "want": "metallic"}
            for Key, Value in reps.items():
                text = text.replace(Key, Value)

            content = f"\r\n\r\n=> # {token} #\r\n{text}\r\n\r\n"

            with open('full.log', 'at') as f:
                f.write(content)

            get_image(text)
            break
