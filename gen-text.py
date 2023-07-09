import requests
from pprint import pprint
import time

url = "https://api.monsterapi.ai/apis/add-task"

payload = {
    "model": "falcon-7b-instruct",
    "data": {
        "prompt": "Write an article about human electronic sense.",
        "top_k": 5,
        "top_p": 0.1
    }
}
headers = {
    'x-api-key': '5jbyNSSpNV3rIcnXM6jpg8m9IZe33XbVWmwAgI8i',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0OTE5OTUsImlhdCI6MTY4ODg"
                     "5OTk5NSwic3ViIjoiNzA1MTUzOTczYzZjYjg0NTlmYjRlODg2YjNmMjcyMTQifQ.MQ8ubkvk58S39wyg26sQ-CHtbuu4_Y-xVgKHe2TUG4s"
}

response = requests.request("POST", url, headers=headers, json=payload)

pprint(response.text)
request = response.json()
process_id = request['process_id']
url = "https://api.monsterapi.ai/apis/task-status"
response = {}

while response.get('response_data') is None or response["response_data"]["status"] != 'COMPLETED':
    print(f'waiting data ...')
    time.sleep(1)
    payload = {"process_id": process_id}

    r = requests.post(url, headers=headers, json=payload)
    response = r.json()

    if response["response_data"]["status"] == 'COMPLETED':
        text = response["response_data"]["result"]["text"]

        print(text)
