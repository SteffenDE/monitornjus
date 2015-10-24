# -*- coding: utf-8 -*-

#### Settings ####

triggerrefresh = False				# <- only enable when NOT running with only 1 handler, e.g. the dev server

running_with_iis = False 			# <- if running with iis
iis_virtual_path = "/monitornjus" 	# <- if running under a "virtual path"

### Authentication ###

auth_enabled = False				# True or False
auth_type = "simple" 				# <- ldap or simple

## if simple
simple_auth_user = "johann"			# user for basic authentication
simple_auth_hashed_pw = ''			# password hash: SHA512 -> run python -> import hashlib; hashlib.sha512("yourpassword").hexdigest()

## if ldap 
ldap_auth_type = "list" 			# list or group
ldap_url = "ldap://10.1.1.1:389"	# LDAP URL
ldap_domain = "musterschule.schule.paedml"
ldap_search_string = "CN=G_Lehrer_JVG,OU=Active Directory,OU=Sicherheitsgruppen,DC=musterschule,DC=schule,DC=paedml" # <- for group based auth
ldap_user_list = ["abc", "def", "muster.benutzer", "username"] # <- only for list auth