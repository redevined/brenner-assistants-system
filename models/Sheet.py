#/usr/bin/env python
# -*- coding: UTF-8 -*-

import pickle
from base64 import b64decode, b64encode
from flask import render_template, url_for, current_app
from flask_weasyprint import HTML, CSS, render_pdf

from utils import Database
from utils import Log
from config import Config


class Sheet() :

	def __init__(self, user, courses, id = None) :
		self.id = id
		self.user = user
		self.courses = courses
		self.filename = u"Auflistung_{0}.pdf".format(user.username)
		self.template = "sheet.html"

	def render(self) :
		html = HTML(string = render_template(
				self.template,
				user = self.user,
				all_courses = self.courses
			),
			encoding = Config.coding
		)
		css = [ CSS(url_for("static", filename = "css/bootstrap.min.css")) ]

		pdf = html.write_pdf(stylesheets = css)
		doc = current_app.response_class(pdf, mimetype = 'application/pdf')
		doc.headers.add('Content-Disposition', 'attachment', filename = self.filename)
		Log.debug("document + response completely rendered")
		#doc = render_pdf(html, stylesheets = css, download_filename = self.filename)
		return doc


def _keys(li) :
	return [ item[0] for item in li ]

def _values(li, key) :
	for item in li :
		if item[0] == key :
			return item[1]

def generate(user, courses, selected, destructive) :
	grouped = list()
	for course in courses :
		day, month, year = course.date.split(".")
		month = Config.Months[month]
		if [month, year] in selected :
			if year not in _keys(grouped) :
				grouped.append((year, list()))
			if month not in _keys(_values(grouped, year)) :
				_values(grouped, year).append((month, list()))
			_values(_values(grouped, year), month).append(course)
			if destructive :
				Database.deleteCourse(user.username, course.id)
	return storeWithId(user, grouped)

def storeWithId(user, courses) :
	data = b64encode(pickle.dumps(courses)).decode(Config.coding)
	id = Database.storeSheetWithId(user.username, data)
	return id

def getById(user, id) :
	data, id = Database.loadSheet(id)
	courses = pickle.loads(b64decode(data))
	sheet = Sheet(user, courses, id)
	return sheet

def deleteById(id) :
	Database.deleteSheet(id)
