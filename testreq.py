import requests


url = "http://localhost:5000/3cx"

payload = { "phone": 698794950 ,
           
           "Name": "Test User"}


res = requests.post(url, json=payload)

print("H apanthsh:", res.json())