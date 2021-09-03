# -*- coding: utf-8 -*-
import json
import requests
from pvu.utils import get_backend_url, get_headers, random_sleep
import os
from logs import log


def get_all_tools():
    url = f"{get_backend_url()}/available-tools"
    headers = get_headers()

    log("Pegando todas as ferramentas disponíveis")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    tool_info = json.loads(response.text)

    if tool_info.get("status") == 444:
        raise Exception("Entrou em Manutenção")

    tools = tool_info.get("data")

    return tools


def get_my_tools():
    url = f"{get_backend_url()}/my-tools"
    headers = get_headers()

    log("Pegando todas as minhas ferramentas")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    tool_info = json.loads(response.text)

    if tool_info.get("status") == 444:
        raise Exception("Entrou em Manutenção")

    tools = tool_info.get("data")

    return tools
