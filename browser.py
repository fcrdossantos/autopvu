# -*- coding: utf-8 -*-
import os
import psutil
import subprocess

from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from logs import log
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions


BROWSER = None


def open_browser():

    close_browser()
    close_all_chrome()

    log("Abrindo Navegador")
    options = ChromeOptions()

    if os.getenv("USER", "1") == "1":
        DATA_DIR = os.getenv("DATA_DIR_1")
        DRIVER = os.getenv("DRIVER_DIR_1")
    else:
        DATA_DIR = os.getenv("DATA_DIR_2")
        DRIVER = os.getenv("DRIVER_DIR_2")
        options.binary_location = os.getenv("PATH_BROWSER_2", "chromium/chrome.exe")

    PROFILE = os.getenv("PROFILE_NAME", "Default")

    if DATA_DIR is None:
        log("Não foi encontrado um caminho para o Chrome")
        current_user = os.getlogin()
        log(f"Usando o padrão para o usuário {current_user}")
        DATA_DIR = (
            "C:\\Users\\"
            + {current_user}
            + "\\AppData\\Local\\Google\\Chrome\\User Data\\"
        )
        log("Caminho:", DATA_DIR)

    options.user_data_dir = DATA_DIR
    options.add_argument(f"--profile-directory={PROFILE}")
    options.add_argument("--ignore-ssl-errors")

    service = Service(DRIVER)

    browser = Chrome(options=options)

    browser.maximize_window()
    browser.get("https://google.com.br")
    return browser


def get_browser(new=False):
    global BROWSER

    if BROWSER is None or new == True:
        BROWSER = open_browser()

    return BROWSER


def close_browser():
    global BROWSER

    if BROWSER is not None:
        log("Fechando Navegador")
        BROWSER.get("https://google.com.br")

        BROWSER.close()
        BROWSER = None


def close_all_chrome():
    for process in psutil.process_iter():
        if process.name() == "chrome.exe" or process.name() == "chromedriver.exe":
            process.kill()
