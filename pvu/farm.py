import json
import time
import os
import requests
import random
from pvu.utils import get_headers, random_sleep
from pvu.captcha import get_captcha_result

# List all farm infos and status
def get_farm_infos():
    print("|| Coletando as informações da fazenda")
    url = "https://backend-farm.plantvsundead.com/farms"

    querystring = {"limit": "10", "offset": "0"}

    payload = ""
    headers = get_headers()

    random_sleep()
    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    return json.loads(response.text)


# Get all plants infos (ID and WATER)
def get_plants():
    print("|| Coletando as informações das plantas")
    farm = get_farm_infos()
    plants = []

    random_sleep()
    if farm.get("status") == 0:
        farm_data = farm.get("data")
        for plant in farm_data:
            _plant = {"id": plant["_id"], "water": 0, "crow": False}

            for tool in plant["activeTools"]:
                if tool["type"] == "WATER":
                    _plant["water"] = tool["count"]
                if tool["type"] == "POT":
                    _plant["pot"] = tool["count"]

            has_crow = plant.get("hasCrow")

            if has_crow is not None:
                _plant["crow"] = has_crow

            _plant["stage"] = plant["stage"]

            plants.append(_plant)

    return plants


def water_plant(plant_id):
    print("|| Aguando a planta:", plant_id)

    url = "https://backend-farm.plantvsundead.com/farms/apply-tool"

    captcha_results = get_captcha_result()

    payload = {
        "farmId": plant_id,
        "toolId": 3,
        "token": {
            "challenge": captcha_results.get("challenge"),
            "seccode": captcha_results.get("seccode"),
            "validate": captcha_results.get("validate"),
        },
    }
    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao regar a planta:", plant_id)
    elif '"status":15' in response.text:
        print("|| Você não tem mais Águas para regar a planta:", plant_id)
    elif '"status":20' in response.text:
        print("|| Não precisa mais regar a planta:", plant_id)
    elif '"status":28' in response.text:
        print("|| Você já regou as 15 plantas hoje, não podemos regar mais.")
    elif '"status":16' in response.text:
        print("|| Essa planta já foi regada as 200 vezes hoje!")
        return False
    else:
        print("|| Erro ao regar a planta", plant_id)
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente!")
        return False
    return True


def water_plants(plants=None):
    print("|| Iniciando a rotina de regar plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        while plant["water"] < 2:
            random_sleep()
            if water_plant(plant["id"]):
                plant["water"] += 1

        random_sleep()
        print(f"|| Planta {plant['id']} terminou de ser regada")

    print("|| Todas as plantas foram regadas")


def remove_crow(plant_id):
    print("|| Removendo corvo da planta:", plant_id)

    url = "https://backend-farm.plantvsundead.com/farms/apply-tool"

    captcha_results = get_captcha_result()

    payload = {
        "farmId": plant_id,
        "toolId": 4,
        "token": {
            "challenge": captcha_results.get("challenge"),
            "seccode": captcha_results.get("seccode"),
            "validate": captcha_results.get("validate"),
        },
    }
    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao remover o corvo da planta:", plant_id)
    elif '"status":15' in response.text:
        print("|| Você não tem mais Espantalhos para tirar corvos da planta:", plant_id)
    elif '"status":20' in response.text:
        print("|| Não precisa mais tirar corvos da planta:", plant_id)
    elif '"status":28' in response.text:
        print("|| Você já tirou corvos das 5 plantas hoje, não podemos remover mais.")
    else:
        print("|| Erro ao remover o corvo da planta", plant_id)
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente!")
        return False
    return True


def remove_crows(plants=None):
    print("|| Iniciando a rotina de remover corvos")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        while plant["crow"]:
            random_sleep()
            if remove_crow(plant["id"]):
                plant["crow"] = False

        random_sleep()
        print(f"|| Planta {plant['id']} não tem mais corvos")

    print("|| Todos os corvos foram retirados")


def use_pot(plant_id):
    print("|| Colocando pote na planta:", plant_id)

    url = "https://backend-farm.plantvsundead.com/farms/apply-tool"

    captcha_results = get_captcha_result()

    if os.getenv("POT_TYPE", "SMALL").lower() in ("big", "2"):
        tool_id = 2
    else:
        tool_id = 1

    payload = {
        "farmId": plant_id,
        "toolId": tool_id,
        "token": {
            "challenge": captcha_results.get("challenge"),
            "seccode": captcha_results.get("seccode"),
            "validate": captcha_results.get("validate"),
        },
    }
    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao colocar o vaso na planta:", plant_id)
    elif '"status":15' in response.text:
        print("|| A planta já está com o limite de vasos:", plant_id)
    elif '"status":20' in response.text:
        print("|| Não precisa mais colocar vasos na planta:", plant_id)
    elif '"status":28' in response.text:
        print("|| Você já atingiu o limite diário de colocar vasos.")
    else:
        print("|| Erro ao colocar o vaso na planta", plant_id)
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente!")
        return False
    return True


def use_pots(plants=None):
    print("|| Iniciando a rotina de colocar vasos nas plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:

        if plant["stage"] == "new":
            print(f"|| A planta é nova e precisa de um vaso")
            use_pot(plant["id"])
            continue

        while plant["pot"] == 0:
            random_sleep()
            if use_pot(plant["id"]):
                plant["pot"] = 1
        random_sleep()
        print(f"|| Planta {plant['id']} não precisa de vasos")

    print("|| Todas as plantas estão com vasos")
