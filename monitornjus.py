#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, render_template, g, request, Response, flash, make_response
app = Flask(__name__)
import sqlite3
import os
import os.path
from modules import common
from functools import wraps
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.secret_key = '\xf9ZNd2\xef\x89\xa8\xe1\x10\x95;\xd6\xdcl\xf3\xed\xfe\xbd\x88 ;\x08O'

####### authentication #######

def check_auth(username, password):
	"""This function is called to check if a username /
	password combination is valid.
	"""
	if username == "johann" and password == "73eb768fe6a4c876aeb9fa99a5abf0d2f201d363db2f3b76d5ccc1ccb96caaa4e9e6fae73804fd0ae97041b4486765ad36619e256488c1ec0adab5e3a15219f2":
		return True
	else:
		return False

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(render_template('401.html'), 401,
	{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, hashlib.sha512(auth.password).hexdigest()):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

@app.errorhandler(400)
def bad_request(error):
	return render_template('400.html'), 400

@app.errorhandler(401)
def authorization_required(error):
	return render_template('401.html'), 401

@app.errorhandler(403)
def access_denied(error):
	return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
	flash(request.path)
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
	import traceback
	return render_template('500.html', error="\n"+traceback.format_exc().rstrip()), 500

@app.route('/')
def index():
	return redirect(url_for('binindex'))

@app.route('/bin/')
def binindex():
	reload(common)
	return render_template('bin_index.html', common=common)

@app.route('/bin/show')
def binshow():
	from modules import checktime
	reload(common)
	rows = common.getrows()
	teilung = int(common.readsettings("TEILUNG"))

	timeL = False
	timeR = False
	geteilt = False
	linksgeteilt = common.getgeteilt("Links")
	rechtsgeteilt = common.getgeteilt("Rechts")

	x = 1
	while x <= rows:
		if checktime.match(common.getinfo("VONBIS", "Links", x),common.datum.now()) and common.getinfo("AKTIV", "Links", x):
			timeL = True
		if checktime.match(common.getinfo("VONBIS", "Rechts", x),common.datum.now()) and common.getinfo("AKTIV", "Rechts", x):
			timeR = True
		if timeL and timeR:
			break
		x = x + 1

	if linksgeteilt and rechtsgeteilt and timeL and timeR:
		geteilt = True
	return render_template('bin_show.html', common=common, geteilt=geteilt, linksgeteilt=linksgeteilt, rechtsgeteilt=rechtsgeteilt, timeR=timeR, timeL=timeL, teilung=teilung)

@app.route('/bin/contentset')
def bin_contentset():
	from modules import checktime
	from modules import getytid
	reload(common)
	gseite = request.args.get('seite', None)
	gnummer = request.args.get('nummer', None)
	rows = common.getrows()
	rand = False
	fadeinzeit = 0.8
	if gseite == "1":
		seite = "1"
		mseite = "Links"
	elif gseite == "2":
		seite = "2"
		mseite = "Rechts"
	else:
		raise Warning("Diese Seite existiert nicht!")
	if gnummer is None:
		x = 0
		while x < rows:
			if checktime.match(common.getinfo("VONBIS", mseite, int(common.minaktiv(mseite))+x),common.datum.now()) == True and common.getinfo("AKTIV", mseite, int(common.minaktiv(mseite))+x) == 1:
				nummer = int(common.minaktiv(mseite))+x
				break
			x += 1
	else:
		nummer = int(gnummer)
	try:
		nummer
	except:
		raise Warning("Es existiert keine aktive Seite oder ein anderer Fehler ist aufgetreten!")
		exit(0)
	url = common.getinfo("URL", mseite, nummer)
	refresh = common.getinfo("REFRESH", mseite, nummer)
	x = 1
	while x < rows or x == 1:
		if nummer < rows and nummer+x <= rows:
			if common.getinfo("AKTIV", mseite, nummer+x) and checktime.match(common.getinfo("VONBIS", mseite, nummer+x),common.datum.now()):
				refreshon = True
				nextnummer = nummer + x
				break
			else:
				refreshon = False
				nextnummer = nummer
		else:
			refreshon = True
			z = 0
			while z < rows:
				if checktime.match(common.getinfo("VONBIS", mseite, int(common.minaktiv(mseite))+z),common.datum.now()) and common.getinfo("AKTIV", mseite, int(common.minaktiv(mseite))+z):
					nextnummer = int(common.minaktiv(mseite))+z
					break
				else:
					nextnummer = nummer
				z += 1
		x += 1
	if common.getinfo("REFRESHAKTIV", mseite, nummer) == 1:
		refreshon = True
	else:
		refreshon = False
	typ = common.checkfiletype(url)
	return render_template('bin_contentset.html', common=common, getytid=getytid, nummer=nummer, nextnummer=nextnummer, refreshon=refreshon, refresh=refresh, seite=seite, mseite=mseite, typ=typ, url=url)

@app.route('/bin/triggerrefresh')
def triggerrefresh():
	import time
	def events():
		ttime = 0
		while True:
			content = int(common.readsettings("REFRESH"))
			if int(content) == 1:
				yield "data: reload\n\n"
				time.sleep(4)
				common.writesettings("REFRESH", "0")
				break
			elif ttime >= 3600:
				break
			else:
				time.sleep(3)

		ttime += 3

	return Response(events(), content_type='text/event-stream')

adminnav = [('../admin/', "Haupteinstellungen"), ('../admin/widgets', "Widgets"), ('../bin/', "Frontend")]

@app.route('/bin/rollen/comprollen')
def comprollen():
	url = request.args.get('url', None)
	typ = request.args.get('type', None)
	speed = request.args.get('speed', None)
	return render_template('comprollen.html', url=url, typ=typ, speed=speed)

@app.route('/admin/')
@requires_auth
def admin_index():
	reload(common)
	from modules import colors
	reload(colors)
	return render_template('admin_index.html', common=common, colors=colors, navigation=adminnav)

@app.route('/admin/widgets')
@requires_auth
def admin_widgets():
	reload(common)
	from modules import colors
	reload(colors)
	return render_template('admin_widgets.html', common=common, colors=colors, navigation=adminnav)

@app.route('/admin/setn', methods=["GET", "POST"])
@requires_auth
def admin_setn():
	def updateurl_refresh(Name, GETNAME, Seite, Nummer, widgname):
		if "index" in referer:
			gval = form.get(Name)
			if gval is not None:
				val = gval
			else:
				val = None
			if val is not None:
				if val == common.getinfo(GETNAME, Seite, Nummer):
					pass
				else:
					common.writeinfo(Seite, Nummer, GETNAME, unicode(val))
		elif "widgets" in referer:
			gval = form.get(Name)
			if gval is not None:
				val = gval
			else:
				val = None
			if val is not None:
				if val == common.getwidgetinfo(widgname, Nummer, GETNAME):
					pass
				else:
					common.writewidgetinfo(widgname, Nummer, GETNAME, unicode(val))
		else:
			raise Warning("Function updateurl_refresh: This referer does not exist.")

	def updateaktiv(Name, GETNAME, Seite, Nummer, widgname, hidden):
		if hidden is None:
			val_flag = 1
		else:
			val_flag = 0

		if "index" in referer:
			if val_flag == common.getinfo(GETNAME, Seite, Nummer):
				pass
			else:
				common.writeinfo(Seite, Nummer, GETNAME, unicode(val_flag))
		elif "widgets" in referer:
			if val_flag == common.getwidgetinfo(widgname, ID, GETNAME):
				pass
			else:
				common.writewidgetinfo(widgname, Nummer, GETNAME, unicode(val_flag))
		else:
			raise Warning("Function updateaktiv: This referer does not exist.")

	def update_align(Name, GETNAME, widgname, ID):
		if "widgets" in referer:
			if form.get(Name):
				val = form.get(Name)
			else:
				val = None
			if val is not None:
				if unicode(val) == common.getwidgetinfo(widgname, ID, GETNAME):
					pass
				else:
					common.writewidgetinfo(widgname, ID, GETNAME, unicode(val))
		else:
			raise Warning("Function update_align: This referer is not allowed.")

	def updatetime(Seite, Nummer):
		if "index" in referer:
			uhrzeit = unicode(form.get("uhrzeit-"+Seite+"-"+unicode(Nummer)))
			wochentag = unicode(form.get("wochentag-"+Seite+"-"+unicode(Nummer)))
			tag = unicode(form.get("tag-"+Seite+"-"+unicode(Nummer)))
			monat = unicode(form.get("monat-"+Seite+"-"+unicode(Nummer)))
			if uhrzeit is None and wochentag is None and tag is None and monat is None:
				pass
			else:
				if uhrzeit is None:
					uhrzeit = "*"
				if wochentag is None:
					wochentag = "*"
				if tag is None:
					tag = "*"
				if monat is None:
					monat = "*"
				common.writeinfo(Seite, Nummer, "VONBIS", uhrzeit+"|"+wochentag+"|"+tag+"|"+monat)
		else:
			raise Warning("Function updatetime: This referer is not allowed.")

	def updateteilung():
		if "index" in referer:
			teilung = form.get("teilung")
			if teilung is not None:
				if teilung == common.readsettings("TEILUNG"):
					pass
				else:
					common.updatesettings("TEILUNG", teilung)
		else:
			raise Warning("Function updateteilung: This referer is not allowed.")

	reload(common)
	form1 = request.form
	form2 = request.args
	form = {}
	for item in form1:
		form[item] = form1[item]
	for item in form2:
		form[item] = form2[item]

	referer = form.get('referer')

	if "index" in referer:
		refresh = url_for('admin_index')

		for item in form:
			if not "teilung" in item and not "referer" in item:
				splitteditem = item.split("-")
				name = splitteditem[0]
				seite = splitteditem[1]
				nummer = splitteditem[2]
				if not "uhrzeit" in item and not "wochentag" in item and not "tag" in item and not "monat" in item:
					if not "aktiv" in name.lower():
						updateurl_refresh(item, name, seite, nummer, "")
					else:
						if "hidden." in item.lower() and not item[7:] in form:
							hidden = 0
							updateaktiv(item[7:], name[7:], seite, nummer, "", hidden)
						elif "hidden." in item.lower() and item[7:] in form:
							pass
						else:
							hidden = None
							updateaktiv(item, name, seite, nummer, "", hidden)
				else:
					updatetime(seite, nummer)
			else:
				updateteilung()

	elif "widgets" in referer:
		refresh = url_for('admin_widgets')

		for item in form:
			if not "referer" in item:
				splitteditem = item.split("-")
				art = splitteditem[0]
				typ = splitteditem[1]
				ID = splitteditem[2]
				if not "aktiv" in art.lower():
					if not "url" in art.lower():
						update_align(item, art, typ, ID)
					else:
						updateurl_refresh(item, art, "", ID, typ)
				else:
					if "hidden." in item.lower() and not item[7:] in form:
						hidden = 0
						updateaktiv(item[7:], art[7:], "", ID, typ, hidden)
					elif "hidden." in item.lower() and item[7:] in form:
						pass
					else:
						hidden = None
						updateaktiv(item, art, "", ID, typ, hidden)

	elif "row" in referer:
		refresh = url_for('admin_index')
		cnum = unicode(form.get("createnum"))
		dnum = unicode(form.get("delnum"))
		if cnum is not None and cnum.isdigit():
			num = int(cnum)
			if num == int(common.getrows())+1:
				common.createrow(num)
			else:
				raise Warning("Neues Displayset - falsche Zahl: "+unicode(num))
		elif dnum is not None and dnum.isdigit():
			num = int(dnum)
			if num <= int(common.getrows()):
				common.delrow(num)
			else:
				raise Warning("Displayset löschen - falsche Zahl: "+unicode(num))

	elif "newwidget" in referer:
		refresh = url_for('admin_widgets')
		if form.get("art") is not None:
			val = unicode(form.get("art"))
		else:
			val = None
		if val is not None:
			if val == "Logo" or val == "Freies_Widget":
				count = list(common.getwidgets())
				ID = int(common.maxid())+1
				common.newwidget(ID, val, val, 0, "placeholder", "bottom", "0px", "center", "0px", "100%", "100%")
			else:
				raise Warning("Falsches Widget: "+val)

	elif "delwidget" in referer:
		refresh = url_for('admin_widgets')
		num = form.get("delnum")
		if num is not None:
			common.removewidget(unicode(num))

	elif "triggerrefresh" in referer:
		refresh = url_for('admin_index')

	return render_template('admin_setn.html', refresh=refresh)

if __name__ == '__main__':
	app.run(host="0.0.0.0")