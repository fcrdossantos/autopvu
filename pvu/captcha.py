# -*- coding: utf-8 -*-
import os
import json
import sys
from threading import Thread
import requests
from twocaptcha import TwoCaptcha
from pvu.utils import get_headers, random_sleep, get_backend_url
from logs import log
from pvu.maintenance_v2 import check_maintenance
from datetime import datetime, timedelta

ACTIVE_CAPTCHAS = []
NEED_CAPTCHA = False


def clear_captchas():
    global ACTIVE_CAPTCHAS
    ACTIVE_CAPTCHAS = []


def store_captcha():
    global ACTIVE_CAPTCHAS
    global NEED_CAPTCHA

    while len(ACTIVE_CAPTCHAS) < 3 and NEED_CAPTCHA:

        log("Armazenando Captchas")
        result = get_captcha_result()

        if result == 444:
            return 444

        if result:
            now = datetime.now()
            expire = now + timedelta(minutes=7)
            captcha = {"captcha": result, "expire": expire}
            ACTIVE_CAPTCHAS.append(captcha)
            log(f"Captcha armazenado! Temos {len(ACTIVE_CAPTCHAS)} captchas")

    if len(ACTIVE_CAPTCHAS) > 0:
        log("Terminou de armazenar todos os captchas")


def wait_min_stored_captchas():
    global ACTIVE_CAPTCHAS
    global NEED_CAPTCHA

    Thread(target=store_captcha).start()
    wait = 0

    while len(ACTIVE_CAPTCHAS) < 1 and NEED_CAPTCHA:

        log("Aguarde enquanto ao menos 1 captcha é resolvido")
        random_sleep(60 * 2, min_time=60, max_time=90)

        wait += 1
        if wait >= 7:
            log("Erro ao pegar os captchas")
            return False

    if len(ACTIVE_CAPTCHAS) >= 1:
        log("Já temos 1 captcha, podemos começar")
        return True
    else:
        log("Não conseguimos pegar nenhum captcha")
        return False


def remove_expired_captchas():
    global ACTIVE_CAPTCHAS
    log("Verificando captchas expirados")
    removed = False
    for captcha in ACTIVE_CAPTCHAS[:]:
        now = datetime.now()
        if now > captcha["expire"]:
            log("Removendo Captcha Expirado")
            ACTIVE_CAPTCHAS.remove(captcha)
            removed = True

    if removed or len(ACTIVE_CAPTCHAS) < 2:
        log("Pegando novos Captchas")
        wait_min_stored_captchas()


def get_captcha():
    global ACTIVE_CAPTCHAS
    global NEED_CAPTCHA

    if not NEED_CAPTCHA:
        return

    log("Buscando captchas disponiveis")
    remove_expired_captchas()

    wait = 0
    while len(ACTIVE_CAPTCHAS) == 0:
        log("Nenhum Capctha disponível, aguardando")
        random_sleep(60 * 2, min_time=60, max_time=90)
        wait += 1

        if wait == 3:
            log("Impossível pegar o captcha")
            return False

    log("Encontrado captcha disponivel")

    captcha = ACTIVE_CAPTCHAS.pop()

    return captcha["captcha"]


def stop_captcha_solver():
    global NEED_CAPTCHA
    NEED_CAPTCHA = False


def start_captcha_solver():
    global NEED_CAPTCHA
    global ACTIVE_CAPTCHAS

    NEED_CAPTCHA = True
    log("Iniciando solucionador de captchas")

    clear_captchas()
    waited = wait_min_stored_captchas()

    if not waited:
        raise Exception("Entrou em manutenção")


# Land
def solve_validation_captcha(captcha_results):
    global ACTIVE_CAPTCHAS
    url = f"{get_backend_url()}/captcha/validate"

    payload = {
        "challenge": captcha_results.get("challenge"),
        "seccode": captcha_results.get("seccode"),
        "validate": captcha_results.get("validate"),
    }
    headers = get_headers()

    log("Solucionando o validador de captchas")
    random_sleep()
    response = requests.request("POST", url, json=payload, headers=headers)

    if '"status":0' in response.text:
        log("Sucesso ao resolver o captcha")
        return True

    return False


def get_challenge_gt():
    global ACTIVE_CAPTCHAS
    global NEED_CAPTCHA
    log("Identificando Challenge e GT")

    url = f"{get_backend_url()}/captcha/register"

    payload = ""
    headers = get_headers()

    random_sleep()
    req = requests.request("GET", url, data=payload, headers=headers)

    response = req.content.decode("utf-8")

    if json.loads(response).get("status") == 444:
        NEED_CAPTCHA = False
        log("Entrou em manutenção, cancelando captcha")
        return 444, 444

    challenge = json.loads(response)["data"]["challenge"]
    gt = json.loads(response)["data"]["gt"]

    return challenge, gt


def upload_captcha():
    global ACTIVE_CAPTCHAS
    log("Enviando Captcha para ser resolvido")

    solver = TwoCaptcha(os.getenv("2CAPTCHA_API"))

    url = "https://marketplace.plantvsundead.com/farm#/farm/"

    challenge, gt = get_challenge_gt()

    if challenge == 444 and gt == 444:
        return 444

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
    global ACTIVE_CAPTCHAS
    for i in range(5):
        if not NEED_CAPTCHA:
            return 444
        log(f"Tentativa {i+1}/5 de solucionar o captcha")
        result = upload_captcha()
        if result is not None:
            break

        if result == 444:
            return 444

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
