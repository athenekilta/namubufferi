import os
import dj_database_url

def assign_from_env(name, envname, is_bool=False):
    try:
        if is_bool is True:
            evar = "False"
            if os.environ[envname] == "true":
                evar = "True"
            exec("{}={}".format(name, evar), globals())
        else:
            exec("{}='{}'".format(name, os.environ[envname]), globals())

        return True

    except KeyError:
        return False

    return False



try:
    ALLOWED_HOSTS = os.environ['NAMUBUFFERI_ALLOWEDHOSTS'].split()
except KeyError:
    pass

assign_from_env("SECRET_KEY", "NAMUBUFFERI_SECRETKEY")
assign_from_env("DEBUG", "DEBUG", is_bool=True)
assign_from_env("STATIC_URL", "NAMUBUFFERI_STATIC_URL")
assign_from_env("STATIC_ROOT", "NAMUBUFFERI_STATIC_ROOT")

if os.environ['NAMUBUFFERI_DB']:
    db_from_env = dj_database_url.parse(os.environ['NAMUBUFFERI_DB'])
    DATABASES = {'default':db_from_env}


assign_from_env("LDAP_AUTH_URL", "NAMUBUFFERI_LDAP_AUTH_URL")
assign_from_env("LDAP_AUTH_SEARCH_BASE", "NAMUBUFFERI_LDAP_AUTH_SEARCH_BASE")
assign_from_env("LDAP_AUTH_CONNECTION_USERNAME", "NAMUBUFFERI_LDAP_AUTH_CONNECTION_USERNAME")
assign_from_env("LDAP_AUTH_CONNECTION_PASSWORD", "NAMUBUFFERI_LDAP_AUTH_CONNECTION_PASSWORD")

