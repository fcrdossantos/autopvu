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


def get_tools():
    all_tools = get_all_tools()
    my_tools = get_my_tools()

    tools_info = []

    for tool in all_tools:
        name = tool.get("name")
        env_name = f"MIN_{name.replace(' ','_').upper()}"

        _id = tool.get("id")
        _type = "tool"

        price = tool.get("price")
        usages = tool.get("usage")

        # current_amount = tool.get('usages')
        min_amount = int(os.getenv(env_name, "-1"))
        if min_amount == -1:
            print(f"|| Não encontramos um valor para {env_name} no arquivo .env")
            print(f"|| Vamos colocar o valor mínimo para {name} como sendo 0")
            min_amount = 0

        current_amount = 0
        for my_tool in my_tools:
            if my_tool.get("name") == my_tool:
                current_amount = my_tool.get("usages")

        _tool = {
            "name": name,
            "id": _id,
            "_type": _type,
            "price": price,
            "usages": usages,
            "min_amount": min_amount,
            "current_amount": current_amount,
        }
        tools_info.append(_tool)

    return tools_info
