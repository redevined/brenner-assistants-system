#/usr/bin/env python

import os
from flask import Flask, request

from controllers import *
from utils.Interface import ViewInterface
from config import Urls, Logger


app = Flask(__name__)
app.secret_key = os.urandom(32)
app.jinja_env.globals.update(app = ViewInterface())

Logger.set(app.logger)


@app.route(Urls.home)
def home() :
	return HomeController.view()

@app.route(Urls.about)
def about() :
	return HomeController.about()

@app.route(Urls.login, methods = ["GET", "POST"])
def login() :
	if request.method == "POST" :
		return LoginController.login(request.form)
	return LoginController.view()

@app.route(Urls.register, methods = ["GET", "POST"])
def register() :
	if request.method == "POST" :
		return RegisterController.register(request.form)
	return RegisterController.view()

@app.route(Urls.logout)
def logout() :
	return LoginController.logout()

@app.route(Urls.courseAdd, methods = ["POST"])
def courseAdd() :
	return CourseController.add(request.form)

@app.route(Urls.courseDelete, methods = ["POST"])
def courseDelete(id) :
	return CourseController.add(id)

@app.route(Urls.courseUpdate, methods = ["POST"])
def courseUpdate(id) :
	return CourseController.add(id, request.form)

@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(500)
def throw(error) :
	return HomeController.error(error.code)


if __name__ == "__main__" :
	app.run(debug = True)
