import os
import sys
import time
from threading import Thread
import dotenv
import browser
import metamask
import admin
from hwid import set_hwid, clear_hwid, check_hwid_clean, CHECK
from pvu.game import play_game
from pvu.login import login
from pvu.utils import random_sleep


try:
    if not admin.isUserAdmin():
        admin.runAsAdmin()
        sys.exit(0)

    print("|| Carregando o ambiente (.env)")
    dotenv.load_dotenv()

    if os.getenv("SET_HWID", "False").lower() in ("true", "1"):
        set_hwid()

    random_sleep()
    driver = browser.get_browser()
    print("|| Não minimize outro mude a aba do navegador ainda!!!")

    random_sleep()
    metamask.login()

    try:
        if driver is not None:
            driver.get("https://marketplace.plantvsundead.com/farm#/")
    except:
        print("|| Impossível acessar a página principal do jogo")

    random_sleep(min_time=1)
    random_sleep()

    print("|| Inicializando o bot")

    random_sleep()
    login()

    print("|| Pronto! Você já pode minimizar ou mudar a aba do navegador")

    if os.getenv("CLEAN_HWID", "False").lower() in ("true", "1"):
        print("|| Limpando o HWID")
        random_sleep()
        if clear_hwid():
            random_sleep()
            print("|| HWID Limpo!")
        else:
            random_sleep()
            print("|| Erro ao limpar o HWID! Tentaremos de novo mais tarde")
        random_sleep()
        thread = Thread(target=check_hwid_clean).start()

    if os.getenv("DEBUG", "FALSE").lower() in ("false", "1"):
        while True:
            try:
                random_sleep()
                play_game()
            except Exception as e:
                print("|| Ocorreu algum problema durante a execução da rotina")
                print(
                    "|| Provavelmente o jogo entrou em manutenção no meio do processo"
                )
                print(e)
                random_sleep()

except KeyboardInterrupt:
    print("|| Processo interrompido pelo usuário")
    browser.close_browser()
    CHECK = False
    sys.exit()
except ConnectionResetError:
    print("|| Navegador forçadamente encerrado")
except Exception as e:
    print("|| Ocorreu um problema")
    print(e)


# Testar:
#
# --------- DAILY ---------
# 1) Na Daily é para regar planta a planta assim que achar
# --- Evita perder tempo e mudar de página
# 2) Além disso, cada função da Daily vai retornar quantas plantas foram aguadas
# --- Temos que ver se está retornando certo e regando certo também
# --- Funções: water_land(); get_land_plants(); get_page_plants()
#
# --------- FARM  ---------
# 1) Pegamos as terras disponíveis na fazenda
# --- Função: get_farm_lands()
# 2) Pegamos a quantidade máxima suportada na terra
# --- Isso vai falar que a terra 0 cabe 5 plantas e 1 mãe
# --- Função: get_available_spaces()


# 1) Adicionar verbose nos sleeps

# 4) Comprar item na loja

# 5) Pegar valor de compra minimo para SUN BOX
# 6) Verificar se quer comprar a SUN BOX
# 7) Se sim, gasta LE até chegar no minimo


# 10) Modo Turbo: Armazenar 10 Captchas (thread) e ir pegando de lá sempre que precisar
# 11) Api do Discord: O bot vai virar uma webapi e printar quais lugares regar
# PS: Precisamos pegar um token vitalício (ou quase isso) -> Login Selenium :) P


# farm status 444 => manutenção (not in the list)
