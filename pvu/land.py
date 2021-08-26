import os
import math

import json

import requests

from pvu.captcha import get_captcha_result
from pvu.farm import water_plant
from pvu.utils import get_headers, random_sleep
from pvu.owner import get_owner
from browser import get_browser

# Land
def solve_land_captcha():
    url = "https://backend-farm.plantvsundead.com/captcha/validate"

    captcha_results = get_captcha_result()

    payload = {
        "challenge": captcha_results.get("challenge"),
        "seccode": captcha_results.get("seccode"),
        "validate": captcha_results.get("validate"),
    }
    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao resolver o captcha")
        return True

    return False


def get_land_page_info(owner, page=0):

    land_info = get_land_info(owner, page)

    while land_info.get("status") == 556:
        print("|| Necessário resolver o captcha")
        while not solve_land_captcha():
            solve_land_captcha()

        land_info = get_land_info(owner)

    return land_info


def get_land_info(owner, page=0, retry=0):
    print(f"|| Buscando informações da fazenda {owner} na página {page+1}")

    offset = page * 10

    url = f"https://backend-farm.plantvsundead.com/farms/other/{owner}?limit=10&offset={offset}"

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(
                    f"https://marketplace.plantvsundead.com/farm#/farm/other/{owner}?page={page+1}"
                )
        except:
            print("|| Erro ao redirecionar para a página da fazenda a ser regada")

    headers = get_headers()

    random_sleep()
    response = requests.request(
        "GET",
        url,
        headers=headers,
    )

    try:
        land_info = json.loads(response.text)

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
        print(land)
        return 0


def get_page_plants(land):
    plants = []
    for plant in land["data"]:
        for tool in plant["activeTools"]:
            if tool["type"] == "WATER":
                water_count = tool["count"]
                if water_count <= 150:
                    plants.append(plant["_id"])

    random_sleep()
    return plants


def get_land_plants(owner):
    plants = []

    land_info = get_land_page_info(owner)

    for page in range(get_land_pages(land_info)):
        page_info = get_land_page_info(owner, page)
        plants += get_page_plants(page_info)

    return plants


def water_land(plants_to_water=15):
    print("|| Buscando uma fazenda para regar")
    owner = get_owner()

    print("|| Vamos regar a fazenda", owner)

    print("|| Vamos buscar todas as plantas dessa fazenda")
    plants = get_land_plants(owner)

    watered_plants = 0

    print(f"|| Encontrei {len(plants)} plantas na fazenda {owner}")

    print(f"|| Vamos regar {plants_to_water} plantas")

    for plant in plants:
        print("|| Regando a planta", plant)

        if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
            try:
                driver = get_browser()

                if driver is not None:
                    driver.get(
                        f"https://marketplace.plantvsundead.com/farm#/farm/{plant}"
                    )
            except:
                print("|| Erro ao redirecionar para página da plata a ser regada")

        if water_plant(plant):
            watered_plants += 1

        print(f"|| {watered_plants}/{plants_to_water} plantas regadas")
        if watered_plants >= plants_to_water:
            random_sleep()
            print("|| Todas as plantas necessárias foram regadas")
            break

    if watered_plants < plants_to_water:
        plants_to_water = plants_to_water - watered_plants
        water_land(plants_to_water)
    return plants
