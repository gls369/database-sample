import requests
## 用GET來取得所有資料或者單一筆資料

res = requests.get("http://127.0.0.1:5000/CV")  ## 全部

print (res.text)


res = requests.get("http://127.0.0.1:5000/CV/3") ## id = 2

print (res.text)

params = {
	"salary_top" : 22000,
	"salary_bottom" : 0,
	"skill" : ["python"]
}

"""

    get的參數使用params來傳(get無法使用跟post一樣的'data'來傳送)，他會顯示在url上，以下面的url當作範例
    會變成 : http://127.0.0.1:5000/person?id=2
    但POST使用data來傳送參數則不會出現在url上

"""

res = requests.get("http://127.0.0.1:5000/CV", params = params)  ## GET傳送參數取得 id = 2 的人

print (res.text)
