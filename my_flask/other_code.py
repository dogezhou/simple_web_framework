#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This is our decorator
def simple_decorator(f):
    # This is the new function we're going to return
    # This function will be used in place of our original definition
    def wrapper():
        print("Entering Function")
        f()
        print("Exited Function")

    return wrapper

@simple_decorator
def hello():
    print("Hello World")

# 相当于：
def hello2():
    print('Hello2 world')
hello2 = simple_decorator(hello2)


# hello()
# hello2()

# 带参数的装饰器，装饰器工厂
def decorator_factory(enter_message, exit_message):
    # We're going to return this decorator
    def simple_decorator(f):
        def wrapper():
            print(enter_message)
            f()
            print(exit_message)

        return wrapper

    return simple_decorator

@decorator_factory("Start", "End")
def hello3():
    print("Hello3 World")

# 相当于
def hello4():
    print("Hello4 World")
hello4 = decorator_factory("Start", "End")(hello4)

# hello3()
# hello4()