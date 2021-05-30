import socket
from typing import Type
import cv2 
import base64
import subprocess
import pynput
import win32gui
from optparse import OptionParser
import inspect

commands = {}


def Register(alias):
    def inner(func):
        if func.__name__ not in commands:
            print("registered", func.__name__)
            commands[alias] = {
                'func_ref':func,
                'args': inspect.signature(func)
            }
        return func
    return inner


class main:
    def __init__(self):
        self.__commands = {}

    @Register(alias="snap")
    def snapshot(self):
        i, img = cv2.VideoCapture(0).read()
        return base64.b64encode(img)

    @Register
    def enablePress(self, button):
        pynput.press(button)
        pynput.release()

    @Register
    def screenshot():
        pass

    def call_func(self, func_ref, *args):
        res = self.commands[func_ref.__name__]
        if len(args) == res['args']:
            res['func_ref'](*args)
        


print(commands)