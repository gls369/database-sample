import requests
import json

headers = {"Content-Type" : "application/json"}

res = requests.delete("http://127.0.0.1:5000/CV/1")

print (res.text)