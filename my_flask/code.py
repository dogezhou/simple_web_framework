#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""code.py"""

from my_flask.application import MyFlask

app = MyFlask()


@app.route("/hello/<username>")
def hello(username):
    return "Hello {}!".format(username)

@app.route('/<username>')
def index(username):
    return "你好，{}".format(username)


if __name__ == '__main__':
    from my_flask.webserver import make_server

    httpd = make_server(('127.0.0.1', 8089), app)
    sa = httpd.listen_socket.getsockname()
    print('http://{0}:{1}/'.format(*sa))

    # Respond to requests until process is killed
    httpd.serve_forever()
