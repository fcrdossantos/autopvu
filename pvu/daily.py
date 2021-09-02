import requests
import json

from pvu.land import water_land
from pvu.utils import get_headers, random_sleep
from logs import log


def get_daily_status():
    url = "https://backend-farm-stg.plantvsundead.com/daily-quest"

    payload = ""
    headers = get_headers()

    try:
        random_sleep()
        response = requests.request("GET", url, data=payload, headers=headers)

        daily = json.loads(response.text)

        if daily.get("status") == 444:
            raise Exception("Entrou em manutenção")

        if daily.get("status") == 0:
            daily_water = daily.get("data").get("water")
            daily_crow = daily.get("data").get("scarecrow")
            return {"water": daily_water, "crow": daily_crow}

        return None
    except:
        return None


def claim_daily():
    url = "https://backend-farm-stg.plantvsundead.com/daily-quest"

    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, headers=headers)

    if '"status":40' in response.text or '"status":40' in response.text:
        log("Você já pegou o bônus da missão diária hoje!")
    elif '"status":0' in response.text:
        log("Você acabou de receber o prêmio da missão diária!")


def do_daily():
    random_sleep()

    daily = get_daily_status()

    if daily is not None:
        plants_to_water = 15 - daily["water"]

        if plants_to_water > 0:
            random_sleep()
            water_land(plants_to_water)

        claim_daily()
