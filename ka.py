from decenc.decstr import strdec
import json as jsond  # json

import time  # sleep before exit

import binascii  # hex encoding

import requests  # https requests

from uuid import uuid4  # gen random guid

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

# aes + padding, sha256

import webbrowser
import platform
import subprocess
import datetime
import datetime
import sys
import os

from requests_toolbelt.adapters.fingerprint import FingerprintAdapter
from decenc.genv import gf
from logs import log


class api:
    name = ownerid = secret = version = ""

    def __init__(self, name, ownerid, secret, version):
        self.name = name

        self.ownerid = ownerid

        self.secret = secret

        self.version = version

    sessionid = enckey = ""

    def init(self):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        self.enckey = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("init").encode()),
            "ver": encryption.encrypt(self.version, self.secret, init_iv),
            "enckey": encryption.encrypt(self.enckey, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        if response == "KeyAuth_Invalid":
            log("The application doesn't exist")
            sys.exit()

        response = encryption.decrypt(response, self.secret, init_iv)
        json = jsond.loads(response)

        if not json["success"]:
            a = "ONwKwJ_aEOe3lZYLOwInEgABhqCAAAAAAGEtqkGabnU7ecPnC_VP17lxZJIEUKVuUFaRF1Wasa-f_qGKk99oMvh32cfM4SeyU9etw6H-uUcBmy4e_C2sfC8asBnoFkQinPj2wHCJQvJkPLNgfpdTVad7QdbExxrgmW-NLPlxfcYxEHxWHu9HadZGFG6EFq96FaKCx6Vng-EJsxVYAEeZ6k9SP6RkGdz9mu6YKoU="
            b = a.encode()
            c = strdec(a, "https://").decode()

            message = json["message"]

            if message == "invalidver":
                log(c)
                sys.exit()
            else:
                log(message)
                sys.exit()

        self.sessionid = json["sessionid"]

    def register(self, user, password, license, hwid=None):
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("register").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "pass": encryption.encrypt(password, self.enckey, init_iv),
            "key": encryption.encrypt(license, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            print("successfully registered")
        else:
            print(json["message"])
            sys.exit()

    def upgrade(self, user, license):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("upgrade").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "key": encryption.encrypt(license, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            print("successfully upgraded user")
        else:
            print(json["message"])
            sys.exit()

    def login(self, user, password, hwid=None):
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("login").encode()),
            "username": encryption.encrypt(user, self.enckey, init_iv),
            "pass": encryption.encrypt(password, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            print("successfully logged in")
        else:
            print(json["message"])
            sys.exit()

    def license(self, key, hwid=None):
        if hwid is None:
            hwid = others.get_hwid()

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("license").encode()),
            "key": encryption.encrypt(key, self.enckey, init_iv),
            "hwid": encryption.encrypt(hwid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)
        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_user_data(json["info"])
            a = "EG9p5uSE3qWY_lRIWhPgJAABhqCAAAAAAGEtp_oTsx9bfBi5jMkSDWIChzbQRt_J5ZkfsujjulBK3qchtvnfVKCVgdTtyU0xBcdf8cd9lWqt_hqAusoyuiEHS_CxUhTGveuJUH2SG8J4PLGrAQ=="
            b = a.encode()
            c = strdec(a, "https://").decode()

            log(c)
            return True
        else:
            a = "AbOAFiQKiWsT50DuXFYmVQABhqCAAAAAAGEtqGBHhHFx_xLtWJZwYTCJziwPfSSiCI6JC40zaslxKSjbLgCghe1eGvA0DY_tmIzo8QtZKSzGhBaBTJD2x4uzzKNlqRQQwbn7M1oyBbspnDGQi4BSmqh6EKZi1YprL2xdKWR3i-9XOxGTL7_Vmu7Kc7hXg_gE0NEMGlmDBjovP-rPtw=="
            b = a.encode()
            c = strdec(a, "https://").decode()

            log(c)
            a = "ONwKwJ_aEOe3lZYLOwInEgABhqCAAAAAAGEtqkGabnU7ecPnC_VP17lxZJIEUKVuUFaRF1Wasa-f_qGKk99oMvh32cfM4SeyU9etw6H-uUcBmy4e_C2sfC8asBnoFkQinPj2wHCJQvJkPLNgfpdTVad7QdbExxrgmW-NLPlxfcYxEHxWHu9HadZGFG6EFq96FaKCx6Vng-EJsxVYAEeZ6k9SP6RkGdz9mu6YKoU="
            b = a.encode()
            c = strdec(a, "https://").decode()

            message = json["message"]

            if message == "invalidver":
                log(c)
                sys.exit()
            else:
                log(message)
                sys.exit()

    def var(self, name):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("var").encode()),
            "varid": encryption.encrypt(name, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def file(self, fileid):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("file").encode()),
            "fileid": encryption.encrypt(fileid, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)

        json = jsond.loads(response)

        if not json["success"]:
            print(json["message"])
            time.sleep(5)
            sys.exit()
        return binascii.unhexlify(json["contents"])

    def webhook(self, webid, param):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("webhook").encode()),
            "webid": encryption.encrypt(webid, self.enckey, init_iv),
            "params": encryption.encrypt(param, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        response = self.__do_request(post_data)

        response = encryption.decrypt(response, self.enckey, init_iv)
        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(5)
            sys.exit()

    def log(self, message):

        init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()

        post_data = {
            "type": binascii.hexlify(("log").encode()),
            "pcuser": encryption.encrypt(os.getenv("username"), self.enckey, init_iv),
            "message": encryption.encrypt(message, self.enckey, init_iv),
            "sessionid": binascii.hexlify(self.sessionid.encode()),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv,
        }

        self.__do_request(post_data)

    def __do_request(self, post_data):
        headers = {"User-Agent": "KeyAuth"}

        rq_out = requests.post(
            "https://keyauth.com/api/1.0/",
            data=post_data,
            headers=headers,
            verify=f"{gf(True)}",
        )

        return rq_out.text

    # region user_data
    class user_data_class:
        key = ""
        expiry = datetime.datetime.now()
        level = 0

    user_data = user_data_class()

    def __load_user_data(self, data):
        self.user_data.username = data["username"]


class others:
    @staticmethod
    def get_hwid():
        if platform.system() != "Windows":
            return "None"

        cmd = subprocess.Popen(
            "wmic useraccount where name='%username%' get sid",
            stdout=subprocess.PIPE,
            shell=True,
        )

        (suppost_sid, error) = cmd.communicate()

        suppost_sid = suppost_sid.split(b"\n")[1].strip()

        return suppost_sid.decode()


class encryption:
    @staticmethod
    def encrypt_string(plain_text, key, iv):
        plain_text = pad(plain_text, 16)

        aes_instance = AES.new(key, AES.MODE_CBC, iv)

        raw_out = aes_instance.encrypt(plain_text)

        return binascii.hexlify(raw_out)

    @staticmethod
    def decrypt_string(cipher_text, key, iv):
        cipher_text = binascii.unhexlify(cipher_text)

        aes_instance = AES.new(key, AES.MODE_CBC, iv)

        cipher_text = aes_instance.decrypt(cipher_text)

        return unpad(cipher_text, 16)

    @staticmethod
    def encrypt(message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]

            _iv = SHA256.new(iv.encode()).hexdigest()[:16]

            return encryption.encrypt_string(
                message.encode(), _key.encode(), _iv.encode()
            ).decode()
        except:
            print(
                "Invalid Application Information. Long text is secret short text is ownerid. Name is supposed to be app name not username"
            )
            sys.exit()

    @staticmethod
    def decrypt(message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]

            _iv = SHA256.new(iv.encode()).hexdigest()[:16]

            return encryption.decrypt_string(
                message.encode(), _key.encode(), _iv.encode()
            ).decode()
        except:
            print(
                "Invalid Application Information. Long text is secret short text is ownerid. Name is supposed to be app name not username"
            )
            sys.exit()
