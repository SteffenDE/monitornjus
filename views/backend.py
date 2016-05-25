#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)
# Backend View

from flask import render_template, request, Blueprint
from modules.code import common
import settings
from tools import requires_auth, ssl_required

backend = Blueprint('backend', __name__, template_folder='templates')

adminnav = [('../admin/', "Haupteinstellungen"),
            ('../admin/widgets', "Widgets"), ('../', "Frontend")]


@backend.route('/admin/')
@ssl_required
@requires_auth
def admin_index():
    reload(common)
    from modules.code import colors
    reload(colors)
    return render_template('backend/index.html', common=common, settings=settings, colors=colors, navigation=adminnav)


@backend.route('/admin/widgets')
@ssl_required
@requires_auth
def admin_widgets():
    reload(common)
    from modules.code import colors
    reload(colors)
    return render_template('backend/widgets.html', common=common, colors=colors, navigation=adminnav)


@backend.route('/admin/setn', methods=["GET", "POST"])
@ssl_required
@requires_auth
def admin_setn():
    from modules.backend import setn

    form1 = request.form
    form2 = request.args
    form = {}
    for item in form1:
        form[item] = form1[item]
    for item in form2:
        form[item] = form2[item]

    refresh = setn.setn(form)
    return render_template('backend/setn.html', refresh=refresh)
