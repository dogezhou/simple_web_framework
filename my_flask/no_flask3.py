#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


class NotFlask():
    def __init__(self):
        self.routes = []
        # [(re.compile("^/hello/(?P<username>.+)$"), fun hello),
        #  (注册路由的正则模式，路由函数)]

    @staticmethod
    def build_route_pattern(route):
        """
        :param route: "/hello/<username>" --> 要注册的路径
        :return: re.compile("^/hello/(?P<username>.+)$") --> 注册路径的正则模式
        """

        route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
        return re.compile("^{}$".format(route_regex))

    def route(self, route_str):
        """
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

    def get_route_match(self, path):
        """
        :param path: '/hello/周伟' --> 请求路径
        """

        for route_pattern, view_function in self.routes:
            # route_pattern, view_function = (re.compile("^/hello/(?P<username>.+)$"), fun hello)
            m = route_pattern.match(path)
            if m:
                return m.groupdict(), view_function
                # m.groupdict() = {'username': '周伟',}, fun hello

        return None

    def serve(self, path):
        """
        :param path: '/hello/周伟' --> 请求路径
        """
        route_match = self.get_route_match(path)
        if route_match:
            kwargs, view_function = route_match  # {'username': '周伟',}, fun hello
            return view_function(**kwargs)  # hello(username = '周伟')
        else:
            raise ValueError('路径 "{}"" 未被注册！'.format(path))


app = NotFlask()


@app.route("/hello/<username>")
def hello(username):
    return "Hello {}!".format(username)


print(app.serve('/hello/周伟'))
