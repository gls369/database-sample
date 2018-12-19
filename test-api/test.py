import requests


## GET


## params 就是要傳的參數自己設定，每個key對應一個value

params = {
	"key", "value"
}

requests.get("localhost:5000/<API_NAME>", params = params)

## POST

## data也是要傳的參數，但是是藏在request中的，POST跟GET的不同處

data = {
	"key", "value"
}

requests.post("localhost:5000/<API_NAME>", data = data)

## DELETE PUT 以此類推，都用data傳資料