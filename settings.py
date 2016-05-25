#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MonitorNjus, 28.11.2015 (Version 1.1)
# Settings

#### Settings ####

SSL = True							# <- SSL for Admin-Panel
# <- only enable when NOT running with only 1 handler, e.g. the dev server
triggerrefresh = True

running_with_iis = False 			# <- if running with iis
iis_virtual_path = "/monitornjus" 	# <- if running under a "virtual path"

### Authentication ###

auth_enabled = True 				# True or False
auth_type = "ldap" 					# <- ldap or simple

# if simple
simple_auth_user = "johann"			# user for basic authentication
# password hash: SHA512 -> run python -> import hashlib;
# hashlib.sha512("yourpassword").hexdigest()
simple_auth_hashed_pw = ''

# if ldap
ldap_auth_type = "list" 			# list or group
ldap_url = "ldap://10.1.1.1:389"  # LDAP URL
ldap_domain = "musterschule.schule.paedml"
# <- for group based auth
ldap_search_string = "CN=G_Lehrer_JVG,OU=Active Directory,OU=Sicherheitsgruppen,DC=musterschule,DC=schule,DC=paedml"
ldap_user_list = ["greu", "rupp", "stol",
                  "steffen.deusch"]  # <- only for list auth
