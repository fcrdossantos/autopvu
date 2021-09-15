# -*- coding: utf-8 -*-
import requests
import json

from pvu.utils import get_backend_url, get_headers, random_sleep
from browser import get_browser
from logs import log
import os
from datetime import datetime, timedelta

LAST_DAY = None
DAILY_DONE = False


def get_last_daily_day():
    log("Verificando o dia da última missão diária (UTC)")
    global LAST_DAY

    if LAST_DAY is None:
        LAST_DAY = datetime.utcnow()

    log("O último dia (UTC) de missão diária foi:", LAST_DAY.strftime("%d/%m/%Y"))

    return LAST_DAY


def reset_daily_day():
    log("Verificando se estamos em um novo dia para missões diárias (UTC)")
    global LAST_DAY
    global DAILY_DONE

    now = datetime.utcnow()
    daily_day = get_last_daily_day()

    if now.day != daily_day.day:
        log(f"Estamos num novo dia (UTC): {now.strftime('%d/%m/%Y')}")
        log("Vamos resetar para fazer a missão diária")
        LAST_DAY = now
        DAILY_DONE = False
    else:
        log("Ainda estamos no dia da última missão diária")


def check_daily_done():
    global DAILY_DONE

    if DAILY_DONE:
        log("Já terminamos as missões diárias de hoje")
    else:
        log("Ainda temos tarefas da missão diária de hoje")

    return DAILY_DONE


def check_daily(datas):
    global DAILY_DONE

    log("Verificando se completamos todas as missões diária")

    if datas.get("data").get("yesterdayReward"):
        log("Ainda temos recompensas de ontem para pegar")
        return True

    for reward in datas.get("data").get("reward"):
        random_sleep()
        if reward.get("status") != "rewarded":
            log("Ainda temos missão de hoje para fazer")
            return True

    log("Já terminamos a missão diária de hoje")
    DAILY_DONE = True
    return False


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
        try:
            rewards = response.get("data")
            if rewards:
                if rewards.get("le"):
                    log(f"=> LE: {rewards.get('le')}")
                if rewards.get("sapling"):
                    log(f"=> Sapling: {rewards.get('sapling')}")
                if rewards.get("sunBox"):
                    log(f"=> Sun Box: {rewards.get('sunBox')}")
                if rewards.get("sunBox") > 0:
                    sunbox_reward = rewards.get("sunBoxReward")
                    if sunbox_reward:
                        infos = [x for x in sunbox_reward.keys()]
                        log(f"==> Prêmio da Sun Box: {infos[-1]}")
        except Exception as e:
            log("Erro ao decifrar a recompensa:", e)
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
        try:
            rewards = response.get("data").get("rewards")
            if rewards:
                for reward in rewards:
                    if reward.get("le"):
                        log(f"=> LE: {reward.get('le')}")
                    if reward.get("sapling"):
                        log(f"=> Sapling: {reward.get('sapling')}")

            sunbox_rewards = response.get("data").get("sunBoxRewards")
            if sunbox_rewards:
                if len(sunbox_rewards) > 0:
                    for sunbox_reward in sunbox_rewards:
                        infos = [x for x in sunbox_reward]
                        if len(infos) > 1:
                            log(f"==> Prêmio da Sun Box: {infos[-1]}")
                        else:
                            if type(infos) == list:
                                log(f"==> Prêmio da Sun Box: {infos[0]}")
                            else:
                                log(f"==> Prêmio da Sun Box: {infos}")
        except Exception as e:
            log("Impossível decifrar a recompensa de ontem:", e)
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


def do_daily(daily=None):
    log("Iniciando a Missão Diária")

    random_sleep()

    log("Redirecionando para a página da missão diária")
    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(f"https://marketplace.plantvsundead.com/farm#/worldtree")
        except:
            log("Erro ao redirecionar para a página da árvore global")

    if daily is None:
        log("Pegando novo status da Missão Diária")
        daily = get_daily_status()
    else:
        log("Pegando o status atual da Missão Diária")

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

    daily = get_daily_status()

    log("Verificando se ainda tem recompensas faltando")

    check_daily(daily)

    log("Voltando para a página da fazenda")
    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()

            if driver is not None:
                random_sleep()
                driver.get(f"https://marketplace.plantvsundead.com/farm#/farm")
        except:
            log("Erro ao redirecionar para a página da fazenda")
