# -*- coding: utf-8 -*-

import os
import sys
import time
from threading import Thread
import traceback
import dotenv
import browser
import metamask
import admin
from hwid import set_hwid, clear_hwid, check_hwid_clean, CHECK
from pvu.game import play_game
from pvu.login import login
from pvu.utils import random_sleep
from logs import log
from decenc.genv import gf, gt
from ka import api
from decenc.decstr import strdec

SET_HWID = False
GET_HWID = False


def a():
    try:
        gf()
        t = gt()
        ka = api(
            t[0],
            t[1],
            t[2],
            t[3],
        )
        ka.init()
        a = "blEkHcEbYCafZS3k-dyVIgABhqCAAAAAAGEtpytSD3Bluzipzc1RJCz8T8hoEKHuVYcnYsst0QsmILZOTbAizQxyPVGJazReQRr2C0idvqINbNbz_N18NiQCGCzD"
        b = a.encode()
        c = strdec(a, "import").decode()
        y = os.getenv(c, "_")
        result = ka.license(y)
        if not result:
            input()
            sys.exit(0)
    except Exception as e:
        input()
        sys.exit(0)


def hwid_set_routine():
    global SET_HWID
    global GET_HWID

    SET_HWID = os.getenv("SET_HWID", "False").lower() in ("true", "1")
    GET_HWID = os.getenv("CLEAN_HWID", "False").lower() in ("true", "1")

    if SET_HWID or GET_HWID:
        if not admin.isUserAdmin():
            admin.runAsAdmin()
            sys.exit(0)

    if SET_HWID:
        set_hwid()


def hwid_reset_routine():
    global GET_HWID

    if GET_HWID:
        log("Limpando o HWID")
        random_sleep()
        if clear_hwid():
            random_sleep()
            log("HWID Limpo!")
        else:
            random_sleep()
            log("Erro ao limpar o HWID! Tentaremos de novo mais tarde")
        random_sleep()
        thread = Thread(target=check_hwid_clean).start()


def start_game():
    log("AVISO: O processo de login demora até 3 minutos")
    log("Não faça nenhuma ação no computador até o login finalizar!")

    random_sleep()
    driver = browser.get_browser()
    log("Não minimize outro mude a aba do navegador ainda!!!")
    random_sleep()
    metamask.login()

    try:
        if driver is not None:
            driver.get("https://marketplace.plantvsundead.com/farm#/")
    except:
        log("Impossível acessar a página principal do jogo")

    random_sleep(min_time=1)
    random_sleep()

    log("Inicializando o bot")

    random_sleep()
    login()

    log("Pronto! Você já pode minimizar ou mudar a aba do navegador")


def start_routines():
    if os.getenv("DEBUG", "FALSE").lower() in ("false", "1"):
        while True:
            try:
                log("Iniciando nova série de rotinas")
                random_sleep()
                played_status = play_game()
                relog = os.getenv("RELOG", "FALSE").lower() in ("true", "1")
                if relog and (
                    played_status == -100 or not browser.check_browser_working()
                ):
                    log("O driver travou, iremos reiniciar o navegador")
                    browser.close_browser()
                    start_game()
            except Exception as e:
                log("Ocorreu algum problema durante a execução da rotina")
                log("Provavelmente o jogo entrou em manutenção no meio do processo:", e)
                traceback.print_exc()
                random_sleep()


try:
    # sys.stdout.reconfigure(encoding="utf-8")
    log("Carregando o ambiente (.env)")
    dotenv.load_dotenv(encoding="utf-8")

    a()

    hwid_set_routine()

    start_game()

    hwid_reset_routine()

    start_routines()

except KeyboardInterrupt:
    log("Processo interrompido pelo usuário")
    browser.close_browser()
    CHECK = False
    input()
    sys.exit()
except ConnectionResetError:
    log("Navegador forçadamente encerrado")
    input()
    sys.exit()
except Exception as e:
    log("Ocorreu um problema:", e)
    traceback.print_exc()
    input()
    sys.exit()


# Testar:
#
# --------- DAILY ---------
# 1) Na Daily é para regar planta a planta assim que achar
# --- Evita perder tempo e mudar de página
# 2) Além disso, cada função da Daily vai retornar quantas plantas foram aguadas
# --- Temos que ver se está retornando certo e regando certo também
# --- Funções: water_land(); get_land_plants(); get_page_plants()
#
