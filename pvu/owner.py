# -*- coding: utf-8 -*-
import os
import random
import requests
import json
from pvu.utils import get_headers, random_sleep, get_backend_url
from browser import get_browser
from logs import log

# Owner


def get_land_owner(x, y):
    url = f"{get_backend_url()}/land/{x}/{y}"
    headers = get_headers()

    random_sleep()
    response = requests.request(
        "GET",
        url,
        headers=headers,
    )

    land_info = json.loads(response.text)

    if land_info.get("status") == 444:
        raise Exception("Entrou em manutenção")

    owner = land_info.get("data").get("ownerId")

    if owner is None or len(owner) == 0:
        return None

    return owner


def find_random_land_owner():
    log("Buscando uma fazenda aleatória")

    coord_x = random.randint(-16, 16)
    coord_y = random.randint(-16, 16)
    log(f"Buscando a fazenda: {coord_x}x{coord_y}")

    owner = get_land_owner(coord_x, coord_y)

    if owner:
        log(f"O dono (ID) da fazenda {coord_x}x{coord_y} é {owner}")
        return owner
    else:
        log(f"A fazenda {coord_x}x{coord_y} ainda não tem dono")
        return False


def get_owner():
    land = find_random_land_owner()

    while not land:
        random_sleep()
        land = find_random_land_owner()

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(
                    f"https://marketplace.plantvsundead.com/farm#/farm/other/{land}"
                )
        except:
            log("Erro ao acessar a página da fazendo para pegar o dono")

    return land
