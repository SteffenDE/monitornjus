#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2015 Steffen Deusch
# Licensed under the MIT license
# MonitorNjus, 28.11.2015 (Version 1.1)

import settings

def check_auth(user, password):
	if settings.auth_type == "simple":
		import hashlib
		password = hashlib.sha512(password).hexdigest()
		if user == settings.simple_auth_user and password == settings.simple_auth_hashed_pw:
			return True
		else:
			return False

	elif settings.auth_type == "ldap":
		import ldap
		authorized = False

		l = ldap.initialize(settings.ldap_url)
		l.set_option(ldap.OPT_REFERRALS, 0)

		try:
			l.simple_bind_s(user+"@"+settings.ldap_domain,unicode(password, "ISO-8859-15"))
		except Exception as e:
			if "invalid credentials" in str(e).lower():
				try:
					l.simple_bind_s(user+"@"+settings.ldap_domain,password)
				except Exception as e:
					if "invalid credentials" in str(e).lower():
						return False
			else:
				raise Exception(e)

		if settings.ldap_auth_type == "list":
			members = settings.ldap_user_list
		elif settings.ldap_auth_type == "group":
			dn, entry = l.search_s(settings.ldap_search_string, ldap.SCOPE_BASE)[0]
			members = entry["member"]
		else:
			raise Exception("Wrong ldap_auth_type! need list or group")

		if user in str(members):
			authorized = True
		
		if authorized:
			return True
		else:
			return False