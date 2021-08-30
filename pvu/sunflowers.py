import json
import requests
from pvu.utils import get_headers, random_sleep
import os
from logs import log


def get_all_sunflowers():
    url = "https://backend-farm.plantvsundead.com/sunflowers"
    headers = get_headers()

    log("Pegando todas as Sunflowers disponíveis")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    sunflower_info = json.loads(response.text)

    all_sunflowers = sunflower_info.get("data")

    all_sunflowers = [
        sunflower for sunflower in all_sunflowers if sunflower.get("name") != "Sun Box"
    ]

    return all_sunflowers


def get_my_sunflowers():
    url = "https://backend-farm.plantvsundead.com/my-sunflowers"
    headers = get_headers()

    log("Pegando as minhas Sunflowers")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    sunflower_info = json.loads(response.text)

    tools = sunflower_info.get("data")

    return tools
