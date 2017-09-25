# -*-coding:utf-8-*-

import os
import settings_production

FLASK_ENV = os.environ.get('FLASK_ENV', '')

if FLASK_ENV == "PRODUCTION":
    settings = settings_production.BaseConfig()
    log_setting = "logging_production.ini"
else:
    log_setting = "logging.ini"
    import settings_local
    settings = settings_local.LocalConfig()
