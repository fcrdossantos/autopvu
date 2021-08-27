# Python3 version of hugo24's snippet
import winreg
import os
import time
from pvu.utils import random_sleep

REG_PATH = r"SOFTWARE\Microsoft\Cryptography"
CHECK = True


def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        registry_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE
        )
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        print("|| HWID Alterado com sucesso!")
        return True
    except WindowsError as e:
        print("|| Problema ao alterar o HWID:", e)
        return False


def get_reg(name):
    try:
        registry_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_READ
        )
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError as e:
        print("|| Problema ao recuperar o valor da chave")
        print(e)
        return None


def delete_reg(name):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_ALL_ACCESS
        )
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        return True
    except WindowsError as e:
        return False


def set_hwid():
    print("|| Lendo o HWID correto")
    if os.getenv("USER") == "1":
        HWID = os.getenv("HWID_1")
    else:
        HWID = os.getenv("HWID_2")

    set_reg("MachineGuid", HWID)


def clear_hwid():
    return delete_reg("MachineGuid")


def check_hwid_clean():
    while CHECK:
        HWID_1 = os.getenv("HWID_1")
        HWID_2 = os.getenv("HWID_2")

        reg = get_reg("MachineGuid")

        if reg is not None:
            if reg != HWID_1 and reg != HWID_2:
                clear_hwid()

        random_sleep(13, min_time=5, max_time=10, verbose=False)