#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log/app.log')
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(filename)s[%(lineno)d] - %(funcName)s - %(message)s',
                               datefmt='%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
