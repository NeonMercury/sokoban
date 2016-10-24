#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from src.application import Application

if __name__ == '__main__':
    app = Application()

    app.load(sys.argv)
    sys.exit(app.run())
