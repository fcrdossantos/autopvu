# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import requests
from pvu.utils import get_headers, random_sleep
from logs import log
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions


def get_weather_source():

    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--ignore-ssl-errors")

        browser_predict = Chrome(options=options)
        browser_predict.get("https://pvuextratools.com/")

        url_js = None
        for request in browser_predict.requests:
            if "pvuextratools" in request.url and request.url.endswith(".js"):
                url_js = request.url

        if url_js is None:
            url_js = "https://pvuextratools.com/4.2404369364c20cfd53d4.js"

        browser_predict.close()
    except:
        log("Erro: A fonte de previsões climáticas não está mais ativa")

    return url_js


def get_weather():

    url = "https://backend-farm.plantvsundead.com/weather-today"

    headers = get_headers()

    random_sleep()

    response = requests.request("GET", url, headers=headers)

    response = json.loads(response.text)

    return response


def get_season():
    season = get_weather()["data"]["season"]
    return season


def next_season(actual):
    if actual == "winter":
        return "spring"
    elif actual == "spring":
        return "summer"
    elif actual == "summer":
        return "autumn"
    elif actual == "autumn":
        return "winter"


def predict_greenhouse(verbose=False):
    try:
        log("Buscando histórico e previsão de climas")
        url = get_weather_source()
        page = requests.get(url)

        page = str(page.content)

        str_start = 'JSON.parse(\\\'{"yesterdaySeason"'
        start = page.index(str_start) + len("JSON.parse(\\'")
        end = page.index("}]}\\')") + len("}]}")

        predict = json.loads(page[start:end])

        forecasts = predict["forecast"]

        use_greenhouse = {}

        log("Calculando a probalidade do clima de amanhã ser bom ou ruim")
        risk = int(os.getenv("GREENHOUSE_RISK_PERCENTAGE", "33"))
        log(f"=> Risco máximo de {risk}%")
        for forecast in forecasts:
            plant = forecast["type"]
            good = forecast["positiveProbability"]
            bad = forecast["negativeProbability"]
            use = bad >= good and bad > 0
            neutral = 100 - good - bad

            if bad >= risk:
                use = True

            if verbose:
                use_str = "Usar" if use else "Não usar"
                log(
                    f"{plant}: {good}% bom x {bad}% ruim x {neutral}% neutro => {use_str} estufa"
                )

            use_greenhouse[plant.lower()] = use

        return use_greenhouse

    except:
        now = datetime.utcnow()
        today = now.weekday()

        season = get_season()

        changing_season_tomorrow = False

        if today == 5:
            changing_season_tomorrow = True

        if changing_season_tomorrow:
            season = next_season(season)

        use_greenhouse = {
            "dark": False,
            "electro": False,
            "fire": False,
            "ice": False,
            "light": False,
            "metal": False,
            "parasite": False,
            "water": False,
            "wind": False,
        }

        if season == "autumn":
            use_greenhouse["fire"] = True
            use_greenhouse["light"] = True
            use_greenhouse["metal"] = True

        elif season == "summer":
            use_greenhouse["ice"] = True
            use_greenhouse["metal"] = True

        elif season == "spring":
            use_greenhouse["fire"] = True
            use_greenhouse["light"] = True

        return use_greenhouse
