#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# Beilage zu MonitorNjus, 24.10.2015 (Version 1.0.2)

from ..backend import common
reload(common)
from flask import url_for

def updateurl_refresh(Name, GETNAME, Seite, Nummer, widgname, referer, form):
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

def updateaktiv(Name, GETNAME, Seite, Nummer, widgname, hidden, referer):
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
		if val_flag == common.getwidgetinfo(widgname, Nummer, GETNAME):
			pass
		else:
			common.writewidgetinfo(widgname, Nummer, GETNAME, unicode(val_flag))
	else:
		raise Warning("Function updateaktiv: This referer does not exist.")

def update_align(Name, GETNAME, widgname, ID, referer, form):
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

def updatetime(Seite, Nummer, referer, form):
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

def updateteilung(referer, form):
	if "index" in referer:
		teilung = form.get("teilung")
		if teilung is not None:
			if teilung == common.readsettings("TEILUNG"):
				pass
			else:
				common.updatesettings("TEILUNG", teilung)
	else:
		raise Warning("Function updateteilung: This referer is not allowed.")

def setn(form):
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
						updateurl_refresh(item, name, seite, nummer, "", referer, form)
					else:
						if "hidden." in item.lower() and not item[7:] in form:
							hidden = 0
							updateaktiv(item[7:], name[7:], seite, nummer, "", hidden, referer)
						elif "hidden." in item.lower() and item[7:] in form:
							pass
						else:
							hidden = None
							updateaktiv(item, name, seite, nummer, "", hidden, referer)
				else:
					updatetime(seite, nummer, referer, form)
			else:
				updateteilung(referer, form)

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
						update_align(item, art, typ, ID, referer, form)
					else:
						updateurl_refresh(item, art, "", ID, typ, referer, form)
				else:
					if "hidden." in item.lower() and not item[7:] in form:
						hidden = 0
						updateaktiv(item[7:], art[7:], "", ID, typ, hidden, referer)
					elif "hidden." in item.lower() and item[7:] in form:
						pass
					else:
						hidden = None
						updateaktiv(item, art, "", ID, typ, hidden, referer)

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

	common.writesettings("REFRESH", "1")

	return refresh