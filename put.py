import requests
import json

## 用PUT來嘗試修改資料

## 將 id = 1 的人的名字改成david
headers = {"Content-Type" : "application/json"}

data = {
    "SalaryExpection" : 500,
	"Department" : 'Washing',
	"Skill" : ['node.js'],
	"wPlace" : ['xdxd company'],
	"wPos" : ['cleaning toliet'],
	"wStartTime" : '2018-01-01',
	"wEndTime" : '2018-01-02',
	"degree" : ['primary school'],
	"school" : ['lol school'],
	"department" : ['M']
}

res = requests.put("http://127.0.0.1:5000/CV/1", data = json.dumps(data), headers = headers)

print (res.text)