#!/usr/bin/env python
# encoding: utf-8

import logging
import logging.handlers as handlers
from ast import literal_eval


class Logger:

    def __init__(self, logger_name, logger_level="INFO"):
        self.logger_level = logger_level
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(getattr(logging, self.logger_level))

        self.handler = logging.StreamHandler()
        self.handler.setLevel(getattr(logging, self.logger_level))

        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)

        self.logger.addHandler(self.handler)

if __name__ == '__main__':
    main()
