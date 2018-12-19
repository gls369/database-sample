import requests
import json
## 用POST讓資料庫多幾筆資料

## data也是要傳的參數，但是是藏在request中的，POST跟GET的不同處

headers = {"Content-Type" : "application/json"}

data = {
	"jobseeker_sID" : "s031005",
	"SalaryExpection" : "22000",
	"Department" : "IT",
	"Skill" : ["python","c","javascript"],
	"wPlace" : ["abc company"],
	"wPosition" : ["programmer"],
	"wStartTime" : "2017-01-17",
	"wEndTime" : "2018-05-21",
	"degree" : ["Diploma"], 
	"school" : ["TKU"], 
	"department" : ["Computer Science"]
}

res = requests.post("http://127.0.0.1:5000/CV", data = json.dumps(data), headers = headers)

print (res.text)

data = {
	"jobseeker_sID" : "s031006",
	"SalaryExpection" : "23000",
	"Department" : "IT",
	"Skill" : ["python","c"],
	"wPlace" : ["bcd company"],
	"wPosition" : ["programmer"],
	"wStartTime" : "2012-12-15",
	"wEndTime" : "2018-05-21",
	"degree" : ["Diploma"], 
	"school" : ["TKU"], 
	"department" : ["Computer Science"]
}

res = requests.post("http://127.0.0.1:5000/CV", data = json.dumps(data), headers = headers)

print (res.text)

data = {
	"jobseeker_sID" : "s031007",
	"SalaryExpection" : "24000",
	"Department" : "IT",
	"Skill" : ["c","javascript"],
	"wPlace" : ["cde company"],
	"wPosition" : ["programmer"],
	"wStartTime" : "2013-01-17",
	"wEndTime" : "2018-08-05",
	"degree" : ["Diploma"], 
	"school" : ["TKU"], 
	"department" : ["Computer Science"]
}

res = requests.post("http://127.0.0.1:5000/CV", data = json.dumps(data), headers = headers)

print (res.text)