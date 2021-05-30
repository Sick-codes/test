import socket
from typing import Type
import cv2 
import base64
import subprocess
import pynput
import inspect
from PIL import Image

commands = {}


def Register(alias):
    def inner(func):
        if func.__name__ not in commands:
            print("registered", func.__name__)
            argspec = inspect.getargspec(func)
            count = len(argspec.args) - 1 if inspect.ismethod(func) else len(argspec.args)   
            print(count)
            commands[alias] = {
                'func_ref':func,
                'args': inspect.signature(func),
                'arg_count':count
                }
        return func
    return inner


class main:

    @Register(alias="snap")
    def snapshot(self):
        i, img = cv2.VideoCapture(0).read()
        return base64.b64encode(img)

    @Register(alias="press")
    def enablePress(self, button):
        pynput.press(button)
        pynput.release()

    @Register(alias="screenshot")
    def screenshot():
        pass

    def call_func(self, func_ref, *args):
        res = self.commands[func_ref.__name__]
        if len(args) == res['args']:
            res['func_ref'](*args)
        

def test(test1, test2, test3):
    pass
print(commands)