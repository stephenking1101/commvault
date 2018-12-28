#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import logging.config
import os
import yaml


class Logger:

    def __init__(self):
        log_conf = "./logging.yaml"

        if os.path.exists(log_conf):
            with open(log_conf, "r") as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def getlogger(self, name):
        return logging.getLogger(name)


logger = Logger()
