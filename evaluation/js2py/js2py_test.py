__all__ = ['js2py_test']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['sayHello'])
@Js
def PyJsHoisted_sayHello_(name, this, arguments, var=var):
    var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
    var.registers(['name'])
    var.get('console').callprop('log', ((Js('Hello, ')+var.get('name'))+Js('!')))
PyJsHoisted_sayHello_.func_name = 'sayHello'
var.put('sayHello', PyJsHoisted_sayHello_)
pass
pass


# Add lib to the module scope
js2py_test = var.to_python()