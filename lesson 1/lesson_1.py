import requests
import json

url = 'https://api.github.com'
user = 'Max-Zima'

req = requests.get(f'{url}/users/{user}/repos')

j_data = req.json()

with open('data.json', 'w') as f:
    json.dump(j_data, f)

for i in j_data:
    print(i['name'])
