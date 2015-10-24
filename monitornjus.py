#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MonitorNjus, 24.10.2015 (Version 1.0.2)

from flask import Flask, url_for, redirect, render_template, g, request, Response, flash, make_response
app = Flask(__name__)
import sqlite3
import os
import os.path
from modules.backend import common
from functools import wraps
import settings
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

if common.readsettings("APPKEY") == "None":
	import binascii
	key = os.urandom(24)
	hexkey = binascii.hexlify(os.urandom(32)).decode()
	common.writesettings("APPKEY", hexkey)
	app.secret_key = hexkey
else:
	app.secret_key = common.readsettings("APPKEY")

if settings.running_with_iis == True:
	from werkzeug.wsgi import DispatcherMiddleware
	iis_app = DispatcherMiddleware(app, {settings.iis_virtual_path: app})
	app.config["APPLICATION_ROOT"] = settings.iis_virtual_path

def raise_helper(msg):
	raise eval(msg)

####### authentication #######

from modules.backend import auth
check_auth = auth.check_auth

def authenticate():
	"""Sends a 401 response that enables basic auth"""
	return Response(render_template('/error/401.html'), 401,
	{'WWW-Authenticate': 'Basic realm="MonitorNjus Admin-Panel"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if settings.auth_enabled:
			auth = request.authorization
			if not auth or not check_auth(auth.username, auth.password):
				return authenticate()
			return f(*args, **kwargs)
		else:
			return f(*args, **kwargs)
	return decorated

@app.errorhandler(400)
def bad_request(error):
	return render_template('error/400.html'), 400

@app.errorhandler(401)
def authorization_required(error):
	return render_template('error/401.html'), 401

@app.errorhandler(403)
def access_denied(error):
	return render_template('error/403.html'), 403

@app.errorhandler(404)
def not_found(error):
	flash(request.path)
	return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
	import traceback
	if "Warning" in traceback.format_exc():
		return render_template('error/userwarning.html', error=error), 200
	else:
		return render_template('error/500.html', error="\n"+traceback.format_exc().rstrip()), 500

@app.route('/')
def index():
	return redirect(url_for('binindex'))

@app.route('/bin/')
def binindex():
	reload(common)
	return render_template('frontend/index.html', common=common, settings=settings)

@app.route('/bin/show')
def binshow():
	from modules.frontend import show
	reload(show)
	geteilt, linksgeteilt, rechtsgeteilt, timeR, timeL, teilung = show.show()
	return render_template('frontend/show.html', common=common, geteilt=geteilt, linksgeteilt=linksgeteilt, rechtsgeteilt=rechtsgeteilt, timeR=timeR, timeL=timeL, teilung=teilung, raise_helper=raise_helper)

@app.route('/bin/contentset')
def bin_contentset():
	from modules.frontend import contentset
	from modules.backend import getytid
	gseite = request.args.get('seite', None)
	gnummer = request.args.get('nummer', None)
	nummer, nextnummer, refreshon, refresh, seite, mseite, typ, url = contentset.contentset(gseite, gnummer)
	return render_template('frontend/contentset.html', common=common, getytid=getytid, nummer=nummer, nextnummer=nextnummer, refreshon=refreshon, refresh=refresh, seite=seite, mseite=mseite, typ=typ, url=url)

@app.route('/bin/triggerrefresh')
def triggerrefresh():
	if settings.triggerrefresh:
		import time
		def events():
			ttime = 0
			while True:
				reload(common)
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

		if settings.running_with_iis:
			reload(common)
			content = int(common.readsettings("REFRESH"))
			if int(content) == 1:
				out = "data: reload\n\n"
				time.sleep(4)
				common.writesettings("REFRESH", "0")
			else:
				out = "data: none\n\n"
			return Response(out, content_type="text/event-stream")
		
		return Response(events(), content_type='text/event-stream')

adminnav = [('../admin/', "Haupteinstellungen"), ('../admin/widgets', "Widgets"), ('../bin/', "Frontend")]

@app.route('/bin/comprollen')
def comprollen():
	url = request.args.get('url', None)
	typ = request.args.get('type', None)
	speed = request.args.get('speed', None)
	return render_template('frontend/comprollen.html', url=url, typ=typ, speed=speed, raise_helper=raise_helper)

@app.route('/admin/')
@requires_auth
def admin_index():
	reload(common)
	from modules.backend import colors
	reload(colors)
	return render_template('admin/index.html', common=common, colors=colors, navigation=adminnav)

@app.route('/admin/widgets')
@requires_auth
def admin_widgets():
	reload(common)
	from modules.backend import colors
	reload(colors)
	return render_template('admin/widgets.html', common=common, colors=colors, navigation=adminnav)

@app.route('/admin/setn', methods=["GET", "POST"])
@requires_auth
def admin_setn():
	from modules.admin import setn

	form1 = request.form
	form2 = request.args
	form = {}
	for item in form1:
		form[item] = form1[item]
	for item in form2:
		form[item] = form2[item]

	refresh = setn.setn(form)
	return render_template('admin/setn.html', refresh=refresh)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)