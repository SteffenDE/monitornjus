#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)

from ..code import checktime
from ..code import getytid
from ..code import common
reload(common)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def contentset(gseite, gnummer, owndate):
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
		while x < rows and x+int(common.minaktiv(mseite)) <= rows:
			if checktime.match(common.getinfo("VONBIS", mseite, int(common.minaktiv(mseite))+x),(common.datum.now() if owndate == None else common.datum.strptime(owndate, '%Y-%m-%d-%H-%M'))) == True and common.getinfo("AKTIV", mseite, int(common.minaktiv(mseite))+x) == 1:
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
			if common.getinfo("AKTIV", mseite, nummer+x) and checktime.match(common.getinfo("VONBIS", mseite, nummer+x),(common.datum.now() if owndate == None else common.datum.strptime(owndate, '%Y-%m-%d-%H-%M'))):
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
				if checktime.match(common.getinfo("VONBIS", mseite, int(common.minaktiv(mseite))+z),(common.datum.now() if owndate == None else common.datum.strptime(owndate, '%Y-%m-%d-%H-%M'))) and common.getinfo("AKTIV", mseite, int(common.minaktiv(mseite))+z):
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

	return nummer, nextnummer, refreshon, refresh, seite, mseite, typ, url