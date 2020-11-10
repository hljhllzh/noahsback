# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
class ProductionConfig(object):
    DEBUG = True
    DB_HOSTNAME = '35.201.20.84'
    DB_PASSWORD = "comp9900"
    DB_SCHEMA = "filmfinder"
    DB_USER = "vlab"
    DB_PORT = 3306
    DB_CHARSET = "utf8"
    SQLALCHEMY_DATABASE_URI = \
        f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_SCHEMA}?charset={DB_CHARSET}'
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 139881176065085772433712442657801793320 #secrets.SystemRandom().getrandbits(128)
    SECRET_KEY = 'w6cirhf-rbN__venIrKlbnTca407g07uRT0jqtbXYb8' #secrets.token_urlsafe()