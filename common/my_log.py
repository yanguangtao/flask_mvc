#!/bin/env python
# -*-coding:utf-8-*- 

import logging
import logging.config
import os
from conf import log_setting

log_path = "%s/conf/%s" % (os.path.abspath('.'), log_setting)
logging.config.fileConfig(log_path)
logger = logging.getLogger("root")
