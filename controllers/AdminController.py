#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import abort, flash, redirect, render_template
from config import Config
from models import User
from utils import Database, Log


def view(query = u"SELECT * FROM users; -- or courses, sheets", res = None) :
	if User.session.exists() :
		if User.session.get().isAdmin() :
			return render_template("admin.html", query = query, result = res)
		else :
			return abort(403)
	return redirect(Config.Urls.App.home)

def execute(form) :
	query = form.get("query")
	res = None
	try :
		res = Database.exeq(query)
	except Exception as e :
		flash(e, Config.Flash.error)
	else :
		flash(u"Befehl erfolgreich ausgeführt!", Config.Flash.success)
	return view(query, res)
