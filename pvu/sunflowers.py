# -*- coding: utf-8 -*-
import json
import requests
from pvu.utils import get_backend_url, get_headers, random_sleep
import os
from logs import log


def get_all_sunflowers():
    url = f"{get_backend_url()}/sunflowers"
    headers = get_headers()

    log("Pegando todas as Sunflowers disponíveis")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    sunflower_info = json.loads(response.text)

    if sunflower_info.get("status") == 444:
        raise Exception("Entrou em Manutenção")

    all_sunflowers = sunflower_info.get("data")

    all_sunflowers = [
        sunflower for sunflower in all_sunflowers if sunflower.get("name") != "Sun Box"
    ]

    return all_sunflowers


def get_my_sunflowers():
    url = f"{get_backend_url()}/my-sunflowers"
    headers = get_headers()

    log("Pegando as minhas Sunflowers")

    random_sleep()
    response = requests.request("GET", url, headers=headers)

    sunflower_info = json.loads(response.text)

    if sunflower_info.get("status") == 444:
        raise Exception("Entrou em Manutenção")

    sunflowers = sunflower_info.get("data")

    return sunflowers
