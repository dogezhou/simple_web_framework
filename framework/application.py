#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""application.py
注意在自制的服务器中，可以接受字符串或者 bytes,
服务器中：
for data in result:
    # flask 返回的是Bytes, 解码成字符串, wsgiapp.py 返回的是字符串，不需要decode
    # 转换成字符串
    if isinstance(data, bytes):
        data = data.decode()
    response += data
"""

import re


class my_app(object):
    """my simple web framework"""
    headers = []

    def __init__(self, urls=(), fvars={}):
        self._urls = urls  # ( ("/", "index"), ("/hello/(.*)", "hello"),)
        self._fvars = fvars  # globals() 字典

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
        path = environ['PATH_INFO']  # '/hello/world'
        method = environ['REQUEST_METHOD']  # "GET'

        for pattern, name in self._urls:
            # pattern = "/hello/(.*)"
            # name = "hello"
            m = re.match('^' + pattern + '$', path)
            # m = re.match('^/hello/(.*)$', '/hello/world')
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()   # ('world',)
                funcname = method.upper()  # 方法名大写（如GET、POST）   # 'GET'
                klass = self._fvars.get(name)  # 根据字符串名称查找类对象   # 定义的 hello 类对象
                if hasattr(klass, funcname):
                    func = getattr(klass, funcname) # hello.GET
                    return func(klass(), *args)     # hello.GET(hello(), 'world')

        return self._notfound()

    def _notfound(self):
        self._status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))
