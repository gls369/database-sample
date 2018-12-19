import requests

## 用PUT來嘗試修改資料

## 將 id = 1 的人的名字改成david

data = {
    "name" : "david"
}

res = requests.put("http://127.0.0.1:5000/person/1", data = data)

print (res.text)