#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模仿 Flask 的 路由定义 API，-----------静态路径
"""
class NotFlask():
    def __init__(self):
        self.routes = {}

    def route(self, route_str):
        def decorator(f):
            # 记录路由和处理函数的映射字典
            self.routes[route_str] = f
            return f

        return decorator

    def serve(self, path):
        """
        服务器代码，只做示例
        """
        view_function = self.routes.get(path)
        if view_function:
            return view_function()
        else:
            raise ValueError('Route "{}"" has not been registered'.format(path))

app = NotFlask()

@app.route("/")
def hello():
    return "Hello World!"

# 相当于
# def hello1():
#     return "Hello World!"
# hello1 = app.route("/")(hello1)

print(app.serve("/"))   # OUTPUT: Hello World!

#++++++++++++++++++++++++++++++++++++++++++++++++++
import unittest

class TestNotFlask(unittest.TestCase):
    def setUp(self):
        self.app = NotFlask()

    def test_valid_route(self):
        @self.app.route('/')
        def index():
            return 'Hello World'

        self.assertEqual(self.app.serve('/'), 'Hello World')

    def test_invalid_route(self):
        with self.assertRaises(ValueError):
            self.app.serve('/invalid')