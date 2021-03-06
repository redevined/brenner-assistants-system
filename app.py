#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, request
from config import Config
from controllers import AdminController, CourseController, HomeController, LoginController, RegisterController, UserController
from models import User
from utils import Log, Patch
from utils.Interface import ViewInterface


# Set up app
app = Flask(__name__)
app.secret_key = Config.secret_key
app.jinja_env.globals.update(_ = ViewInterface())

# Execute eventual startup patches
Patch.execute()


@app.route(Config.Urls.App.home)
def home() :
	return HomeController.view()

@app.route(Config.Urls.App.about)
def about() :
	return HomeController.about()

@app.route(Config.Urls.App.user, methods = ["GET", "POST"])
def user() :
	if request.method == "POST" :
		return UserController.update(request.form)
	return UserController.view()

@app.route(Config.Urls.App.admin, methods = ["GET", "POST"])
def admin() :
	if request.method == "POST" :
		return AdminController.execute(request.form)
	return AdminController.view()


@app.route(Config.Urls.App.login, methods = ["GET", "POST"])
def login() :
	if request.method == "POST" :
		return LoginController.login(request.form)
	return LoginController.view()

@app.route(Config.Urls.App.register, methods = ["GET", "POST"])
def register() :
	if request.method == "POST" :
		return RegisterController.register(request.form)
	return RegisterController.view()

@app.route(Config.Urls.App.logout)
def logout() :
	return LoginController.logout()


@app.route(Config.Urls.App.course_add, methods = ["POST"])
def courseAdd() :
	return CourseController.add(request.form)

@app.route(Config.Urls.App.course_delete + "/<int:id>")
def courseDelete(id) :
	return CourseController.delete(id)

@app.route(Config.Urls.App.course_submit, methods = ["POST"])
def courseSubmit() :
	return CourseController.submit(request.form)

@app.route(Config.Urls.App.sheet_download)
def downloadSheetByCookie() :
	return CourseController.downloadSheet()

@app.route(Config.Urls.App.sheet_download + "/<int:id>")
def downloadSheet(id) :
	return CourseController.downloadSheet(id)

@app.route(Config.Urls.App.sheet_delete + "/<int:id>")
def deleteSheet(id) :
	return CourseController.deleteSheet(id)


@app.errorhandler(403)
def error403(e) :
	return HomeController.error(403, e)

@app.errorhandler(404)
def error404(e) :
	return HomeController.error(404, e)

@app.errorhandler(405)
def error405(e) :
	return HomeController.error(405, e)

@app.errorhandler(500)
def error500(e) :
	return HomeController.error(500, e)


if __name__ == "__main__" :
	app.run(debug = Config.debug)
