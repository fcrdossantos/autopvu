import time
import os
from datetime import datetime, timedelta
from browser import get_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pvu.utils import random_sleep


import json
import requests
from pvu.utils import get_headers, random_sleep
from logs import log


def maintenance_request():
    url = "https://backend-farm.plantvsundead.com/farming-stats"
    headers = get_headers()

    log("Verificando se está em manutenção via request")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)

    status = user_info.get("status")

    # 444 = maintenance
    return status == 444


def get_next_group_time():
    random_sleep()
    now = datetime.now()
    current_minute = now.minute

    next_minute = int(os.getenv("GROUP_RESET_MINUTE"))

    next_group = now.replace(
        microsecond=0,
        second=0,
        minute=next_minute,
        hour=now.hour,
        day=now.day,
        month=now.month,
        year=now.year,
    )

    if current_minute >= next_minute:
        next_group = next_group + timedelta(hours=1)

    random_sleep()
    return next_group


def can_login_maintenance(next_group_date):
    random_sleep()
    if datetime.now() > next_group_date:
        return True
    else:
        return False


def check_maintenance():
    try:

        if maintenance_request():
            log("Confirmamos a manutenção via request")
            return True

        driver = get_browser()

        game_url = "https://marketplace.plantvsundead.com/farm#/farm/"
        driver.get(game_url)

        random_sleep(min_time=1)

        random_sleep(3)

        if driver is not None:
            current_url = driver.current_url
            while current_url != game_url and current_url != game_url[:-1]:
                current_url = driver.current_url
                log("Não está no link certo", current_url, game_url)
                driver.get(game_url)
                random_sleep(5, min_time=3)

        maintenance = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div/p")
            )
        )

        maintenance = maintenance.text

        random_sleep()
        if maintenance == "Farm Maintenance":
            log("Em Manutenção! Tente novamente mais tarde")
            return True

        return False
    except Exception as e:
        random_sleep(3)
        log("Jogo liberado! Pode jogar")
        return False


def wait_maintenance():
    if check_maintenance():
        next_group_time = get_next_group_time()
        now = datetime.now().strftime("%H:%M:%S")

        log(f" [{now}] Jogo indisponível no momento (Manutenção)")

        waited = 0
        while not can_login_maintenance(next_group_time):
            now = datetime.now().strftime("%H:%M:%S")
            log(f" [{now}] Esperando até", next_group_time)
            random_sleep(6 * 60, min_time=3 * 60, max_time=5 * 60, verbose=True)

            if waited == 5:
                if not check_maintenance():
                    break
                waited = 0
    else:
        log("Não está em manutenção")


# When we don't know group reset time
def wait_maintenance_force():
    while check_maintenance():
        now = datetime.now().strftime("%H:%M:%S")

        log(f" [{now}] Jogo indisponível no momento (Manutenção)")

        random_sleep(6 * 60, min_time=3 * 60, max_time=5 * 60, verbose=True)
    else:
        log("Não está em manutenção")
