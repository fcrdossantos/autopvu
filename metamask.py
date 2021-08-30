import os
import pyperclip
import pyautogui
from gui_locate import locate, locate_click, regions
from pvu.utils import random_sleep


def open_mask():
    print("|| Abrindo o MetaMask")

    random_sleep(min_time=1)
    mask_1 = locate_click("mask_icon.png", regions("icon_mask"))
    random_sleep(min_time=1)

    if not mask_1:
        mask2 = locate_click("mask_icon_2.png", regions("icon_mask"))
        random_sleep(min_time=1)

        if not mask2:
            print("|| Não achamos o botão para ativar o MetaMask!")
            print("|| Abra o MetaMask manualmente")
            print("|| Após isso, pressione [ENTER] (aqui) continuar")
            input()
            return False

    random_sleep(6, min_time=3, max_time=5)
    return True


def unlock_mask():
    print("|| Digitando a senha")

    pyperclip.copy(os.getenv("PASSWORD"))

    pyautogui.hotkey("ctrl", "v")
    random_sleep(min_time=1)

    print("|| Desbloqueando MetaMask")

    unlock = locate_click("button_unlock.png")

    if not unlock:
        unlock = locate_click("button_unlock2.png")
        if not unlock:
            print("|| Não achamos o botão para desbloquear o MetaMask!")
            print("|| Desbloqueie o MetaMask manualmente")
            print("|| Após isso, pressione [ENTER] (aqui) continuar")
            input()
            return False

    random_sleep(min_time=2)
    return True


def login():
    if open_mask():
        if unlock_mask():
            random_sleep(15)
            if locate("open.png"):
                print("|| Ocultando a extensão do MetaMask!")
                locate_click("mask_icon.png", regions("icon_mask"))
            else:
                random_sleep(15)
                if locate("open.png"):
                    print("|| Ocultando a extensão do MetaMask!")
                    locate_click("mask_icon.png", regions("icon_mask"))
                else:
                    print("|| Não achei a extensão do Metamask aberta para ocultá-la")
