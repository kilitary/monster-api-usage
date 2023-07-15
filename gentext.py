#  Copyright (c) 2024/Axis9 (Umbrella corp. experimental division grouping style) | kilitry@gmail.com | https://linktr.ee/kilitary
import os
import random
import sys
from pprint import pprint
import requests
import time
from genimg import get_image

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
             "3G (WCDMA) 2100 – 2170 Мгц;" \
             "4G LTE: 2320-2690 Мгц;" \
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

API_KEY = '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i'
API_URL = 'https://api.monsterapi.ai/apis'
MODEL_NAME = 'falcon-7b-instruct'
REQUEST_PAYLOAD = {
    "model": MODEL_NAME,
    "data": {
        "prompt": "",
        "top_k": 10,
        "top_p": 0.7
    }
}

tokens = tokens_all.split(';')
random.shuffle(tokens)
os.truncate('full.txt', 0)
headers = {
    'x-api-key': API_KEY,
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlh"
                     "dCI6MTY4ODg5OTk5NSwic3ViIjoiNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQ"
                     "ifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
}

for token in tokens:
    REQUEST_PAYLOAD["data"]["prompt"] = f"what criminal can do with {token}"

    response = requests.post(f"{API_URL}/add-task", headers=headers, json=REQUEST_PAYLOAD)
    resp = response.json()
    process_id = resp.get('process_id')
    if process_id is None:
        pprint(resp)
        sys.exit()

    print(f'waiting data for [{token}] ...')
    while True:
        time.sleep(1)
        payload = {"process_id": process_id}
        response = requests.post(f"{API_URL}/task-status", headers=headers, json=payload)
        response_data = response.json()["response_data"]

        if response_data["status"] == 'COMPLETED':
            text = response_data["result"]["text"]
            print(f'reply: {text}')

            content = f"\r\n#{token}\r\n\r\n{text}"
            with open('full.txt', 'at') as f:
                f.write(content)

            get_image(text)
            break
