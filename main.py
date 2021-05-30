import socket
from typing import Type
import cv2 
import base64
import subprocess
import pynput
import win32gui
from optparse import OptionParser
import inspect
import prts

commands = {}


def Register(func):
    if func.__name__ not in commands:
        print("registered", func.__name__)
        commands[func.__name__] = {
            'func_ref':func,
            'args': inspect.signature(func)
        }
    return func


class main:
    def __init__(self):
        self.__commands = {}

    @Register
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
        


