from flask import Flask, render_template
from flask import Response, current_app, url_for
from flask import stream_with_context
from flask import request, jsonify, json, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
from sqlalchemy import or_, and_
import os
import traceback
import pickle

app = Flask(__name__)
# 設定資料庫位置，並建立 app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CV.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

migrate = Migrate(app, db)
from model import *


@app.route("/CV",methods=['POST'])
#新增
def insert_cv():
	try:
		res = request.json
		jobseeker_sID = res['jobseeker_sID']#request.form.get('jobseeker_sID')
		CV = cv(jobseeker_sID = jobseeker_sID)
		CV.SalaryExpection = res["SalaryExpection"]#request.form.get('SalaryExpection')
		CV.Department = res["Department"]#request.form.get('Department')
		sk = res['Skill']#request.form.get('Skill')
		CV.Skill = pickle.dumps(sk)
		CV.SubmitDate = datetime.now()
		db.session.add(CV)
		db.session.commit()
		cv_ID = CV.id
		wPlace = res['wPlace']#request.form.get('wPlace')
		wpl = pickle.dumps(wPlace)
		wPos = res['wPosition']#request.form.get('wPosition')
		wpo = pickle.dumps(wPos)
		wStartTime = res['wStartTime']#request.form.get('wStartTime')
		s_time = wStartTime.split("-")
		wStartTime = date(int(s_time[0]), int(s_time[1]), int(s_time[2]))
		wEndTime = res['wEndTime']#request.form.get('wEndTime')
		e_time = wEndTime.split("-")
		wEndTime = date(int(e_time[0]), int(e_time[1]), int(e_time[2]))
		w = wExp(cv_ID = cv_ID, wPlace = wpl, wPos = wpo, wStartTime = wStartTime, wEndTime = wEndTime)
		degree = res['degree']#request.form.get('degree')
		deg = pickle.dumps(degree)
		school = res['school']#request.form.get('school')
		sc = pickle.dumps(school)
		department = res['department']#request.form.get('department')
		dep = pickle.dumps(department)
		lexp = learningExp(cv_ID = cv_ID, degree = deg, school = sc, department = dep)
		db.session.add(w)
		db.session.add(lexp)
		db.session.commit()
		return jsonify({"status" : "success"})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail" })


@app.route("/CV",methods=['GET'])
def search_cv():
	try:
		res = list()

		if request.args :
			salary_top = request.args.get('salary_top')
			salary_bottom = request.args.get('salary_bottom')
			skill = request.args.getlist('skill')
			TempCV = cv.query.all()
			CV = list()
			if salary_top != None and salary_bottom != None :
				for c in TempCV :
					if c.SalaryExpection >= int(salary_bottom) and c.SalaryExpection <= int(salary_top) :
						CV.append(c)
				TempCV = list(CV)
			if request.args.get('skill') != None:
				for c in TempCV :
					if not set(pickle.loads(c.Skill)).intersection(skill) :
						CV.remove(c)
		else:
			CV = cv.query.all()
		for c in CV :
			id = c.id
			jobseeker_sID = c.jobseeker_sID
			SalaryExpection = c.SalaryExpection
			Department = c.Department
			skill = c.Skill
			sk = pickle.loads(skill)
			SubmitDate = c.SubmitDate
			WEXP = wExp.query.filter_by(cv_ID = id).first()
			wPlace = WEXP.wPlace
			wpl = pickle.loads(wPlace)
			wPos = WEXP.wPos
			wpo = pickle.loads(wPos)
			wStartTime = WEXP.wStartTime
			wEndTime = WEXP.wEndTime
			LE = learningExp.query.filter_by(cv_ID = id).first()
			degree = LE.degree
			deg = pickle.loads(degree)
			school = LE.school
			sc = pickle.loads(school)
			department = LE.department
			dep = pickle.loads(department)
			res.append({
				"id" : id,
				"jobseeker_sID" : jobseeker_sID,
				"SalaryExpection" : SalaryExpection,
				"Department" : Department,
				"Skill" : sk,
				"SubmitDate" : SubmitDate,
				"wPlace" : wpl,
				"wPos" : wpo,
				"wStartTime" : wStartTime,
				"wEndTime" : wEndTime,
				"degree" : deg,
				"school" : sc,
				"department" : dep
			})
		return jsonify({"status": "success", "response": res})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})

		


@app.route("/CV/<int:id>",methods=['GET'])
#顯示自己的cv
def show_cv_own(id):
	try:
		res = list()
		c = cv.query.filter_by(id = id).first()
		jobseeker_sID = c.jobseeker_sID
		SalaryExpection = c.SalaryExpection
		Department = c.Department
		skill = c.Skill
		sk = pickle.loads(skill)
		SubmitDate = c.SubmitDate
		WEXP = wExp.query.filter_by(cv_ID = id).first()
		wPlace = WEXP.wPlace
		wpl = pickle.loads(wPlace)
		wPos = WEXP.wPos
		wpo = pickle.loads(wPos)
		wStartTime = WEXP.wStartTime
		wEndTime = WEXP.wEndTime
		LE = learningExp.query.filter_by(cv_ID = id).first()
		degree = LE.degree
		deg = pickle.loads(degree)
		school = LE.school
		sc = pickle.loads(school)
		department = LE.department
		dep = pickle.loads(department)
		res.append({
			"id" : id,
			"jobseeker_sID" : jobseeker_sID,
			"SalaryExpection" : SalaryExpection,
			"Department" : Department,
			"Skill" : sk,
			"SubmitDate" : SubmitDate,
			"wPlace" : wpl,
			"wPos" : wpo,
			"wStartTime" : wStartTime,
			"wEndTime" : wEndTime,
			"degree" : deg,
			"school" : sc,
			"department" : dep
		})
		return jsonify({"status": "success", "response": res})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})


@app.route("/CV/<int:id>",methods=["PUT"])
#更新cv
def update_cv(id):
	try:
		req = request.json
		res = list()
		CV = cv.query.filter_by(id = id).first()
		se = req['SalaryExpection']#request.form.get('SalaryExpection')
		CV.SalaryExpection = se
		dep = req['Department']#request.form.get('Department')
		CV.Department = dep
		sk = req['Skill']#request.form.get('Skill')
		Skill = pickle.dumps(sk)
		CV.Skill = Skill
		submitdate = datetime.now()
		CV.SubmitDate = submitdate
		'''
		WEXP = wExp.query.filter_by(cv_ID = id).first()
		wPlace = req['wPlace']#request.form.get("wPlace")
		WEXP.wpl = pickle.dumps(wPlace)
		wPos = req['wPos']#request.form.get("wPos")
		WEXP.wpo = pickle.dumps(wPos)
		wStartTime = req['wStartTime']#request.form.get('wStartTime')
		s_time = wStartTime.split("-")
		WEXP.wStartTime = date(int(s_time[0]), int(s_time[1]), int(s_time[2]))
		wEndTime = req['wEndTime']#request.form.get('wEndTime')
		e_time = wEndTime.split("-")
		WEXP.wEndTime = date(int(e_time[0]), int(e_time[1]), int(e_time[2]))
		le = learningExp.query.filter_by(id = id).first()
		degree = req['degree']#request.form.get('degree')
		le.deg = pickle.dumps(degree)
		school = req['school']#request.form.get('school')
		le.sc = pickle.dumps(school)
		department = req['department']#request.form.get('department')
		le.dep = pickle.dumps(department)
		'''
		wpl = req['wPlace']
		wExp.query.get(id).wPlace = pickle.dumps(wpl)
		wpo = req['wPos']
		wExp.query.get(id).wPos = pickle.dumps(wpo)
		wStartTime = req['wStartTime']
		s_time = wStartTime.split("-")
		wExp.query.get(id).wStartTime = date(int(s_time[0]), int(s_time[1]), int(s_time[2]))
		wEndTime = req['wEndTime']
		e_time = wEndTime.split("-")
		wExp.query.get(id).wEndTime = date(int(e_time[0]), int(e_time[1]), int(e_time[2]))
		deg = req['degree']
		learningExp.query.get(id).degree = pickle.dumps(deg)
		sc = req['school']
		learningExp.query.get(id).school = pickle.dumps(sc)
		dep = req['department']#request.form.get('department')
		learningExp.query.get(id).department = pickle.dumps(dep)
		db.session.commit()
		return jsonify({"status": "success"})

		flash("Your CV has been updated!")
		
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})

'''
@app.route("/wExp",methods=["PUT"])
#更新工作經驗
def update_wexp():
	id = request.form.get("id")
	wPlace = request.form.get("wPlace")
	wPos = request.form.get("wPos")
	wStartTime = request.form.get("wStartTime")
	wEndTime = request.form.get("wEndTime")
	try:
		res = list()
		wexp = wExp.query.filter_by(id = id).first()
		wpl = pickles.dumps(wPlace)
		wexp.wPlace = wpl
		wpo = pickles.dumps(wPos)
		wexp.wPos = wpo
		wexp.wStartTime = wStartTime
		wexp.wEndTime = wEndTime
		res = {
			"wPlace" : wpl,
			"wPos" : wpo,
			"wStartTime" : wStartTime,
			"wEndTime" : wEndTime
		}
		db.commit()
		return jsonify({"status" : "success", "response" : res})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})

#problem: 多個學歷
@app.route("/leaningExp",methods=["PUT"])
#更新學歷
def update_le():
	id = request.form.get("id")
	degree = request.form.get("degree")
	school = request.form.get("school")
	department = request.form.get("department")
	try:
		res = list()
		le = leaningExp.query.filter_by(id = id).first()
		deg = pickle.dumps(degree)
		le.degree = deg
		sc = pickle.dumps(school)
		le.school = sc
		dep = pickle.dumps(department)
		le.department = dep
		res = {
			"degree" : deg,
			"school" : sc,
			"department" : dep
		}
		db.commit()
		return jsonify({"status" : "success", "response" : res})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})
'''


@app.route("/Request/delete",methods=["POST"])
def update_boss_request(id):
	try:
		pass
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass


@app.route("/CV/<int:id>", methods=["DELETE"])
def delete_employee_cv(id):
	try:
		delete_id = cv.query.filter_by(id=id).first()
		db.session.delete(delete_id)
		db.session.commit()
		return jsonify({"status": "success"})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})

@app.route("/Request/delete",methods=["POST"])
def delete_boss_request(id):
	try:
		delete_request = Request.query.filter_by(id=id)
		db.session.delete(delete_request)
		db.session.commit()
		return jsonify({"status": "success"})
	except Exception as e:
		traceback.print_exc()
		return jsonify({"status": "fail"})
		