import requests

## 用POST讓資料庫多幾筆資料

## data也是要傳的參數，但是是藏在request中的，POST跟GET的不同處

data = {
    "name" : "apie"
}

res = requests.post("http://127.0.0.1:5000/person", data = data)

print (res.text)

data = {
    "name" : "apie2"
}

res = requests.post("http://127.0.0.1:5000/person", data = data)

print (res.text)

data = {
    "name" : "apie3"
}

res = requests.post("http://127.0.0.1:5000/person", data = data)

print (res.text)