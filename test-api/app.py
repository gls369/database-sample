from flask import Flask, render_template
from flask import Response, current_app, url_for
from flask import stream_with_context
from flask import request, jsonify, json, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import traceback


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'  ## 我們用sqlite所以直接讀取DB即可
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Person


## 抓值時建議用一個module(這邊沒寫到)或function來回傳整個程式會比較有獨立性

def getpersonbyname(name) :
    try :
        p = Person.query.filter_by(name = name).first()
        name = p.name
        id = p.id
        response = {
            "id" : id,
            "name" : name
        }
        print (response)
        return jsonify({"status": "success", "results": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})

@app.route("/person", methods = ["GET"])
def getperson():
    try :
        id = request.args.get("id")
        name = request.args.get("name")
        if id != None :        ## 偵測到參數內有id，這邊的功能跟59行的route一樣，兩種方式都能寫，選你們覺得好用的寫
            return getpersonbyid(id)
        elif name != None :    ## 偵測到參數內有name就去抓 name = 傳來的參數值 的資料
            return getpersonbyname(name)  
        res = Person.query.all()
        response = []
        for r in res :
            name = r.name
            id = r.id
            response.append({"id":id, "name": name})
        print (response)
        return jsonify({"status": "success", "results": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})

@app.route("/person/<int:id>", methods = ["GET"])
def getpersonbyid(id):
    try :
        p = Person.query.filter_by(id = id).first()
        
        name = p.name
        id = p.id
        response = {
            "id" : id,
            "name" : name
        }
        print (response)
        return jsonify({"status": "success", "results": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})

@app.route("/person", methods = ["POST"])
def addperson():
    try :
        name = request.form.get("name")
        db.session.add(Person(name=name))
        db.session.commit()
        return jsonify({"status": "success", "name": name})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})

@app.route("/person/<int:id>", methods = ["PUT"])
def updateperson(id) :
    try :
        name = request.form.get("name")
        Person.query.get(id).name = name
        db.session.commit()
        return jsonify({"status": "success", "name": name, "id" : id})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})

@app.route("/person/<int:id>", methods = ["DELETE"])
def deleteperson(id) :
    try :
        p = Person.query.filter_by(id = id).first()
        name = p.name
        db.session.delete(p)
        db.session.commit()
        return jsonify({"status": "success", "name": name, "id" : id})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "fail"})