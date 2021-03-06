#!/usr/bin/env python
# -*- coding: utf-8 -*-
# apache + fastcgi (flup)

import sys
sys.path.insert(0, "/path/to/monitornjus_root_folder")

from flup.server.fcgi import WSGIServer
from app import app

class ScriptNameStripper(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = ''
		return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
	WSGIServer(app).run()