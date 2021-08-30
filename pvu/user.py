import requests
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import get_browser
from pvu.utils import get_headers, random_sleep
from pvu.items import get_items
from logs import log


def get_pvu():
    random_sleep()
    driver = get_browser()

    xpath_pvu = "/html/body/div[1]/div/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]"

    log("Pegando seus PVU's")

    try:
        pvus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_pvu))
        )

        return float(pvus.text)
    except:
        log("Não conseguimos pegar seus PVU's")
        return 0.0


def get_le():
    url = "https://backend-farm.plantvsundead.com/farming-stats"
    headers = get_headers()

    log("Pegando seus LE's")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)
    le = user_info.get("data").get("leWallet")

    if le is not None and len(le) > 0:
        return int(le)
    else:
        log("Erro ao pegar os LES:", user_info)
        return 0


def get_user_info():
    farm_url = "https://marketplace.plantvsundead.com/farm#/farm/"

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            if driver.current_url != farm_url:
                driver.get(farm_url)
    except:
        log("Impossível ir para a página principal da fazenda")

    pvu = get_pvu()
    le = get_le()
    items = get_items()

    log("Você possui:")
    log(f" => {pvu} PVU's")
    log(f" => {le} LE's")
    for item in items:
        log(f" => {item.get('current_amount')} {item.get('name')}")
