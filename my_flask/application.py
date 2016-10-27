#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""application.py
修改 application WSGI 框架，使他提供一个类似 Flask 的接口
"""

import re


class MyFlask(object):
    """简单的 Web 框架"""
    headers = []

    def __init__(self):
        self.routes = []
        # [(re.compile("^/hello/(?P<username>.+)$")), fun hello),
        #  (注册路由的正则模式，路由函数)]

    def __call__(self, environ, start_response):
        """
        在具体应用中，传入 my_app 实例
        > wsgiapp = my_app(urls, globals())
        > httpd = make_server('', 8086, wsgiapp)
        在服务器中：
        > result = wsgiapp(environ, start_response)     # 调用了 __call__ 方法
        > for data in result
        """
        self._status = '200 OK'  # 默认状态OK
        # 由于传入服务器是同一个实例，每一次需要调用需要清空上一次headers
        del self.headers[:]  # 清空上一次的headers
        #
        result = self._delegate(environ)
        start_response(self._status, self.headers)

        # 将返回值result（字符串 或者 字符串列表）转换为迭代对象
        if isinstance(result, bytes):
            return iter([result])
        else:
            return iter(result)

    def _delegate(self, environ):
        """
        :param environ: {'PATH_INFO': '/hello/周伟’，'REQUEST_METHOD': 'GET'}
        :return: 路由函数执行结果
        """
        path = environ['PATH_INFO']  # '/hello/周伟'
        method = environ['REQUEST_METHOD']  # "GET'

        for route_pattern, view_function in self.routes:
            # route_pattern = re.compile("^/hello/(?P<username>.+)$")
            # view_function = fun hello
            m = route_pattern.match(path)
            if m:
                # 把匹配的对象传入函数做参数
                kwargs = m.groupdict()  # {'username': '周伟'}
                return view_function(**kwargs)  # username = '周伟'

        return self._notfound()

    def _notfound(self):
        self._status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "404 Not Found\n"

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))

    @staticmethod
    def build_route_pattern(route):
        """
        把 "/hello/<username>" 转换成 注册路径的正则模式
        :param route: "/hello/<username>" --> 要注册的路径
        :return: re.compile("^/hello/(?P<username>.+)$") --> 注册路径的正则模式
        """

        route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
        return re.compile("^{}$".format(route_regex))

    def route(self, route_str):
        """
        注册路由和路由函数
        :param route_str: "/hello/<username>" --> 要注册的路径
        """

        def decorator(f):
            """
            :param f: fun hello --> 要注册的路由函数
            """
            route_pattern = self.build_route_pattern(route_str)
            self.routes.append((route_pattern, f))

            return f

        return decorator
