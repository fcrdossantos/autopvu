import math
import requests
import os
from pvu.utils import get_headers, random_sleep
from pvu.items import get_items
from browser import get_browser
from pvu.user import get_le
from logs import log


def buy_item(item, buy_times):
    item_id = item["id"]

    total_price = item["price"] * buy_times
    total_le = get_le()

    if total_le < total_price:
        buy_times = total_le // item["price"]

    if buy_times == 0:
        log("Você não tem dinheiro pra comprar tudo o que precisa")
        return False

    times_text = "vez" if buy_times == 1 else "vezes"

    log(f" Vou comprar {item['name']} {buy_times} {times_text}")

    if item["type"] == "tool":
        url = "https://backend-farm.plantvsundead.com/buy-tools"
        payload = {"amount": buy_times, "toolId": item_id}
    else:
        url = "https://backend-farm.plantvsundead.com/buy-sunflowers"
        payload = {"amount": buy_times, "sunflowerId": item_id}

    log(f" Sucesso ao comprar {item['name']}")

    headers = get_headers()

    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    # log("Resultado da loja:", response.text)

    if '"status":0' in response.text:
        log("Sucesso ao comprar o item:", item["name"])
    elif '"status":9' in response.text:
        log("Você não tem dinheiro para comprar o item:", item["name"])
    else:
        log("Erro ao comprar o item:", item["name"])
        log("=> Resposta:", response.text)
        log("Tentarei novamente mais tarde!")
        return False

    return True


def buy_items():
    log("Iniciando a rotina de comprar itens")

    log("Pegando seus itens atuais e necessidades de compra")
    items = get_items()

    if os.getenv("HUMANIZE", "TRUE").lower() in ("true", "1"):
        try:
            driver = get_browser()
            store_url = "https://marketplace.plantvsundead.com/farm#/farm/shop/"

            if driver is not None:
                driver.get(store_url)
                random_sleep()
        except:
            log("Erro ao redirecionar para a página da loja")

    log("Verificando se é necessário comprar algum item")
    for item in items:
        current_amount = item["current_amount"]
        min_amount = item["min_amount"]

        if current_amount < min_amount:
            buy_amount = min_amount - current_amount
            buy_times = math.ceil(buy_amount / item["buy_amount"])

            log(
                f"Precisa comprar {item['name']} temos {current_amount} de {min_amount}"
            )

            buy_item(item, buy_times)

    log("Não precisa comprar mais nenhum item")

    log("Fim da rotina de comprar itens")
