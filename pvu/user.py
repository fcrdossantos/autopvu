import requests
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import get_browser
from pvu.utils import get_headers, random_sleep


def get_pvu():
    random_sleep()
    driver = get_browser()

    xpath_pvu = "/html/body/div[1]/div/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[2]"

    print("|| Pegando seus PVU's")

    try:
        pvus = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_pvu))
        )

        return {"pvu": pvus.text}
    except:
        return {"pvu": "0"}


def get_le():
    url = "https://backend-farm.plantvsundead.com/farming-stats"
    headers = get_headers()

    print("|| Pegando seus LE's")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)
    le = user_info.get("data").get("leWallet")

    return {"le": le}


def get_tools():
    available_tools = {
        "Water": 0,
        "Scarecrow": 0,
        "Big Pot": 0,
        "Small Pot": 0,
        "Greenhouse": 0,
    }

    url = "https://backend-farm.plantvsundead.com/my-tools"
    headers = get_headers()

    print("|| Pegando suas ferramentas")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)

    tools = user_info.get("data")

    for tool in tools:
        name = tool.get("name")
        count = tool.get("usages")
        available_tools[name] = count

    return available_tools


def get_user_info():
    print("|| Pegando as informações do usuário")

    farm_url = "https://marketplace.plantvsundead.com/farm#/farm/"

    try:
        driver = get_browser()

        if driver is not None:
            random_sleep()
            if driver.current_url != farm_url:
                driver.get(farm_url)
    except:
        print("Impossível ir para a página principal da fazenda")

    pvu = get_pvu()
    le = get_le()
    tools = get_tools()

    print("|| Você possui:")
    print(f"|| => {pvu['pvu']} PVU's")
    print(f"|| => {le['le']} LE's")
    print(f"|| => {tools['Small Pot']} Vasos Pequenos")
    print(f"|| => {tools['Big Pot']} Vasos Grandes")
    print(f"|| => {tools['Water']} Águas")
    print(f"|| => {tools['Scarecrow']} Espantalhos")
    print(f"|| => {tools['Greenhouse']} Estufas")

    user_info = pvu
    user_info.update(le)
    user_info.update(tools)

    for info in user_info.keys():
        user_info[info] = float(user_info[info])

    return user_info
