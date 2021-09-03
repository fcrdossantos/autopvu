import os
from pvu.sunflowers import get_all_sunflowers, get_my_sunflowers
from pvu.tools import get_all_tools, get_my_tools
from logs import log


def get_items_info(all_items, my_items, _type):
    items_info = []

    for item in all_items:
        name = item.get("name")

        priority = 8

        priority_list = {
            "Scarecrow": 1,
            "Water": 2,
            "Small Pot": 3,
            "Big Pot": 4,
            "Sunflower Sapling": 5,
            "Sunflower mama": 6,
            "Greenhouse": 7,
        }

        if priority_list.get(name) is not None:
            priority = priority_list.get(name)

        env_name = f"MIN_{name.replace(' ','_').upper()}"

        _id = item.get("id")

        if not _id:
            log("Item sem ID:", item)

        price = item.get("price")
        usages = item.get("usages")

        if not usages:
            usages = 1

        # current_amount = tool.get('usages')
        min_amount = int(os.getenv(env_name, "-1"))
        if min_amount == -1:
            log(f"Não encontramos um valor para {env_name} no arquivo .env")
            log(f"Vamos colocar o valor mínimo para {name} como sendo 0")
            min_amount = 0

        current_amount = 0
        for my_item in my_items:
            if my_item.get("name") == name:
                current_amount = my_item.get("usages")

        _item = {
            "name": name,
            "id": int(_id),
            "type": _type,
            "price": int(price),
            "buy_amount": int(usages),
            "min_amount": int(min_amount),
            "current_amount": int(current_amount),
            "priority": int(priority),
        }
        items_info.append(_item)

    return items_info


def get_items():
    tools = get_items_info(
        get_all_tools(),
        get_my_tools(),
        "tool",
    )

    sunflowers = get_items_info(
        get_all_sunflowers(),
        get_my_sunflowers(),
        "sunflower",
    )

    items = tools + sunflowers

    items = sorted(items, key=lambda k: k["priority"])

    return items
