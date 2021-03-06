#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)
# Frontend View

from flask import url_for, render_template, request, Response, flash, make_response, Blueprint
from modules.code import common
import settings
from tools import raise_helper

frontend = Blueprint('frontend', __name__, template_folder='templates')


@frontend.route('/')
def binindex():
    import datetime
    trigger = request.args.get("disabletrigger")
    owndate = request.args.get("owndate")
    return render_template('frontend/index.html', common=common, settings=settings, trigger=trigger, owndate=owndate)


@frontend.route('/show')
def binshow():
    from modules.frontend import show
    reload(show)
    owndate = request.args.get("owndate")
    geteilt, linksgeteilt, rechtsgeteilt, timeR, timeL, teilung = show.show(
        owndate)
    return render_template('frontend/show.html', common=common, geteilt=geteilt, linksgeteilt=linksgeteilt, rechtsgeteilt=rechtsgeteilt, timeR=timeR, timeL=timeL, teilung=teilung, raise_helper=raise_helper, owndate=owndate)


@frontend.route('/contentset')
def bin_contentset():
    from modules.frontend import contentset
    from modules.code import getytid
    owndate = request.args.get("owndate")
    gseite = request.args.get('seite', None)
    gnummer = request.args.get('nummer', None)
    nummer, nextnummer, refreshon, refresh, seite, mseite, typ, url = contentset.contentset(
        gseite, gnummer, owndate)
    return render_template('frontend/contentset.html', common=common, getytid=getytid, nummer=nummer, nextnummer=nextnummer, refreshon=refreshon, refresh=refresh, seite=seite, mseite=mseite, typ=typ, url=url, owndate=owndate)


@frontend.route('/triggerrefresh')
def triggerrefresh():
    if settings.triggerrefresh:
        import time

        def events():
            ttime = 0
            while True:
                try:
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
                        yield "data: none\n\n"
                        time.sleep(3)
                    ttime += 3
                except:
                    break

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

        else:
            return Response(events(), content_type='text/event-stream')
    else:
        return render_template('error/400.html'), 400
