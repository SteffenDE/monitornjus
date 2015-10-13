# -*- coding: utf-8 -*-

#### Settings ####

running_with_iis = False # <- if running with iis
iis_virtual_path = "/monitornjus" # <- if running under a virtual path

auth_enabled = False # True or False
auth_type = "simple" # <- ldap or simple

## if simple
simple_auth_user = "user"
simple_auth_hashed_pw = 'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f'
##

## if ldap 
ldap_auth_type = "list" # list or group
ldap_url = "ldap://10.1.1.1:389"
ldap_domain = "musterschule.schule.paedml"
ldap_search_string = "CN=G_Lehrer_JVG,OU=Active Directory,OU=Sicherheitsgruppen,DC=musterschule,DC=schule,DC=paedml" # <- for group based auth
ldap_user_list = ["greu", "rupp", "stol", "steffen.deusch"] # <- only for list auth
##