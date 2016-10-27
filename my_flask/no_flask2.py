#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置 动态路由的演示例子， /hello/<username>
"""
import re

route_regex = re.compile(r"^/hello/(.+)$")
match = route_regex.match("/hello/ains")

print(match.groups())

# 给匹配组命名
route_regex = re.compile(r'^/hello/(?P<username>.+)$')
match = route_regex.match("/hello/ains")

print(match.groupdict())


# 将声明路径转换成等价的正则表达式模式
# '/hello/<username>' ---> '^/hello/(?P<username>.+)$'
def build_route_pattern(route):
    route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
    return re.compile("^{}$".format(route_regex))


print(build_route_pattern('/hello/<username>'))


def my_sub(pattern, repl, string):
    """
    :param pattern: 需要替换的字符串的正则表达式
    :param repl: 替换为此字符串
    :param string: 字符串
    :return:    替换后的字符串
    """
    match = re.search(pattern, string)  # pattern = "(<\w+>)", string = "/hello/<username>"
    result = ''
    pointer_1 = 0
    # 把 repl = r'(?P\1.+)' 中的 \1,\2... 替换成匹配 match 对象中的 <username>
    while pointer_1 < len(repl):
        if repl[pointer_1] == '\\':
            after_slash = repl[pointer_1+1]
            if after_slash.isdigit():
                result += match.group(int(after_slash))
                pointer_1 += 2
        else:
            result += repl[pointer_1]
            pointer_1 += 1

    return match

print('my_sub 返回 result = ', my_sub(r'(<\w+>)', r'(?P\1.+)', '/hello/<username>'))