#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
application.py
WSGI 接口
WSGI 服务器把请求数据 environ 和 函数 start_response传递给应用来调用应用，
    应用通过 start_response 设置响应码和响应头，返回一个字符串迭代对象，服务器用他们构建响应
"""
import re


class my_app:
    # ("/", "index") --> （请求路径的正则表达式，处理函数）
    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )  ##########修改点

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        # 消除 GET_* 方法中重复的部分
        self.status = '200 OK'
        self._headers = []

    def __iter__(self):
        """
        WSGI 服务器，这样
        > result = my_app(environ, start_response)
        调用 / 创建了一个实例，实例有 __iter__ 方法， 所以result是可迭代实例
        > for data in result:
        相当于，iter(result) 调用 __iter__ 方法， 得到一个迭代器，调用 next 方法得到 data
        """
        result = self.delegate()    # 一个 字符串或字符串列表 而不是一个迭代器对象

        # python3 WSGI 接受 bytes, 把 返回的字符串或字符串列表，encode
        if isinstance(result, str):
            result = result.encode('utf-8')
        else:
            result = [a_str.encode('utf-8') for a_str in result]

        self.start(self.status, self._headers)  # 添加响应头

        # 将返回值 result（字符串 或者 字符串列表）转换为迭代对象
        if isinstance(result, bytes): # ! python3 bytes 和 str 没有一个 base class basestring(移除了）
            return iter([result])
        else:
            return iter(result)

    def delegate(self):
        """
        使用请求路径和方法找出处理函数，调用处理函数
        返回字符串或字符串列表
        """
        # 获取请求路径
        path = self.environ['PATH_INFO']  # "/hello/world"
        # 获取请求方法
        method = self.environ['REQUEST_METHOD']  # "GET"

        for pattern, name in self.urls:
            # pattern = "/hello/(.*)"
            # name = "hello"
            m = re.match('^' + pattern + '$', path)
            # re.match('^' + "/hello/(.*)" + '$', "/hello/world")
            if m:
                # 把匹配的组当作参数调用处理函数
                args = m.groups()  # ('world',) m.groups() == (m.group(1), m.group(2)...)
                # 处理函数名
                funcname = method.upper() + '_' + name  # 'GET' + '_' + 'hello'
                if hasattr(self, funcname):
                    # 如果存在处理函数，获取对象
                    func = getattr(self, funcname)  # func = self.GET_hello
                    return func(*args)  # self.GET_hello(*('world', )

        return self.notfound()

    def header(self, name, value):
        self._headers.append((name, value))

    def GET_index(self):
        self.header('Content-type', 'text/plain')
        return "Welcome!\n", '周伟'

    def GET_hello(self, name):
        self.header('Content-type', 'text/plain')
        return "Hello %s!\n" % name

    def notfound(self):
        self.status = '404 Not Found'
        self.header('Content-type', 'text/plain')
        return "Not Found\n"