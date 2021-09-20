# -*- coding: utf-8 -*-
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
from pvu.utils import get_backend_url, random_sleep
from pvu.utils import get_headers, random_sleep
from logs import log


def check_maintenance():
    url = f"{get_backend_url()}/farm-status"
    headers = get_headers()

    log("Verificando se está em manutenção via request")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    maintenance_info = json.loads(response.text)

    status = maintenance_info.get("status")
    data = maintenance_info.get("data")

    if status == 0 and data is not None:
        my_group = data.get("inGroup")
        current_group = data.get("currentGroup")

        status_data = data.get("status")
        if status_data is not None and status_data == 1:
            return False

        if my_group == current_group:
            return False

        next_group = data.get("nextGroup")

        return next_group

    return False


def get_next_group_time(next_group):
    try:
        random_sleep()

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
        log("Aguarde mais alguns minutos para iniciar! (evitar lag nos grupos)")
        random_sleep(60 * 7, min_time=60 * 2, max_time=60 * 5)
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

    if not maintenance:
        return False

    if maintenance:
        next_group_time = get_next_group_time(maintenance)

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

        return True

    else:
        log("Não está em manutenção")
        return True
