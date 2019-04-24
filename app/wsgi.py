#!/usr/bin/env python3

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))

from app import app as application


if __name__ == '__main__':
    application.run()
