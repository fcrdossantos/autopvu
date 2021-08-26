import os
from pvu.sunflowers import get_all_sunflowers, get_my_sunflowers
from pvu.tools import get_all_tools, get_my_tools


def get_items_info(all_items, my_items, _type):
    items_info = []

    for tool in items_info:
        name = tool.get("name")
        env_name = f"MIN_{name.replace(' ','_').upper()}"

        _id = tool.get("id")

        price = tool.get("price")
        usages = tool.get("usage")

        # current_amount = tool.get('usages')
        min_amount = int(os.getenv(env_name, "-1"))
        if min_amount == -1:
            print(f"|| Não encontramos um valor para {env_name} no arquivo .env")
            print(f"|| Vamos colocar o valor mínimo para {name} como sendo 0")
            min_amount = 0

        current_amount = 0
        for my_tool in my_items:
            if my_tool.get("name") == my_tool:
                current_amount = my_tool.get("usages")

        _tool = {
            "name": name,
            "id": int(_id),
            "_type": _type,
            "price": int(price),
            "usages": int(usages),
            "min_amount": int(min_amount),
            "current_amount": int(current_amount),
        }
        items_info.append(_tool)

    return items_info


def get_items():
    sunflowers = get_all_sunflowers(
        get_all_sunflowers(),
        get_my_sunflowers(),
        "sunflower",
    )

    tools = get_all_sunflowers(
        get_all_tools(),
        get_my_tools(),
        "tool",
    )

    return sunflowers + tools
