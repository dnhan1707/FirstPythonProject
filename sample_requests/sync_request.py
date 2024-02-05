import requests


response = requests.get('http://127.0.0.1:8000/user/0', headers={})

print(response.json())
