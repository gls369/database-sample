# 建立資料表欄位
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from app import db
import pickle

class jobseeker(db.Model):
	__tablename__ = 'JobSeeker'
	id = db.Column(db.Integer, primary_key=True)
	sID = db.Column(db.String(80),primary_key=True)
	sName = db.Column(db.String(60))
	sBDate = db.Column(db.Date)
	sTel = db.Column(db.String(60))
	sEmail = db.Column(db.String(60))
	sPw = db.Column(db.String(60))
	sGender = db.Column(db.String(20))
	def __init__(self, sName, sBDate, sTel, sEmail, sPw, sGender):
		self.sName = sName
		self.sBDate = sBDate

class cv(db.Model):
	__tablename__ = 'CV'
	id = db.Column(db.Integer, primary_key=True)
	jobseeker_sID = db.Column(db.String(80))#,db.ForeignKey('JobSeeker.sID'))
	SalaryExpection = db.Column(db.Integer)
	Department = db.Column(db.String(60))
	Skill = db.Column(db.PickleType)
	SubmitDate = db.Column(db.DateTime)

class wExp(db.Model):
	__tablename__ = 'WorkingExperience'
	id = db.Column(db.Integer,primary_key=True)
	cv_ID = db.Column(db.String(60),db.ForeignKey('CV.id'))
	wPlace = db.Column(db.PickleType)
	wPos = db.Column(db.PickleType)
	wStartTime = db.Column(db.Date)
	wEndTime = db.Column(db.Date)

class learningExp(db.Model):
	__tablename__ = 'learningExp'
	id = db.Column(db.Integer,primary_key=True)
	cv_ID = db.Column(db.String(60),db.ForeignKey('CV.id'))
	degree = db.Column(db.PickleType)
	school = db.Column(db.PickleType)
	department = db.Column(db.PickleType)

class company(db.Model):
	__tablename__ = 'Company'
	id = db.Column(db.Integer,primary_key=True)
	cID = db.Column(db.String(60),primary_key=True)
	cName = db.Column(db.String(80))
	cTel = db.Column(db.String(80))
	cCategory = db.Column(db.String(80))
	cCity = db.Column(db.String(80))
	cPw = db.Column(db.String(60))

class job(db.Model):
	__tablename__ = 'Job'
	id = db.Column(db.Integer,primary_key=True)
	c_ID = db.Column(db.String(60),db.ForeignKey('Company.cID'))
	Salary = db.Column(db.Integer)
	cPos = db.Column(db.String(80))
	cNeededSkill = db.Column(db.PickleType)
	cPickeds = db.Column(db.PickleType)
