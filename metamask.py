import os
import pyperclip
import pyautogui
from gui_locate import locate, locate_click, regions
from pvu.utils import random_sleep
from logs import log


def open_mask():
    log("Abrindo o MetaMask")

    icon_possibilities = 4

    random_sleep(min_time=1)
    mask_found = False

    for i in range(icon_possibilities):

        mask_found = locate_click(f"mask_icon_{i+1}.png", regions("icon_mask"))
        random_sleep(min_time=1)

        if mask_found:
            random_sleep(6, min_time=3, max_time=5)
            return True

    log("Não achamos o botão para ativar o MetaMask!")
    log("Abra o MetaMask manualmente")
    log("Após isso, pressione [ENTER] (aqui) continuar")
    input()

    random_sleep(6, min_time=3, max_time=5)
    return False


def unlock_mask():
    log("Digitando a senha")

    pyperclip.copy(os.getenv("PASSWORD"))

    pyautogui.hotkey("ctrl", "v")
    random_sleep(min_time=1)

    log("Desbloqueando MetaMask")

    unlock = locate_click("button_unlock.png")

    if not unlock:
        unlock = locate_click("button_unlock2.png")
        if not unlock:
            log("Não achamos o botão para desbloquear o MetaMask!")
            log("Desbloqueie o MetaMask manualmente")
            log("Após isso, pressione [ENTER] (aqui) continuar")
            input()
            return False

    random_sleep(min_time=2)
    return True


def login():
    if open_mask():
        if unlock_mask():
            random_sleep(15)
            if locate("open.png"):
                log("Ocultando a extensão do MetaMask!")
                locate_click("mask_icon.png", regions("icon_mask"))
            else:
                random_sleep(15)
                if locate("open.png"):
                    log("Ocultando a extensão do MetaMask!")
                    locate_click("mask_icon.png", regions("icon_mask"))
                else:
                    log("Não achei a extensão do Metamask aberta para ocultá-la")
