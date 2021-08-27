import json
import requests
from pvu.utils import get_headers, random_sleep
import os


def get_all_tools():
    url = "https://backend-farm.plantvsundead.com/available-tools"
    headers = get_headers()

    print("|| Pegando todas as ferramentas disponíveis")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)

    tools = user_info.get("data")

    return tools


def get_my_tools():
    url = "https://backend-farm.plantvsundead.com/my-tools"
    headers = get_headers()

    print("|| Pegando todas as minhas ferramentas")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    user_info = json.loads(response.text)

    tools = user_info.get("data")

    return tools
