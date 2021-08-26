import os
import random
import time
from datetime import datetime
from browser import get_browser
from local_storage import LocalStorage


BEARER = None


def get_headers():
    random_sleep()

    headers = {
        "authority": "backend-farm.plantvsundead.com",
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


def get_bearer_token():
    global BEARER

    if BEARER is None:
        print("|| Pegando novo Token")
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
            print("|| Impossível ir para a página de inventário")

        waiting_req = True

        while waiting_req:
            random_sleep()

            for req in driver.requests:
                if (
                    "https://backend-farm.plantvsundead.com/get-seeds-inventory"
                    in req.url
                ):
                    if "authorization" in req.headers:
                        BEARER = req.headers["authorization"]
                        waiting_req = False

        try:
            if driver is not None:
                random_sleep()
                driver.get("https://marketplace.plantvsundead.com/farm#/farm")
        except:
            print("|| Impossível voltar para a fazenda após pegar o token")
    finally:
        return BEARER


def random_sleep(multiplier=2, min_time=0, max_time=None, verbose=False):
    if os.getenv("RANDOM_SLEEPS", "TRUE").lower() in ("false", "1"):
        return
    random_time = random.random() * multiplier

    if random_time < min_time:
        random_time += min_time

    if max_time is not None:
        if random_time > max_time:
            random_time = random.randint(min_time, max_time)
            if random_time == max_time:
                random_time -= random.random()
            else:
                random_time += random.random()

    if verbose:
        if random_time > 60:
            minutes = random_time // 60
            seconds = random_time % 60
            print(
                f"||Esperando {minutes:.0f} minutos e {seconds:.2f} segundos para a próxima ação"
            )
        else:
            print(f"|| Esperando {random_time:.2f} segundos para a próxima ação")

    time.sleep(random_time)
