# -*- coding: utf-8 -*-
import requests
import json

from pvu.land import water_land
from pvu.utils import get_backend_url, get_headers, random_sleep
from browser import get_browser
from logs import log
import os


def get_daily_status():

    url = f"{get_backend_url()}/world-tree/datas"

    headers = get_headers()

    random_sleep()

    response = requests.request("GET", url, headers=headers)

    response = json.loads(response.text)

    return response


def water_world_tree(daily_water):
    log("Regando a Árvore Global")

    url = f"{get_backend_url()}/world-tree/give-waters"

    headers = get_headers()

    random_sleep()

    payload = {"amount": daily_water}

    response = requests.request("POST", url, json=payload, headers=headers)

    response = json.loads(response.text)

    if response["status"] == 0:
        return True

    log("Erro ao aguar a planta global:", response)
    return False


def claim_reward(reward_type):
    log(f"Pegando a recompensa {reward_type}")
    url = f"{get_backend_url()}/world-tree/claim-reward"

    headers = get_headers()

    random_sleep()

    payload = {"type": reward_type}

    response = requests.request("POST", url, json=payload, headers=headers)

    response = json.loads(response.text)

    if response["status"] == 0:
        log(f"Conseguimos pegar a recompensa {reward_type}")
        return True

    log("Erro ao pegar a recompensa:", response)
    return False


def claim_yesterday_rewards():
    url = f"{get_backend_url()}/world-tree/claim-yesterday-reward"

    headers = get_headers()

    random_sleep()

    response = requests.request("POST", url, headers=headers)

    response = json.loads(response.text)

    if response["status"] == 0:
        log("Conseguimos pegar a recompensa de ontem")
        return True

    log("Erro ao pegar a recompensa de ontem:", response)
    return False


def claim_rewards(datas):
    log("Verificando as Recompensas")

    log("Verificando se tem recompensas de ontem para pegar")
    if datas.get("data").get("yesterdayReward"):
        log("Temos recompensas de ontem para pegar")
        claim_yesterday_rewards()
    else:
        log("Não temos recompensas de ontem para pegar")

    log("Verificando as recompensas de hoje")

    for reward in datas.get("data").get("reward"):
        random_sleep()
        if reward.get("status") == "finish":
            reward_type = reward.get("type")
            log(f"Vamos pegar a Recompensa {reward_type}")
            claim_reward(reward_type)
        elif reward.get("status") == "rewarded":
            log(f"Já pegou a Recompensa {reward.get('type')}")
        else:
            log(f"A recompensa {reward.get('type')} ainda não foi concluída")


def do_daily():
    log("Iniciando a Missão Diária")

    random_sleep()

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(f"https://marketplace.plantvsundead.com/farm#/worldtree")
        except:
            log("Erro ao redirecionar para a página da árvore global")

    log("Pegando o status atual da Missão Diária")
    daily = get_daily_status()

    my_water = daily.get("data").get("myWater")

    tries = 0
    while my_water is None:
        daily = get_daily_status()
        my_water = daily.get("data").get("myWater")
        tries += 1
        if tries >= 3:
            my_water = 0
            break

    daily_water = int(os.getenv("DAILY_WATER", "20"))

    random_sleep()

    log(
        f"Você já aguou {my_water} vezes a Árvore Global, de um total de {daily_water} regadas necessárias"
    )

    if daily_water < 20:
        daily_water = 20

    if my_water < daily_water:
        log("Precisamos regar a Árvore Global")
        random_sleep()
        watered = water_world_tree(daily_water)
        tries = 0

        while not watered:
            watered = water_world_tree(daily_water)

            tries += 1
            if tries >= 3:
                log("Impossível aguar a planta global no momento!")
                return False

            random_sleep()

    log("A Árvore Global já foi regada o suficiente")

    random_sleep()

    claim_rewards(daily)

    log("Fim da rotina de missão diária")

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(f"https://marketplace.plantvsundead.com/farm#/farm")
        except:
            log("Erro ao redirecionar para a página da árvore global")
