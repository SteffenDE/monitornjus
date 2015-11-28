#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)

import os
import os.path
import datetime
import sqlite3

datum = datetime.datetime.now()
version = "1.1&beta;"
workingdir = os.path.dirname(os.path.realpath(__file__))
dbpath = workingdir+'/../MonitorNjus.db'

######################### basics #########################

def raise_helper(message):
	exec('raise '+message)

def getinfo(Info, Seite, Nummer):
	cursor = conn.execute("SELECT "+Info+" FROM DISPLAYSETS WHERE SEITE=? AND NUMMER=?", [unicode(Seite), unicode(Nummer)]);
	return cursor.fetchone()[0]

def writeinfo(Seite, Nummer, Info, value):
	conn.execute("UPDATE DISPLAYSETS SET "+Info+"= ? WHERE SEITE=? AND NUMMER=?", [unicode(value), unicode(Seite), unicode(Nummer)]);
	conn.commit()

def getwidgetinfo(NAME, ID, Info):
	cursor = conn.execute("SELECT "+Info+" FROM WIDGETS WHERE NAME=? and ID=?", [unicode(NAME), unicode(ID)]);
	widgetinfo = cursor.fetchone()[0]
	return widgetinfo

def writewidgetinfo(Name, ID, Info, value):
	conn.execute("UPDATE WIDGETS SET "+Info+" = ? WHERE NAME=? and ID=?", [unicode(value), unicode(Name), unicode(ID)]);
	conn.commit()

def getgeteilt(Seite):
	cursor = conn.execute("SELECT AKTIV FROM DISPLAYSETS WHERE SEITE=\'"+Seite+"\';");
	val = unicode(cursor.fetchall())
	liste = " ".join(val)
	return liste

def minaktiv(Seite):
	cursor = conn.execute("SELECT NUMMER FROM DISPLAYSETS WHERE AKTIV=1 and SEITE=?", [unicode(Seite)]);
	val = cursor.fetchall()
	minval = min(val)
	y = unicode(minval).replace('(','').replace(')','').replace(',','')
	return y

def allaktiv(Seite):
	cursor = conn.execute("SELECT NUMMER FROM DISPLAYSETS WHERE AKTIV=1 and SEITE=?", [unicode(Seite)]);
	val = cursor.fetchall()
	return val

def getrows():
	cursor = conn.execute("SELECT NUMMER FROM DISPLAYSETS WHERE SEITE=\"Links\";");
	val = cursor.fetchall()
	maxval = max(val)
	return maxval[0]

def getallrows():
	cursor = conn.execute("SELECT NUMMER FROM DISPLAYSETS WHERE SEITE=\"Links\";");
	val = unicode(cursor.fetchall())
	liste = val
	return eval(str(liste).replace("(", "").replace(",)", ""))

######################### firstrun #########################

def write(Seite, Nummer, URL, Aktiv, Refreshaktiv, Refresh, vonbis, marginleft, marginright, margintop, marginbottom, connt=False):
	global conn
	if connt:
		conn = connt
	conn.execute("DELETE FROM DISPLAYSETS where SEITE=\'"+Seite+"\' AND NUMMER="+unicode(Nummer)+";");
	conn.execute("INSERT INTO DISPLAYSETS (SEITE,NUMMER,URL,AKTIV,REFRESHAKTIV,REFRESH,VONBIS,MARGINLEFT,MARGINRIGHT,MARGINTOP,MARGINBOTTOM) values (?,?,?,?,?,?,?,?,?,?,?)", \
	[unicode(Seite), unicode(Nummer), unicode(URL), unicode(Aktiv), unicode(Refreshaktiv), unicode(Refresh), unicode(vonbis), unicode(marginleft), unicode(marginright), unicode(margintop), unicode(marginbottom)]);
	conn.commit()

def newwidget(ID, NAME, TYP, AKTIV, URLw, valign, align, vmargin, margin, width, height, connt=False):
	global conn
	if connt:
		conn = connt
	conn.execute("DELETE FROM WIDGETS WHERE ID=?", [unicode(ID)]);
	conn.execute("INSERT INTO WIDGETS (ID,NAME,TYP,AKTIV,URL,valign,align,vmargin,margin,width,height) values ("+str(ID)+",\'"+NAME+"\',\'"+TYP+"\',"+unicode(AKTIV)+",\'"+URLw+"\',\'"+valign+"\',\'"+unicode(align)+"\',\'"+vmargin+"\',\'"+unicode(margin)+"\',\'"+unicode(width)+"\',\'"+unicode(height)+"\')");
	conn.commit()

def firstrun():
	connt = sqlite3.connect(dbpath, check_same_thread=False)
	connt.execute('''CREATE TABLE DISPLAYSETS
		(ID INT PRIMARY KEY,
			SEITE			TEXT,
			NUMMER			INT,
			URL				TEXT,
			AKTIV			INT,
			REFRESH 		INT,
			REFRESHAKTIV 	INT,
			VONBIS			TEXT,
			MARGINLEFT		TEXT,
			MARGINRIGHT		TEXT,
			MARGINTOP		TEXT,
			MARGINBOTTOM	TEXT);''')
	connt.execute('''CREATE TABLE WIDGETS
		(ID INT PRIMARY KEY,
			NAME			TEXT,
			TYP				TEXT,
			AKTIV			INT,
			URL				TEXT,
			valign			TEXT,
			align			TEXT,
			vmargin 		TEXT,
			margin			TEXT,
			width			TEXT,
			height			TEXT);''')
	connt.execute('''CREATE TABLE SETTINGS
		(ID INT PRIMARY KEY,
			NAME			TEXT,
			VALUE			TEXT);''')

	write("Links", 1, "placeholder.html", 1, 1, 60, "*|*|*|*", "0px", "0px", "0px", "0px", connt)
	write("Rechts", 1, "placeholder.html", 1, 1, 60, "*|*|*|*", "0px", "0px", "0px", "0px", connt)
	write("globalmon", 0, "placeholder.html", 1, 1, 3600, "*|*|*|*", "0px", "0px", "0px", "0px", connt)
	write("global", 0, "placeholder.html", 1, 1, 1800, "*|*|*|*", "0px", "0px", "0px", "0px", connt)

	writesettings("TEILUNG", "50", connt)
	writesettings("REFRESH", "0", connt)
	writesettings("APPKEY", "None")
	writesettings("triggerrefresh", "False")

	newwidget(1, "Adminlink", "Adminlink", 1, "placeholder", "bottom", "0px", "center", "0px", "0", "0", connt)
	newwidget(2, "Logo", "Logo", 0, "placeholder", "bottom", "0px", "left", "0px", "100%", "100%", connt)
	newwidget(3, "Freies_Widget", "Freies_Widget", 0, """<iframe name="flipe" scrolling="no" src="http://www.daswetter.com/getwid/ef3e15e299d279eec78fbfc75d5190f6" id="ef3e15e299d279eec78fbfc75d5190f6" style="width: 250px; color: rgb(128, 128, 128); height: 142px;" frameborder="0"></iframe>""", "bottom", "-90px", "right", "145px", "100px", "200px", connt)

	connt.commit()
	connt.close()

######################### Displaysets #########################

def createrow(Nummer):
	write("Links", Nummer, "placeholder.html", 0, 1, 60, "*|*|*|*", "0px", "0px", "0px", "0px")
	write("Rechts", Nummer, "placeholder.html", 0, 1, 60, "*|*|*|*", "0px", "0px", "0px", "0px")

def delrow(Nummer):
	rows = getrows()
	if Nummer is not rows:
		conn.execute("DELETE FROM DISPLAYSETS where NUMMER=?", unicode(Nummer));
		x = rows
		diff = rows - Nummer
		z = 0
		while z < diff:
			conn.execute("UPDATE DISPLAYSETS SET NUMMER = ? where NUMMER= ?", [unicode(Nummer+z), unicode(Nummer+z+1)]);
			conn.commit()
			z = z + 1
	elif Nummer == rows:
		conn.execute("DELETE FROM DISPLAYSETS where NUMMER=?", [unicode(Nummer)]);
		conn.commit()

def writesettings(NAME, VAL, connt=False):
	global conn
	if connt:
		conn = connt
	conn.execute("DELETE FROM SETTINGS where NAME=?", [unicode(NAME)]);
	conn.execute("INSERT INTO SETTINGS (NAME,VALUE) values (\'"+NAME+"\',\'"+VAL+"\');");
	conn.commit()

def updatesettings(NAME, VAL):
	conn.execute("UPDATE SETTINGS SET VALUE=? where NAME=?;", [unicode(VAL), unicode(NAME)]);
	conn.commit()

def readsettings(NAME):
	cursor = conn.execute("SELECT VALUE FROM SETTINGS WHERE NAME=\'"+NAME+"\';");
	return cursor.fetchone()[0]

######################### Widgets #########################

def getwidgets():
	cursor = conn.execute("SELECT ID FROM WIDGETS;");
	erg = cursor.fetchall()
	out = []
	for item in range(0,len(erg)):
		out.append(erg[item][0])
	return out

def getwidgTYPfromID(ID):
	cursor = conn.execute("SELECT TYP FROM WIDGETS WHERE ID=?", [unicode(ID)]);
	return cursor.fetchone()[0]

def maxid():
	cursor = conn.execute("SELECT MAX(ID) FROM WIDGETS;");
	return cursor.fetchone()[0]

def removewidget(ID):
	anz = int(maxid())
	ID = int(ID)
	if ID is not anz:
		conn.execute("DELETE FROM WIDGETS where ID = ?", [unicode(ID)]);
		x = anz
		diff = anz - ID
		z = 0
		while z < diff:
			conn.execute("UPDATE WIDGETS SET ID = ? where ID = ?", [unicode(ID+z), unicode(ID+z+1)]);
			conn.commit()
			z = z + 1
	elif ID == anz:
		conn.execute("DELETE FROM WIDGETS where ID = ?", [unicode(ID)]);
		conn.commit()

######################### other functions #########################

def checkfiletype(datei):
	if ".png" in datei or ".jpg" in datei or ".gif" in datei or ".bmp" in datei or ".jpeg" in datei:
		return "image"
	elif ".mp4" in datei or ".wmv" in datei:
		return "video"
	elif ".pdf" in datei:
		return "pdf"
	elif "youtube" and "watch?v=" in datei:
		return "youtube"
	else:
		return "unknown"

def addpx(string):
	if "px" in unicode(string):
		return unicode(string)
	elif "auto" in unicode(string):
		return unicode(string)
	elif "%" in unicode(string):
		return unicode(string)
	else:
		return unicode(string)+"px"

######################### checkvalues #########################

def testexist(GETNAME, Seite, Nummer):										# Daten aus der Datenbank lesen
	try:
		if getinfo(GETNAME, Seite, Nummer) is not None:
			return getinfo(GETNAME, Seite, Nummer)
		else:
			return "Keine Daten für "+GETNAME
	except:
		return "Keine Daten"

def aktiv(GETNAME, Seite, Nummer):											# Überprüft, ob eine Checkbox aktiviert ist
	try:
		if getinfo(GETNAME, Seite, Nummer) == 1:
			return "checked=\"checked\""
		else:
			return ""
	except:
		return ""

def widgaktiv(widgname, ID):												# Dasselbe wie testexist(), nur für Widgets
	try:
		if getwidgetinfo(widgname, ID, "Aktiv") == 1:
			return "checked=\"checked\""
		else:
			return ""
	except:
		return ""

def valign(widgname, ID, typ):												# Wichtig für die Dropdown Auswahl der Lage von Widgets
	if typ == "valign":
		try:
			if getwidgetinfo(widgname, ID, "valign") == "top":
				return """
										<option value="" disabled selected>top</option>
										<option value="bottom">bottom</option>"""
			elif getwidgetinfo(widgname, ID, "valign") == "bottom":
				return """
										<option value="" disabled selected>bottom</option>
										<option value="top">top</option>"""
		except:
			return """
										<option value="" disabled selected>valign wählen...</option>
										<option value="top">top</option>
										<option value="bottom">bottom</option>"""
	elif typ == "vmargin":
		try:
			if "left" in getwidgetinfo(widgname, ID, "vmargin"):
				return """
												<option value="" disabled selected>left</option>
												<option value="center">center</option>
												<option value="right">right</option>"""
			elif "center" in getwidgetinfo(widgname, ID, "vmargin"):
				return """
												<option value="" disabled selected>center</option>
												<option value="left">left</option>
												<option value="right">right</option>"""
			elif "right" in getwidgetinfo(widgname, ID, "vmargin"):
				return """
												<option value="" disabled selected>right</option>
												<option value="center">center</option>
												<option value="left">left</option>"""
		except:
			return """
												<option value="" disabled selected>Ausrichtung w&aumlhlen...</option>
												<option value="left">left</option>
												<option value="center">center</option>
												<option value="right">right</option>"""

def getdate(value, Seite, Nummer):											# Splittet die Daten in der Datenbank mit Anordnung nach (*|*|*|*)
	timespan = getinfo("VONBIS", Seite, Nummer).split("|")					# in einzelne Werte für Uhrzeit, Wochentag, usw auf, um im Interface
	if value == "uhrzeit":													# getrennt angezeigt zu werden
		return timespan[0]
	elif value == "wochentag":
		return timespan[1]
	elif value == "tag":
		return timespan[2]
	elif value == "monat":
		return timespan[3]
	else:
		return "Fehler"

if not os.path.exists(dbpath):
	firstrun()
conn = sqlite3.connect(dbpath, check_same_thread=False)