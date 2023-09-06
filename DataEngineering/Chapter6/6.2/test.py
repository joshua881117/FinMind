import requests

res = requests.get("http://192.168.66.22:8888/")
print(res.json())