import requests

## 用DELETE來嘗試刪除資料

## 將 id = 1 的人刪掉

data = {
    "name" : "david"
}

res = requests.delete("http://127.0.0.1:5000/person/1")

print (res.text)