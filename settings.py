# -*- coding: utf-8 -*-

#### Settings ####

triggerrefresh = False				# <- only enable when running with MULTIPLE workers, e.g. NOT the dev server

running_with_iis = False 			# <- if running with iis
iis_virtual_path = "/monitornjus" 	# <- if running under a "virtual path"

### Authentication ###

auth_enabled = False				# True or False
auth_type = "simple" 				# <- ldap or simple

## if simple
simple_auth_user = "johann"			# user for basic authentication
simple_auth_hashed_pw = '73eb768fe6a4c876aeb9fa99a5abf0d2f201d363db2f3b76d5ccc1ccb96caaa4e9e6fae73804fd0ae97041b4486765ad36619e256488c1ec0adab5e3a15219f2'			# password hash: SHA512 -> run python -> import hashlib; hashlib.sha512("yourpassword").hexdigest()

## if ldap 
ldap_auth_type = "list" 			# list or group
ldap_url = "ldap://10.1.1.1:389"	# LDAP URL
ldap_domain = "musterschule.schule.paedml"
ldap_search_string = "CN=G_Lehrer_JVG,OU=Active Directory,OU=Sicherheitsgruppen,DC=musterschule,DC=schule,DC=paedml" # <- for group based auth
ldap_user_list = ["abc", "def", "muster.benutzer", "username"] # <- only for list auth