# -*- coding: utf-8 -*-
import json
from pvu.user import get_user
import time
import os
import requests
import random
from pvu.utils import get_headers, random_sleep, get_backend_url
from pvu.captcha import solve_validation_captcha, get_captcha
from logs import log

# List all farm infos and status
def get_farm_infos():
    log("Coletando as informações da fazenda")
    url = f"{get_backend_url()}/farms"

    querystring = {"limit": "10", "offset": "0"}

    payload = ""
    headers = get_headers()

    random_sleep()
    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    farm_info = json.loads(response.text)

    status = farm_info["status"]

    if status == 444:
        raise Exception("Entrou em manutenção")

    return farm_info


# Get all plants infos (ID and WATER)
def get_plants():
    log("Coletando as informações das plantas")
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


def water_plant(plant_id, need_captcha=False):
    log("Aguando a planta:", plant_id)

    url = f"{get_backend_url()}/farms/apply-tool"

    items = get_user()["items"]

    for item in items:
        if item["id"] == 3 and item["type"] == "tool":
            if item["current_amount"] == 0:
                log("Você não tem água suficiente para isso")
                return 404

    if need_captcha:
        captcha_results = get_captcha()
        if not captcha_results:
            raise Exception("Entrou em manutenção")
    else:
        captcha_results = {
            "challenge": "default",
            "seccode": "default",
            "validate": "default",
        }

    if need_captcha:
        solved = solve_validation_captcha(captcha_results)
        while not solved:
            captcha_results = get_captcha()
            if not captcha_results:
                raise Exception("Entrou em manutenção")
            solved = solve_validation_captcha(captcha_results)

    try:
        payload = {
            "farmId": plant_id,
            "toolId": 3,
            "token": {
                "challenge": captcha_results.get("challenge"),
                "seccode": captcha_results.get("seccode"),
                "validate": captcha_results.get("validate"),
            },
        }
    except Exception as e:
        log("Ocorreu um erro ao descriptografar o resultado do captcha:", e)
        log("Resultado:", captcha_results, " => ", type(captcha_results))
        return False

    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        log("Sucesso ao regar a planta:", plant_id)
    elif '"status":15' in response.text:
        log("Você não tem mais Águas para regar a planta:", plant_id)
    elif '"status":20' in response.text:
        log("Não precisa mais regar a planta:", plant_id)
    elif '"status":28' in response.text:
        log("Você já regou as 15 plantas hoje, não podemos regar mais.")
    elif '"status":16' in response.text:
        log("Essa planta já foi regada as 200 vezes hoje!")
        return False
    elif '"status":556' in response.text:
        log("Precisa de Captcha para regar")
        return 556
    elif '"status":10' in response.text:
        log("Deu erro de Status 10. Vou pular essa planta")
        return 10
    else:
        log("Erro ao regar a planta", plant_id)
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False
    return 1


def water_plants(plants=None):
    log("Iniciando a rotina de regar plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        if plant.get("stage") == "farming":
            while plant["water"] < 2:
                random_sleep()
                result_water = water_plant(plant["id"])

                if result_water == 556:
                    result_water = water_plant(plant["id"], need_captcha=True)

                if result_water == 10:
                    plant["water"] = 3
                    continue

                if result_water == 1:
                    plant["water"] += 1

                if result_water == 404:
                    return

            random_sleep()
            log(f"Planta {plant['id']} terminou de ser regada")

    log("Fim da rotina de regar plantas")


def remove_crow(plant_id, need_captcha=False):
    log("Removendo corvo da planta:", plant_id)

    url = f"{get_backend_url()}/farms/apply-tool"

    items = get_user()["items"]
    for item in items:
        if item["id"] == 4 and item["type"] == "tool":
            if item["current_amount"] == 0:
                log("Você não tem corvo suficiente para isso")
                return 404

    if need_captcha:
        captcha_results = get_captcha()
        if not captcha_results:
            raise Exception("Entrou em manutenção")
    else:
        captcha_results = {
            "challenge": "default",
            "seccode": "default",
            "validate": "default",
        }

    if need_captcha:
        solved = solve_validation_captcha(captcha_results)
        while not solved:
            captcha_results = get_captcha()
            if not captcha_results:
                raise Exception("Entrou em manutenção")
            solved = solve_validation_captcha(captcha_results)

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
        log("Sucesso ao remover o corvo da planta:", plant_id)
    elif '"status":15' in response.text:
        log("Você não tem mais Espantalhos para tirar corvos da planta:", plant_id)
    elif '"status":20' in response.text:
        log("Não precisa mais tirar corvos da planta:", plant_id)
    elif '"status":28' in response.text:
        log("Você já tirou corvos das 5 plantas hoje, não podemos remover mais.")
    elif '"status":556' in response.text:
        log("Precisa de Captcha para tirar o corvo")
        return 556
    elif '"status":10' in response.text:
        log("Deu erro de Status 10. Vou pular essa planta")
        return 10
    else:
        log("Erro ao remover o corvo da planta", plant_id)
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False
    return 1


def remove_crows(plants=None):
    log("Iniciando a rotina de remover corvos")

    if plants is None:
        plants = get_plants()

    for plant in plants:

        if plant.get("stage") == "farming":
            while plant["crow"]:
                random_sleep()
                result_crow = remove_crow(plant["id"])

                if result_crow == 556:
                    result_crow = remove_crow(plant["id"], need_captcha=True)

                if result_crow == 10:
                    plant["crow"] = False
                    continue

                if result_crow == 1:
                    plant["crow"] = False

                if remove_crow == 404:
                    return

            random_sleep()
            log(f"Planta {plant['id']} não tem mais corvos")

    log("Fim da rotina de remover corvos")


def use_pot(plant_id, need_captcha=False):
    log("Colocando pote na planta:", plant_id)

    url = f"{get_backend_url()}/farms/apply-tool"

    if os.getenv("POT_TYPE", "SMALL").lower() in ("big", "2"):
        tool_id = 2
    else:
        tool_id = 1

    items = get_user()["items"]

    for item in items:
        if item["id"] == tool_id and item["type"] == "tool":
            if item["current_amount"] == 0:
                log("Você não tem vasos suficientes para isso")
                return 404

    if need_captcha:
        captcha_results = get_captcha()
        if not captcha_results:
            raise Exception("Entrou em manutenção")
    else:
        captcha_results = {
            "challenge": "default",
            "seccode": "default",
            "validate": "default",
        }

    if need_captcha:
        solved = solve_validation_captcha(captcha_results)
        while not solved:
            captcha_results = get_captcha()
            if not captcha_results:
                raise Exception("Entrou em manutenção")
            solved = solve_validation_captcha(captcha_results)

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
        log("Sucesso ao colocar o vaso na planta:", plant_id)
    elif '"status":15' in response.text:
        log("A planta já está com o limite de vasos:", plant_id)
    elif '"status":20' in response.text:
        log("Não precisa mais colocar vasos na planta:", plant_id)
    elif '"status":28' in response.text:
        log("Você já atingiu o limite diário de colocar vasos.")
    elif '"status":556' in response.text:
        log("Precisa de Captcha para colocar o vaso")
        return 556
    elif '"status":10' in response.text:
        log("Erro de Status 10. Vou pular essa planta")
        return 10
    else:
        log("Erro ao colocar o vaso na planta", plant_id)
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False
    return 1


def use_pots(plants=None):
    log("Iniciando a rotina de colocar vasos nas plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:

        if plant["stage"] == "new":
            log(f"A planta é nova e precisa de um vaso")
            result_pot = use_pot(plant["id"])

            if result_pot == 556:
                result_pot = use_pot(plant["id"], need_captcha=True)

            if result_pot == 404:
                return

            continue

        while plant["pot"] == 0:
            random_sleep()
            result_pot = use_pot(plant["id"])

            if result_pot == 556:
                result_pot = use_pot(plant["id"], need_captcha=True)

            if result_pot == 1:
                plant["pot"] = 1

            if result_pot == 10:
                plant["pot"] = 1
                continue

            if result_pot == 404:
                return

        random_sleep()
        log(f"Planta {plant['id']} não precisa de vasos")

    log("Fim da rotina de colocar vasos")


def remove_plant(plant_id):

    log("Removendo a planta:", plant_id)

    url = f"https://backend-farm-stg.plantvsundead.com/farms/{plant_id}/deactivate"
    headers = get_headers()

    payload = {}

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        log("Sucesso ao remover a planta:", plant_id)
    else:
        log("Erro ao remover a planta", plant_id)
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False

    return True


def harvest_plant(plant_id):
    log("Colhendo a planta:", plant_id)

    url = f"https://backend-farm-stg.plantvsundead.com/farms/{plant_id}/harvest"
    headers = get_headers()

    payload = {}

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        log("Sucesso ao colher planta:", plant_id)
    elif '"status":11' in response.text:
        log("A planta não pode mais ser colhida:", plant_id)
        return 11
    elif '"status":15' in response.text:
        log("A planta já está com o limite de colheita:", plant_id)
    elif '"status":20' in response.text:
        log("Não precisa colher a planta novamente:", plant_id)
    elif '"status":28' in response.text:
        log("Você já atingiu o limite diário de colher plantas.")
    else:
        log("Erro ao colher a planta", plant_id)
        if response.text.startswith("<!DOCTYPE html>"):
            log("Erro HTML => Página/Gateway não alcançável")
        else:
            log("=> Resposta:", response.text[:])
        log("Tentarei novamente mais tarde!")
        return False

    return True


def harvest_plants(plants=None):
    log("Iniciando a rotina de colher plantas")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        if plant["stage"] == "cancelled":
            status = harvest_plant(plant["id"])
            if status == 11 or status == True:
                if plant["temp"]:
                    remove_plant(plant["id"])

        random_sleep()
        log(f"Planta {plant['id']} foi colhida")

    log("Fim da rotina de colher plantas")


def add_plant(plant_id):

    if plant_id == 1:
        log("Adicionando uma planta Sunflower Sapling")
    else:
        log("Adicionando uma planta Sunflower Mama")

    url = f"https://backend-farm-stg.plantvsundead.com/farms"
    headers = get_headers()

    payload = {"landId": 0, "sunflowerId": plant_id}

    items = get_user()["items"]

    for item in items:
        if item["id"] == plant_id and item["type"] == "sunflower":
            if item["current_amount"] == 0:
                log("Você não tem planta suficiente para isso")
                return 404

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        log("Sucesso ao adicionar a planta:")
    elif '"status":14' in response.text:
        log("Você está no limite de plantas")
    else:
        log("Erro ao adicionar a planta")
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False

    return True


def get_farm_lands():
    url = f"{get_backend_url()}/my-lands?limit=9&offset=0"

    headers = get_headers()

    log("Pegando as minhas Terras da Fazenda")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    farm_info = json.loads(response.text)

    if farm_info.get("status") == 444:
        raise Exception("Entrou em manutenção")

    lands = farm_info.get("data")

    return lands


def get_available_spaces():
    lands = get_farm_lands()

    for land in lands:
        capacity = land["land"]["capacity"]
        current = land["totalFarming"]
        available_tree = capacity["plant"] - current["plant"]
        available_mother = capacity["motherTree"] - current["motherTree"]

        return {"tree": available_tree, "mother": available_mother}


def add_plants():
    log("Iniciando rotina de adicionar novas plantas")
    available_lands = get_available_spaces()

    available_trees = available_lands["tree"]
    for _ in range(available_trees):
        add_plant(1)

    available_mothers = available_lands["mother"]
    for _ in range(available_mothers):
        add_plant(2)

    if available_trees > 0 or available_mothers > 0:
        plants = get_plants()
        use_pots(plants)
        water_plants(plants)

    log("Fim da rotina de adicionar novas plantas")


def check_need_actions(plants=None):

    log("Verificando se alguma ação será necessária")

    if plants is None:
        plants = get_plants()

    for plant in plants:
        if plant.get("stage") == "farming":
            if plant["water"] < 2:
                log("Ações serão necessárias (algumas plantas precisam ser regadas)")
                return True

            if plant["crow"]:
                log("Ações serão necessárias (algumas plantas possuem corvo)")
                return True

            if plant["pot"]:
                log(
                    "Ações serão necessárias (algumas plantas precisam ser colocadas no vaso)"
                )
                return True

        if plant.get("stage") == "new":
            log("Ações serão necessárias (algumas plantas são novas)")
            return True

        if plant["stage"] == "cancelled":
            log("Ações serão necessárias (algumas plantas precisam ser colhidas")
            return True

    log("Nenhuma ação será necessária")

    return False
