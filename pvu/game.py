# -*- coding: utf-8 -*-
import os
import traceback
from datetime import datetime
from typing import Tuple

from browser import get_browser
from logs import log

from pvu.captcha import start_captcha_solver, stop_captcha_solver
from pvu.daily import check_daily_done, do_daily, get_daily_status, reset_daily_day
from pvu.farm import (
    add_greenhouses,
    add_plants,
    check_need_actions,
    get_plants,
    harvest_plants,
    harvest_seeds,
    remove_crows,
    use_pots,
    water_plants,
)
from pvu.maintenance_v2 import wait_maintenance
from pvu.store import buy_items
from pvu.user import get_le, get_user, get_user_info, reset_user
from pvu.utils import random_sleep, reset_backend_url


def play_game():

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            driver.get("https://marketplace.plantvsundead.com/farm#/farm/")
    except:
        log("Impossível acessar a página da fazenda para iniciar as rotinas do bot")
        # random_sleep(60 * 8, min_time=60 * 3.6)
        # return -100

    random_sleep(min_time=3)
    maintenance = wait_maintenance()

    if maintenance:
        driver.refresh()

    log(f"Jogo disponível! Iniciando")

    log("Redirecionando para a página da fazenda")

    if not driver.current_url == "https://marketplace.plantvsundead.com/farm#/farm/":
        random_sleep()
        driver.get("https://marketplace.plantvsundead.com/farm#/farm/")
        random_sleep(3)

    log("Iniciando as rotinas")

    try:
        reset_daily_day()
        reset_user()
        reset_backend_url()
    except:
        log("Impossível reiniciar as informações do usuário")
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        log("Pegando as informações das fazendas e plantas")
        plants = get_plants()
        for plant in plants:
            log(f"Status da planta ID {plant['id']}")
            if plant["pot"] == 0:
                log("- Precisa de um vaso")
            else:
                log("- Não precisa de vaso")
            if plant["water"] < 2:
                log(f"- Precisa ser aguada {2 - plant['water']} vezes")
            else:
                log("- Não precisa ser aguada")
            if plant["crow"]:
                log("- Precisa ter um corvo removido")
            else:
                log("- Não possui corvos")
            if plant["stage"] == "cancelled":
                log("- Precisa ser colhida")
            else:
                log("- Não precisa ser colhida")
    except:
        log("Erro ao pegar informações das fazendas e plantas")
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        log("Pegando informações da missão diária")
        if check_daily_done():
            log("Missão diária já finalizada")
            daily = -10
        else:
            daily = get_daily_status()
    except:
        log("Impossível pegar informações da missão diária")
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        log("Hora de verificar se o bot precisará fazer algo")
        need_actions = check_need_actions(plants, daily)
        if need_actions["need_action"]:
            log("Ações necessárias, iniciando rotinas")
        else:
            log("Ações não necessárias no momento, tentaremos mais tarde")
            if os.getenv("LONG_DELAY", "True").lower() in ("true", 1):
                random_sleep(
                    60 * 60 * 10,
                    min_time=60 * 60 * 0.7,
                    max_time=60 * 60 * 2.3,
                    verbose=True,
                )
            else:
                random_sleep(
                    60 * 60 * 2,
                    min_time=60 * 15,
                    max_time=60 * 30,
                    verbose=True,
                )
            return True
    except:
        log("Impossível detectar se alguma ação é necessária")
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if need_actions["need_captcha"]:
            start_captcha_solver()
    except Exception as e:
        log("Erro na rotina de solucionar captchas iniciais:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        log(f"Hora de pegar informações do usuário!")
        random_sleep(3)
        user_info = get_user()
    except Exception as e:
        log("Erro na rotina de pegar informações do usuário:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        harvested = False
        if need_actions["need_harvest"] != 0:
            if os.getenv("HARVEST", "TRUE").lower() in ("true", "1"):
                log("Hora de colher as plantas")
                random_sleep(3)
                harvested = harvest_plants(plants=plants)
    except Exception as e:
        log("Erro na rotina de colher plantas:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if need_actions["plant_action"]:
            log("Recarregando a página da fazenda")
            driver.refresh()
    except:
        log("Impossível recarregar a página da fazenda")

    try:
        daily_rewarded = False
        if os.getenv("DAILY").lower() in ("true", "1"):
            if check_daily_done():
                log("Missão diária já realizada hoje!")
            else:
                log("Hora de fazer a missão diária")
                random_sleep(3)
                do_daily()
                daily_rewarded = True
    except Exception as e:
        log("Erro na rotina de missão diária:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if harvest_plants or daily_rewarded:
            user_info["le"] = get_le()

        user_le = user_info["le"]
        if os.getenv("BUY_ITEMS", "TRUE").lower() in ("true", "1"):
            log("Hora de comprar itens")
            if user_le < int(os.getenv("MIN_LE", 0)):
                log("Você não tem o dinheiro minimo para a rotina de compra")
            else:
                log("Hora de comprar os itens")
                random_sleep(3)
                buy_items()
    except Exception as e:
        log("Erro na rotina de comprar itens:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    if not driver.current_url == "https://marketplace.plantvsundead.com/farm#/farm/":
        random_sleep()
        driver.get("https://marketplace.plantvsundead.com/farm#/farm/")
        random_sleep(3)

    try:
        if os.getenv("POT", "TRUE").lower() in ("true", "1"):
            log("Hora de colocar os vasos")
            random_sleep(3)
            use_pots(plants=plants)
    except Exception as e:
        log("Erro na rotina de colocar vasos:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    plants = get_plants()

    try:
        if os.getenv("WATER", "TRUE").lower() in ("true", "1"):
            log("Hora de regar plantas!")
            random_sleep(3)
            water_plants(plants=plants)
    except Exception as e:
        log("Erro na rotina de aguar plantas:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if os.getenv("CROW", "TRUE").lower() in ("true", "1"):
            log("Hora de remover corvos")
            random_sleep(3)
            remove_crows(plants=plants)
    except Exception as e:
        log("Erro na rotina de remover corvos:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if os.getenv("GREENHOUSE", "TRUE").lower() in ("true", "1"):
            log("Hora de colocar estufas")
            random_sleep(3)
            add_greenhouses(plants=plants)
    except Exception as e:
        log("Erro na rotina de colocar estufas:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if os.getenv("PLANT", "TRUE").lower() in ("true", "1"):
            log("Hora de adicionar novas plantas")
            random_sleep(3)
            add_plants()
    except Exception as e:
        log("Erro na rotina de plantas arvores:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        log("Hora de colher sementes")
        random_sleep(3)
        harvest_seeds(plants=plants)
    except Exception as e:
        log("Erro na rotina de colher sementes:", e)
        traceback.print_exc()
        random_sleep(60 * 8, min_time=60 * 3.6)
        return False

    try:
        if need_actions["plant_action"]:
            log("Recarregando a página da fazenda")
            driver.refresh()
    except:
        log("Impossível recarregar a página da fazenda")

    stop_captcha_solver()
    log(f"Tudo feito! Até mais tarde :)")
    if os.getenv("LONG_DELAY", "True").lower() in ("true", 1):
        random_sleep(
            60 * 60 * 10,
            min_time=60 * 60 * 0.7,
            max_time=60 * 60 * 2.3,
            verbose=True,
        )
    else:
        random_sleep(
            60 * 60 * 2,
            min_time=60 * 15,
            max_time=60 * 30,
            verbose=True,
        )
    return True
