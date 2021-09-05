# -*- coding: utf-8 -*-
import math
import requests
import os
from pvu.utils import get_headers, random_sleep, get_backend_url
from pvu.items import get_items
from browser import get_browser
from pvu.user import get_le, get_user, update_user
from logs import log
from pvu.user import get_user


def buy_item(item, buy_times):

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()
            store_url = "https://marketplace.plantvsundead.com/farm#/farm/shop/"

            if driver is not None:
                if driver.current_url != store_url:
                    driver.get(store_url)
                    random_sleep()
        except:
            log("Erro ao redirecionar para a página da loja")

    item_id = item["id"]

    total_price = item["price"] * buy_times
    user = get_user()

    total_le = user["le"]

    if total_le < total_price:
        buy_times = total_le // item["price"]
        if buy_times == 0:
            total_le = get_le()
            buy_times = total_le // item["price"]

    if buy_times == 0:
        log("Você não tem dinheiro pra comprar esse item")
        return 999

    times_text = "vez" if buy_times == 1 else "vezes"

    log(f"Vou comprar {item['name']} {buy_times} {times_text}")

    if item["type"] == "tool":
        url = f"{get_backend_url()}/buy-tools"
        payload = {"amount": buy_times, "toolId": item_id}
    else:
        url = f"{get_backend_url()}/buy-sunflowers"
        payload = {"amount": buy_times, "sunflowerId": item_id}

    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        total_price = item["price"] * buy_times
        user["le"] -= total_price

        for _item in user["items"]:
            if _item["id"] == item_id:
                _item["current_amount"] += buy_times * _item["buy_amount"]

        update_user(user)
        log("Sucesso ao comprar o item:", item["name"])
    elif '"status":9' in response.text:
        log("Você não tem dinheiro para comprar o item:", item["name"])
        return 999
    else:
        log("Erro ao comprar o item:", item["name"])
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False

    return True


def buy_items():
    log("Iniciando a rotina de comprar itens")

    log("Pegando seus itens atuais e necessidades de compra")
    items = get_user()["items"]

    log("Verificando se é necessário comprar algum item")

    need_buy = True

    tries = 0

    while need_buy:
        need_buy = False
        cant_buy = 0
        needed = 0

        for item in items:
            current_amount = item["current_amount"]
            min_amount = item["min_amount"]

            if current_amount < min_amount:
                buy_amount = min_amount - current_amount
                if os.getenv("SINGLE_BUY", "False").lower() in ("true", 1):
                    buy_times = 1
                else:
                    buy_times = math.ceil(buy_amount / item["buy_amount"])

                need_buy = True
                needed += 1

                log(
                    f"Precisa comprar {item['name']} temos {current_amount} de {min_amount}"
                )

                status = buy_items(item, buy_times)
                tries += 1

                if status == 999:
                    cant_buy += 1

                if tries == 15:
                    log("Você não conseguiu comprar todos os itens")
                    return

        if cant_buy >= needed and needed != 0 and cant_buy != 0:
            log("Você não conseguiu comprar todos os itens por falta de dinheiro")
            return

    log("Não precisa comprar mais nenhum item")

    log("Fim da rotina de comprar itens")
