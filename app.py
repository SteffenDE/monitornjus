#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)

from flask import Flask, flash, request, render_template, Blueprint
app = Flask(__name__)
import views
import os
import os.path
from modules.code import common
import settings

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from views.frontend import frontend
from views.backend import backend
app.register_blueprint(frontend)
app.register_blueprint(backend)

import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(os.path.abspath(os.path.dirname(__file__))+'/monitornjus.log', maxBytes=10000, backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

if common.readsettings("APPKEY") == "None":
	import binascii
	key = os.urandom(24)
	hexkey = binascii.hexlify(os.urandom(32)).decode()
	common.writesettings("APPKEY", hexkey)
	app.secret_key = hexkey
else:
	app.secret_key = common.readsettings("APPKEY")

if settings.SSL:
	app.config["SSL"] = True

if settings.running_with_iis == True:
	from werkzeug.wsgi import DispatcherMiddleware
	app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {settings.iis_virtual_path: app.wsgi_app})
	app.config["APPLICATION_ROOT"] = settings.iis_virtual_path

####### error #######

@app.errorhandler(400)
def bad_request(error):
	app.logger.error(error)
	return render_template('error/400.html'), 400

@app.errorhandler(401)
def authorization_required(error):
	app.logger.error(error)
	return render_template('error/401.html'), 401

@app.errorhandler(403)
def access_denied(error):
	app.logger.error(error)
	return render_template('error/403.html'), 403

@app.errorhandler(404)
def not_found(error):
	app.logger.error(error)
	flash(request.path)
	return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
	app.logger.error(error)
	import traceback
	if "Warning" in traceback.format_exc():
		return render_template('error/userwarning.html', error=error), 200
	else:
		return render_template('error/500.html', error="\n"+traceback.format_exc().rstrip()), 500

####################

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)