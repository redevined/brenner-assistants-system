#/usr/bin/env python

import psycopg2 as pgsql

from config import Connection


def checkTables() :
	db.execute("SELECT table_name FROM information_schema.tables;")
	tables = [ res[0] for res in db.fetchall() ]
	if "users" not in tables :
		createUserTable()
	if "courses" not in tables :
		createCourseTable()

def createUserTable() :
	print "[WARN] No table 'users' found!"
	db.execute("CREATE TABLE users (username varchar(255) PRIMARY KEY, password varchar(255), role varchar(255));")
	print "[INFO] New table 'users' created."

def createCourseTable() :
	print "[WARN] No table 'courses' found!"
	db.execute("CREATE TABLE courses (id serial PRIMARY KEY, username varchar(255) REFERENCES users (username), name varchar(255), date varchar(255), time varchar(255), role varchar(255));")
	print "[INFO] New table 'courses' created."


def loadUser(un) :
	db.execute("SELECT username, password, role FROM users WHERE username=%s;", (un,))
	return db.fetchone()

def storeUser(user) :
	db.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s);", (user.username, user.password, user.role))

def deleteUser(un) :
	db.execute("DELETE FROM users WHERE username=%s;", (un,))
	deleteCourses(un)

def existsUser(un) :
	return loadUser(un) is not None


def loadCourses(un) :
	db.execute("SELECT id, name, date, time, role FROM courses WHERE username=%s;", (un,))
	return db.fetchall()

def storeCourse(un, course) :
	db.execute("INSERT INTO courses (username, name, date, time, role) VALUES (%s, %s, %s, %s, %s);", (un, course.name, course.date, course.time, user.role))

def deleteCourse(un, id) :
	db.execute("DELETE FROM courses WHERE username=%s and id=%s;", (un, id))

def deleteCourses(un) :
	db.execute("DELETE FROM courses WHERE username=%s;", (un,))


try :
	conn = pgsql.connect(
		database = Connection.path[1:],
		user = Connection.username,
		password = Connection.password,
		host = Connection.hostname,
		port = Connection.port
	)
	db = conn.cursor()
	checkTables()
except Exception as e :
	print "[ERROR] Connection to PostgreSQL database could not be established, please check your connection settings."
	print "[ERROR]     {0}".format(e)
