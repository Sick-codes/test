from os import set_inheritable
import socket
from typing import Type
from PIL.Image import Image
from PIL.ImageGrab import grab
import cv2 
import base64
import subprocess
from mss.models import Monitor
import pynput
import inspect
import mss
import mss.tools
commands = {}


def register(alias):
    def inner(func):
        if func.__name__ not in commands:
            commands[alias] = {
                'func_ref':func,
                'args': inspect.signature(func),
                'arg_count':len(inspect.getfullargspec(func).args)
                }
        return func
    return inner


class main:

    @register(alias="snap")
    def __snapshot(self):
        i, img = cv2.VideoCapture(0).read()
        img.release()
        return base64.b64encode(img)

    @register(alias="press")
    def __enablePress(self, button):
        pynput.press(button)
        pynput.release()


    @register(alias="sys")
    def sysCommand(self, sys_command, *args):
        subprocess.Popen()

    @register(alias="screenshot")
    def __screenshot(self, monitor_number=1):
        m = mss.mss()
        monintor1 = m.monitors[monitor_number]
        e = m.grab(monintor1)
        return base64.b64encode(
             mss.tools.to_png(e.rgb, e.size))


    def call_func(self, alias, *args, is_sys=False):
        try:
            if is_sys:
                return subprocess.Popen(
                    [alias, *args], 
                    shell=True,
                    stdout=subprocess.PIPE
                )
            else:
                func = commands[alias]
                print(func["arg_count"])
                if len(args) == func['arg_count']-1:
                    new_tuple = (self, *args)
                    return func['func_ref'](*new_tuple)
        except KeyError:
            None


inst = main()
x = inst.call_func("snap")