import os
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


def play_game():

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            driver.get("https://marketplace.plantvsundead.com/farm#/farm/")
    except:
        print(
            "|| Impossível acessar a página da fazenda para iniciar as rotinas do bot"
        )

    random_sleep(min_time=3)
    wait_maintenance()

    now = datetime.now().strftime("%H:%M:%S")
    print(f"|| [{now}] Jogo disponível! Iniciando")

    print(f"|| Hora de pegar informações da sua fazenda!")
    random_sleep(3)
    get_user_info()

    print("|| Hora de colocar os vasos")
    random_sleep(3)
    use_pots()

    print("|| Hora de regar plantas!")
    random_sleep(3)
    water_plants()

    print("|| Hora de remover corvos")
    random_sleep(3)
    remove_crows()

    print("|| Hora de colher as plantas")
    random_sleep(3)
    harvest_plants()

    print("|| Hora de adicionar novas plantas")
    random_sleep(3)
    add_plants()

    if os.getenv("DAILY").lower() in ("true", "1"):
        print("|| Hora de fazer a missão diária")
        random_sleep(3)
        do_daily()

    print(f"|| [{now}] Tudo feito! Até mais tarde :)")
    random_sleep(60 * 15)
