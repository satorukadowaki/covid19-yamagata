#!/usr/bin/env python

import os

# -- Server Configuration
LOG_FORMAT = "[%(asctime)s] [%(module)s:%(lineno)s] %(levelname)s %(message)s"
SERVER_PORT = os.environ.get("API_PORT", 8320)

RELEASE_VERSION = os.environ.get("VERSION", "v0.0.1")
ENV_NAME = os.environ.get("ENV_NAME", "DEV")
# STATIC_FILE_DIRECTORY = os.environ.get("STATIC_FILE_DIRECTORY", "./")
