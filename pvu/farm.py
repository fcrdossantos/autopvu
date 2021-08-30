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
            _plant = {
                "id": plant["_id"],
                "water": 0,
                "crow": False,
                "stage": "farming",
                "temp": False,
            }

            for tool in plant["activeTools"]:
                if tool["type"] == "WATER":
                    _plant["water"] = tool["count"]
                if tool["type"] == "POT":
                    _plant["pot"] = tool["count"]

            has_crow = plant.get("hasCrow")

            if has_crow is not None:
                _plant["crow"] = has_crow

            _plant["stage"] = plant["stage"]

            _plant["temp"] = plant.get("isTempPlant")

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
        print("|| Tentarei novamente mais tarde!")
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

    print("|| Fim da rotina de regar plantas")


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
        print("|| Tentarei novamente mais tarde!")
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

    print("|| Fim da rotina de remover corvos")


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
        print("|| Tentarei novamente mais tarde!")
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

    print("|| || Fim da rotina de colocar vasos")


def remove_plant(plant_id):

    print("|| Removendo a planta:", plant_id)

    url = f"https://backend-farm.plantvsundead.com/farms/{plant_id}/deactivate"
    headers = get_headers()

    payload = {}

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao remover a planta:", plant_id)
    else:
        print("|| Erro ao remover a planta", plant_id)
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente mais tarde!")
        return False

    return True


def harvest_plant(plant_id):
    print("|| Colhendo a planta:", plant_id)

    url = f"https://backend-farm.plantvsundead.com/farms/{plant_id}/harvest"
    headers = get_headers()

    payload = {}

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao colher planta:", plant_id)
    elif '"status":11' in response.text:
        print("|| A planta não pode mais ser colhida:", plant_id)
        return 11
    elif '"status":15' in response.text:
        print("|| A planta já está com o limite de colheita:", plant_id)
    elif '"status":20' in response.text:
        print("|| Não precisa colher a planta novamente:", plant_id)
    elif '"status":28' in response.text:
        print("|| Você já atingiu o limite diário de colher plantas.")
    else:
        print("|| Erro ao colher a planta", plant_id)
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente mais tarde!")
        return False

    return True


def harvest_plants(plants=None):
    print("|| Iniciando a rotina de colher plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        if plant["stage"] == "cancelled":
            status = harvest_plant(plant["id"])
            if status == 11 or status == True:
                if plant["temp"]:
                    remove_plant(plant["id"])

        random_sleep()
        print(f"|| Planta {plant['id']} foi colhida")

    print("|| Fim da rotina de colher plantas")


def add_plant(plant_id):

    if plant_id == 1:
        print("|| Adicionando uma planta Sunflower Sapling")
    else:
        print("|| Adicionando uma planta Sunflower Mama")

    url = f"https://backend-farm.plantvsundead.com/farms"
    headers = get_headers()

    payload = {"landId": 0, "sunflowerId": plant_id}

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        print("|| Sucesso ao adicionar a planta:")
    elif '"status":14' in response.text:
        print("|| Você está no limite de plantas")
    else:
        print("|| Erro ao adicionar a planta")
        print("|| => Resposta:", response.text)
        print("|| Tentarei novamente mais tarde!")
        return False

    return True


def get_farm_lands():
    url = "https://backend-farm.plantvsundead.com/my-lands?limit=9&offset=0"

    headers = get_headers()

    print("|| Pegando as minhas Sunflowers")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    farm_info = json.loads(response.text)

    lands = farm_info.get("data")

    return lands


def get_available_spaces():
    land = get_farm_lands()[0]
    capacity = land["land"]["capacity"]
    current = land["totalFarming"]
    available_tree = capacity["plant"] - current["plant"]
    available_mother = capacity["motherTree"] - current["motherTree"]

    return {"tree": available_tree, "mother": available_mother}


def add_plants():
    print("|| Iniciando rotina de adicionar novas plantas")
    available_lands = get_available_spaces()

    available_trees = available_lands["tree"]
    for _ in range(available_trees):
        add_plant(1)

    available_mothers = available_lands["mother"]
    for _ in range(available_mothers):
        add_plant(2)

    if available_trees > 0 or available_mothers > 0:
        use_pots()
        water_plants()

    print("|| Fim da rotina de adicionar novas plantas")
