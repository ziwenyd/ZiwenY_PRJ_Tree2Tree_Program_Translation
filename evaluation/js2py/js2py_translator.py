"""
author: Ziwen Yuan
A simple experiment with Js2Py.
"""
import js2py
js2py.translate_file('js2py_test.js', 'js2py_test.py')  # translate

from example import example  # use translation result to call translated function
example.sayHello('Hi! I am Js2Py')
