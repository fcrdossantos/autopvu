import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import get_browser
from gui_locate import locate_click, regions
from pvu.utils import random_sleep


def login_pvu():
    print("|| Logando na conta")

    random_sleep(min_time=1)
    login_btn = locate_click("login.png", regions("full"))
    random_sleep(min_time=1)

    if not login_btn:
        print("|| Não achamos o botão para logar no jogo!")
        print("|| Logue no jogo manualmente")
        print("|| Após isso, pressione [ENTER] (aqui) continuar")
        input()
        return False

    random_sleep(6, min_time=3, max_time=5)
    return True


def confirm_access():
    print("|| Vamos confirmar (assinar) o acesso (login)")

    random_sleep(min_time=1)
    login_btn = locate_click("sign.png", regions("full"))
    random_sleep(min_time=1)

    if not login_btn:
        random_sleep(min_time=1)
        login_btn2 = locate_click("sign2.png", regions("full"))
        random_sleep(min_time=1)

        if not login_btn2:
            print("|| Não achamos o botão para confirmar o acesso!")
            print("|| Logue no jogo manualmente")
            print("|| Após isso, pressione [ENTER] (aqui) continuar")
            input()
            return False

    random_sleep(6, min_time=3, max_time=5)
    return True


def check_logged():
    print("|| Aguarde até 10 segundos")
    print("|| Verificando Jogo e Login")
    try:
        driver = get_browser()

        random_sleep()
        maintenance = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div[1]")
            )
        )

        print("|| Precisamos logar na conta!")
        return False
    except:
        print("|| Já está logado na conta!")
        print("|| Vamos iniciar as rotinas do jogo")
        return True


def login():
    random_sleep()
    if not check_logged():
        random_sleep()
        if login_pvu():
            random_sleep()
            confirm_access()
