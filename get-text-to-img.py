#     ■ Copyright (c) 2024 | Axis9 (Umbrella corp. experimental division grouping style)  Right s: res e rv ed
#     ■ kilitary@gmail.com  | deconf@ya.ru | https://twitter.com/CommandmentTwo | https://vk.com/agent1348
#     ■ bus: https://linktr.ee/kilitary
#     ■ mode: Active Counter-TIe
#     ■ Unles s required by applicable law or agreed to in writing, software,
#     √ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied will be "faced" this rule S.
#
import requests
import json

url = "https://api.monsterapi.ai/apis/task-status"

payload = json.dumps({
    "process_id": "e3c6e837-1dec-11ee-bb1a-673a01c56348"
})
headers = {
    'x-api-key': 'pZJENJoUJi9CoHBFJ6di93Ay1LS5eZhr3dWtB5Km',
    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2OTE0NDc2OTMsImlhdCI6MTY4ODg1NTY5"
                     "Mywic3ViIjoiZmViNTVhMmQ0NmY2MWRlMzE5NzQ3NGI3NTcwZWM2YTMifQ.wWse12KVmq2yONKj5a5dEYmg7ApwHBi86ZVvzTmU4PE",
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
