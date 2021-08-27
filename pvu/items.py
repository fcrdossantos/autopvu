import os
from pvu.sunflowers import get_all_sunflowers, get_my_sunflowers
from pvu.tools import get_all_tools, get_my_tools


def get_items_info(all_items, my_items, _type):
    items_info = []

    for item in all_items:
        name = item.get("name")
        env_name = f"MIN_{name.replace(' ','_').upper()}"

        _id = item.get("id")

        if not _id:
            print(item)

        price = item.get("price")
        usages = item.get("usages")

        if not usages:
            usages = 1

        # current_amount = tool.get('usages')
        min_amount = int(os.getenv(env_name, "-1"))
        if min_amount == -1:
            print(f"|| Não encontramos um valor para {env_name} no arquivo .env")
            print(f"|| Vamos colocar o valor mínimo para {name} como sendo 0")
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

    return tools + sunflowers
