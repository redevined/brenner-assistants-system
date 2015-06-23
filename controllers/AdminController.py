#/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import abort, flash, redirect, render_template

from models import User
from utils import Database
from config import Urls, Msgs


def view(query = "SELECT table_name FROM information_schema.tables;", res = None) :
	if User.session.exists() :
		if User.session.get().isAdmin() :
			return render_template("admin.html", query = query, result = res)
		else :
			abort(403)
	return redirect(Urls.home)

def execute(form) :
	query = form.get("query")
	res = None
	try :
		res = Database.exeq(query)
	except Exception as e :
		flash(e.message, Msgs.error)
	else :
		flash(u"Befehl erfolgreich ausgeführt!", Msgs.success)
	return view(query, res)
