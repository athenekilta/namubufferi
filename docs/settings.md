# Settings
Following settings should be supplied as enviromental
variables.

## Generic
* __NAMUBUFFERI_DB__
    - postgres://user:password@db.namubufferi.com/namubufferi
* __NAMUBUFFERI_SECRETKEY__
* __DEBUG__
    - _false_
* __NAMUBUFFERI_ALLOWEDHOSTS__
    - _namubufferi.com namubufferi.org_
* __NAMUBUFFERI_OUTPAN_API_KEY__
    - API key to outpan.com

## LDAP integration
* __NAMUBUFFERI_USELDAP__ (true/false)
    - Docker image uses this variable
* __NAMUBUFFERI_LDAP_AUTH_URL__
    - _ldap://ldap:389_
* __NAMUBUFFERI_LDAP_AUTH_SEARCH_BASE__
    - _dc=namubufferidomain,dc=com_
* __NAMUBUFFERI_LDAP_AUTH_CONNECTION_USERNAME__
    - _namubufferiuser_
* __NAMUBUFFERI_LDAP_AUTH_CONNECTION_PASSWORD__
    - _namubufferipw_

## Email
Set these

* __NAMUBUFFERI_USE_SMTP__
    - _true_
* __SMTP_HOST__
* __SMTP_PORT__
* __SMTP_USER__
* __SMTP_PASSWORD__
* __SMTP_TLS__ or __SMTP_SSL__
    - _true_

Or these

* __SENDGRID_USERNAME__
* __SENDGRID_PASSWORD__

