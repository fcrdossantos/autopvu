# -*- coding: utf-8 -*-
import requests
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import get_browser
from pvu.utils import get_headers, random_sleep, get_backend_url
from pvu.items import get_items
from logs import log

USER_INFO = None


def reset_user():
    global USER_INFO

    USER_INFO = None


def get_user():
    global USER_INFO

    if USER_INFO is None:
        USER_INFO = get_user_info()

    return USER_INFO


def update_user(user):
    global USER_INFO

    USER_INFO = user


def get_pvu():
    random_sleep()
    driver = get_browser()

    xpath_pvu = "/html/body/div/div/div/div[1]/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]"

    log("Pegando seus PVU's")

    try:
        pvus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_pvu))
        )

        return float(pvus.text)
    except:
        log("Não conseguimos pegar seus PVU's")
        return 0.0


def get_le():
    url = f"{get_backend_url()}/farming-stats"
    headers = get_headers()

    log("Pegando seus LE's")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)
    le = user_info.get("data").get("leWallet")

    if user_info.get("status") == 444:
        raise Exception("Entrou em manutenção")

    if le is not None and len(str(le)) > 0:
        return int(le)
    else:
        log("Erro ao pegar os LES:", user_info)
        return 0


def get_user_info():
    global USER_INFO

    farm_url = "https://marketplace.plantvsundead.com/farm#/farm/"

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            if driver.current_url != farm_url:
                driver.get(farm_url)
    except:
        log("Impossível ir para a página principal da fazenda")

    pvu = get_pvu()
    le = get_le()
    items = get_items()

    USER_INFO = {"pvu": pvu, "le": le, "items": items}

    log("Você possui:")
    log(f"=> {pvu} PVU's")
    log(f"=> {le} LE's")
    for item in items:
        log(f"=> {item.get('current_amount')} {item.get('name')}")

    return USER_INFO
