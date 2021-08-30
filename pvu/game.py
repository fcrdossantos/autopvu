import os
import traceback
from datetime import datetime
from browser import get_browser
from pvu.maintenance import wait_maintenance
from pvu.farm import (
    water_plants,
    remove_crows,
    use_pots,
    harvest_plants,
    add_plants,
)
from pvu.daily import do_daily
from pvu.user import get_user_info
from pvu.utils import random_sleep
from pvu.store import buy_items
from logs import log


def play_game():

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            driver.get("https://marketplace.plantvsundead.com/farm#/farm/")
    except:
        log("Impossível acessar a página da fazenda para iniciar as rotinas do bot")

    random_sleep(min_time=3)

    wait_maintenance()

    log(f"Jogo disponível! Iniciando")

    try:
        log(f"Hora de pegar informações da sua fazenda!")
        random_sleep(3)
        get_user_info()
    except Exception as e:
        log("Erro na rotina de pegar informações do usuário:", e)
        traceback.print_exc()

    try:
        if os.getenv("BUY_ITEMS", "TRUE").lower() in ("true", "1"):
            log("Hora de comprar os itens")
            random_sleep(3)
            buy_items()
    except Exception as e:
        log("Erro na rotina de comprar itens:", e)
        traceback.print_exc()

    try:
        if os.getenv("POT", "TRUE").lower() in ("true", "1"):
            log("Hora de colocar os vasos")
            random_sleep(3)
            use_pots()
    except Exception as e:
        log("Erro na rotina de colocar vasos:", e)
        traceback.print_exc()

    try:
        if os.getenv("WATER", "TRUE").lower() in ("true", "1"):
            log("Hora de regar plantas!")
            random_sleep(3)
            water_plants()
    except Exception as e:
        log("Erro na rotina de aguar plantas:", e)
        traceback.print_exc()

    try:
        if os.getenv("CROW", "TRUE").lower() in ("true", "1"):
            log("Hora de remover corvos")
            random_sleep(3)
            remove_crows()
    except Exception as e:
        log("Erro na rotina de remover corvos:", e)
        traceback.print_exc()

    try:
        if os.getenv("HARVEST", "TRUE").lower() in ("true", "1"):
            log("Hora de colher as plantas")
            random_sleep(3)
            harvest_plants()
    except Exception as e:
        log("Erro na rotina de colher plantas:", e)
        traceback.print_exc()

    try:
        if os.getenv("PLANT", "TRUE").lower() in ("true", "1"):
            log("Hora de adicionar novas plantas")
            random_sleep(3)
            add_plants()
    except Exception as e:
        log("Erro na rotina de plantas arvores:", e)
        traceback.print_exc()

    try:
        if os.getenv("DAILY").lower() in ("true", "1"):
            log("Hora de fazer a missão diária")
            random_sleep(3)
            do_daily()
    except Exception as e:
        log("Erro na rotina de missão diária:", e)
        traceback.print_exc()

    try:
        if os.getenv("BUY_ITEMS", "TRUE").lower() in ("true", "1"):
            log("Hora de comprar itens usados nas rotinas")
            random_sleep(3)
            buy_items()
    except Exception as e:
        log("Erro na rotina de comprar itens:", e)
        traceback.print_exc()

    log(f"Tudo feito! Até mais tarde :)")
    random_sleep(60 * 15)
