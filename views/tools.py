#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)
# View Tools

import settings
from flask import request, Response, render_template, current_app, redirect
from functools import wraps
from modules.code import auth
check_auth = auth.check_auth


def raise_helper(msg):
    raise eval(msg)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(render_template('error/401.html'), 401,
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


def ssl_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

    return decorated_view
