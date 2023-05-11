import requests
import json

api_url = "http://0.0.0.0/state_device/get/led"
response = requests.get(api_url)
data = json.loads(response.json()['data'])[0]['state']
print(data)


# state =  json.loads(response.json())
# print(state['data']['state'])