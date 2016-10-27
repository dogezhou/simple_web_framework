#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""code.py"""

from framework.application import my_app

# ((请求路径正则表达式，处理类名），）
urls = (
    ("/", "index"),
    ("/hello/(.*)", "hello"),
)

# 实例化了一个 wsgiapp, 有余 my_app 有 __call__ 方法，所以 wsgiapp 可调用，传入 server
wsgiapp = my_app(urls, globals())


class index(object):
    def GET(self):
        my_app.header('Content-type', 'text/plain')
        return "Welcome!\n".encode()


class hello(object):
    def GET(self, name):
        my_app.header('Content-type', 'text/plain')
        return "Hello %s!\n" % name


if __name__ == '__main__':
    # python3 的 wsgiref 好像有问题
    # from wsgiref.simple_server import make_server
    from framework.webserver import make_server

    httpd = make_server(('127.0.0.1', 8089), wsgiapp)
    sa = httpd.listen_socket.getsockname()
    print('http://{0}:{1}/'.format(*sa))

    # Respond to requests until process is killed
    httpd.serve_forever()
