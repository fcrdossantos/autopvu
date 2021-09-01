import time
import os

import json
import requests
from datetime import datetime
from dateutil import tz


from datetime import datetime
from browser import get_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pvu.utils import random_sleep
from pvu.utils import get_headers, random_sleep
from logs import log


def check_maintenance():
    url = "https://backend-farm-stg.plantvsundead.com/farming-stats"
    headers = get_headers()

    log("Verificando se está em manutenção")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)

    status = user_info.get("status")

    # 444 = maintenance
    return status == 444


def get_next_group_time():
    try:
        random_sleep()

        url = "https://backend-farm-stg.plantvsundead.com/farm-status"
        headers = get_headers()

        log("Pegando horário do próximo grupo")

        random_sleep()
        response = requests.request("GET", url, headers=headers)

        json_response = json.loads(response.text)

        next_group = json_response.get("data").get("nextGroup")

        next_group_utc = datetime.strptime(next_group, "%Y-%m-%dT%H:%M:%S.%fZ")

        next_group_utc = next_group_utc.replace(tzinfo=tz.tzutc())

        local_next_group = next_group_utc.astimezone(tz=tz.tzlocal())

        log("Horário do próximo grupo encontrado!")
        random_sleep()

        return local_next_group
    except:
        log("Horário do próximo grupo não informado")
        return False


def can_login_maintenance(next_group_date):
    random_sleep()
    now = datetime.now().replace(tzinfo=tz.tzlocal())

    if now > next_group_date:
        log("Chegou a hora do seu grupo jogar!")
        log("Aguarde mais um minuto para iniciar!")
        random_sleep(60 * 2, min_time=60, max_time=90)
        return True
    else:
        log("Ainda não é a hora do seu grupo jogar")
        return False


def wait_next_group(next_group_time):
    waited = 0
    while not can_login_maintenance(next_group_time):
        if waited >= 5:
            log("Tendo certeza de que ainda está em manutenção")
            if not check_maintenance():
                break
            waited = 0

        log(f"Esperando até", next_group_time)
        random_sleep(6 * 60, min_time=3 * 60, max_time=5 * 60)
        waited += 1


def wait_maintenance():
    log("Verificando se o jogo está em manutenção")
    maintenance = check_maintenance()

    if maintenance:
        next_group_time = get_next_group_time()

        if next_group_time:
            log(f"Jogo indisponível no momento (Manutenção)")
            wait_next_group(next_group_time)
            random_sleep()
        else:
            while maintenance:
                log(f"Jogo indisponível no momento (Manutenção)")

                random_sleep(6 * 60, min_time=3 * 60, max_time=5 * 60, verbose=True)

                log("Verificando se o jogo ainda está em manutenção")
                maintenance = check_maintenance()

    else:
        log("Não está em manutenção")
