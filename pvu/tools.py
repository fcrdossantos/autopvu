import json
import requests
from pvu.utils import get_headers, random_sleep
import os
from logs import log


def get_all_tools():
    url = "https://backend-farm.plantvsundead.com/available-tools"
    headers = get_headers()

    log("Pegando todas as ferramentas disponíveis")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    tool_info = json.loads(response.text)

    tools = tool_info.get("data")

    return tools


def get_my_tools():
    url = "https://backend-farm.plantvsundead.com/my-tools"
    headers = get_headers()

    log("Pegando todas as minhas ferramentas")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    tool_info = json.loads(response.text)

    tools = tool_info.get("data")

    return tools
