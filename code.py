#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
一个 web 应用
"""

from wsgiref.simple_server import make_server
from application import my_app as app

if __name__ == '__main__':
    httpd = make_server('127.0.0.1', 8888, app)
    sa = httpd.socket.getsockname()
    print('http://{0}:{1}/'.format(*sa))

    # Respond to requests until process is killed
    httpd.serve_forever()