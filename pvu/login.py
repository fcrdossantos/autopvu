# -*- coding: utf-8 -*-
from random import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import get_browser
from gui_locate import locate_click, regions
from pvu.utils import random_sleep
from logs import log


def login_pvu():
    log("Logando na conta")

    random_sleep(min_time=1)
    login_btn = locate_click("login.png", regions("full"))
    random_sleep(min_time=1)

    if not login_btn:
        log("Não achamos o botão para logar no jogo!")
        log("Logue no jogo manualmente")
        log("Após isso, pressione [ENTER] (aqui) continuar")
        input()
        return False

    random_sleep(6, min_time=3, max_time=5)
    return True


def confirm_access():
    log("Vamos confirmar (assinar) o acesso (login)")

    random_sleep(10, min_time=5)
    login_btn = locate_click("sign.png", regions("full"))
    random_sleep(min_time=2)

    if not login_btn:
        random_sleep(10, min_time=5)
        login_btn2 = locate_click("sign2.png", regions("full"))
        random_sleep(min_time=2)

        if not login_btn2:
            log("Não achamos o botão para confirmar o acesso!")
            log("Logue no jogo manualmente")
            log("Após isso, pressione [ENTER] (aqui) continuar")
            input()
            return False

    random_sleep(6, min_time=3, max_time=5)
    return True


def check_logged():
    log("Aguarde até 10 segundos")
    log("Verificando Jogo e Login")
    try:
        driver = get_browser()

        random_sleep()
        maintenance = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div[1]")
            )
        )

        log("Precisamos logar na conta!")
        return False
    except:
        log("Já está logado na conta!")
        log("Vamos iniciar as rotinas do jogo")
        return True


def login():
    random_sleep()
    if not check_logged():
        random_sleep(5)
        if login_pvu():
            random_sleep(5)
            confirm_access()
            random_sleep(15, min_time=10, max_time=13)
