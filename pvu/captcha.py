import os
import json
import requests
from twocaptcha import TwoCaptcha
from pvu.utils import get_headers, random_sleep
from logs import log


def get_challenge_gt():
    log("Identificando Challenge e GT")

    url = "https://backend-farm.plantvsundead.com/captcha/register"

    payload = ""
    headers = get_headers()

    random_sleep()
    req = requests.request("GET", url, data=payload, headers=headers)

    response = req.content.decode("utf-8")

    challenge = json.loads(response)["data"]["challenge"]
    gt = json.loads(response)["data"]["gt"]

    return challenge, gt


def upload_captcha():
    log("Enviando Captcha para ser resolvido")

    solver = TwoCaptcha(os.getenv("2CAPTCHA_API"))
    url = "https://marketplace.plantvsundead.com/farm#/farm/"

    challenge, gt = get_challenge_gt()

    try:
        log("Tentando solucionar o captcha")
        result = solver.geetest(gt=gt, challenge=challenge, url=url)

    except Exception as e:
        log("Erro ao solucionar o captcha:", e)
        result = None

    else:
        log("Sucesso ao solucionar o captcha!")

    return result


def get_captcha_result():
    for i in range(5):
        log(f" Tentativa {i+1}/5 de solucionar o captcha")
        result = upload_captcha()
        if result is not None:
            break

    if not result:
        return False
    else:
        return_code = json.loads(result["code"])
        result_challenge = return_code.get("geetest_challenge")
        result_validate = return_code.get("geetest_validate")
        result_seccode = return_code.get("geetest_seccode")

        log("Enviando resultado do captcha")
        return {
            "challenge": result_challenge,
            "validate": result_validate,
            "seccode": result_seccode,
        }
