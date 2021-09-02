import os
import math

import json
from cv2 import solve

import requests

from pvu.captcha import get_captcha, solve_validation_captcha
from pvu.farm import water_plant
from pvu.utils import get_headers, random_sleep
from pvu.owner import get_owner
from browser import get_browser
from logs import log


def get_land_page_info(owner, page=0):

    land_info = get_land_info(owner, page)

    while land_info.get("status") == 556:
        log("Necessário resolver o captcha")

        captcha_results = get_captcha()
        if not captcha_results:
            raise Exception("Entrou em manutenção")

        solved = solve_validation_captcha(captcha_results)
        while not solved:
            captcha_results = get_captcha()
            if not captcha_results:
                raise Exception("Entrou em manutenção")

            solved = solve_validation_captcha(captcha_results)

        land_info = get_land_info(owner)

    return land_info


def get_land_info(owner, page=0, retry=0):
    log(f"Buscando informações da fazenda {owner} na página {page+1}")

    offset = page * 10

    url = f"https://backend-farm-stg.plantvsundead.com/farms/other/{owner}?limit=10&offset={offset}"

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(
                    f"https://marketplace.plantvsundead.com/farm#/farm/other/{owner}?page={page+1}"
                )
        except:
            log("Erro ao redirecionar para a página da fazenda a ser regada")

    headers = get_headers()

    random_sleep()
    response = requests.request(
        "GET",
        url,
        headers=headers,
    )

    try:
        land_info = json.loads(response.text)

        if land_info.get("status") == 444:
            raise Exception("Entrou em manutenção")

        return land_info
    except:
        retry += 1
        if retry <= 3:
            get_land_info(owner, page, retry)


def get_land_pages(land):
    total = land.get("total")

    if total:
        pages = math.ceil(total / 10)

        if pages > 5:
            pages = 5

        return pages
    else:
        log("Fazenda sem valor Total de terras", land)
        return 0


def get_page_plants(land, plants_to_water, watered_plants):
    plants = 0
    for plant in land["data"]:
        for tool in plant["activeTools"]:
            if tool["type"] == "WATER":
                water_count = tool["count"]
                if water_count <= 370:
                    log("Regando a planta", plant)

                    result_water = water_plant(plant)

                    if result_water == 556:
                        result_water = water_plant(plant["id"], need_captcha=True)

                    if result_water == 1:
                        plants += 1

                    log(f"{watered_plants}/{plants_to_water} plantas regadas")

                    if watered_plants >= plants_to_water:
                        random_sleep()
                        log("Todas as plantas necessárias foram regadas")
                        return -1

    random_sleep()
    return plants


def get_land_plants(owner, plants_to_water, watered_plants):
    new_watered_plants = 0

    land_info = get_land_page_info(owner)

    for page in range(get_land_pages(land_info)):
        page_info = get_land_page_info(owner, page)
        plants = get_page_plants(page_info, plants_to_water, watered_plants)
        if plants == -1:
            return -1
        else:
            new_watered_plants += new_watered_plants

    return new_watered_plants


def water_land(plants_to_water=15):
    log(f"Vamos regar {plants_to_water} plantas")

    log("Buscando uma fazenda para regar")
    owner = get_owner()

    log("Vamos regar a fazenda", owner)

    log("Vamos buscar todas as plantas dessa fazenda")
    watered_plants = get_land_plants(owner, plants_to_water, watered_plants=0)

    if watered_plants < plants_to_water:
        plants_to_water = plants_to_water - watered_plants
        water_land(plants_to_water)
