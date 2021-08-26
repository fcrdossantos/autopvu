import time
import os
from datetime import datetime, timedelta
from browser import get_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pvu.utils import random_sleep


def get_next_group_time():
    random_sleep()
    now = datetime.now()
    current_minute = now.minute

    next_minute = int(os.getenv("GROUP_RESET_MINUTE"))

    next_group = now.replace(
        microsecond=0,
        second=0,
        minute=next_minute,
        hour=now.hour,
        day=now.day,
        month=now.month,
        year=now.year,
    )

    if current_minute >= next_minute:
        next_group = next_group + timedelta(hours=1)

    random_sleep()
    return next_group


def can_login_maintenance(next_group_date):
    random_sleep()
    if datetime.now() > next_group_date:
        return True
    else:
        return False


def check_maintenance():
    try:
        driver = get_browser()

        game_url = "https://marketplace.plantvsundead.com/farm#/farm"

        random_sleep(min_time=1)

        random_sleep(3)

        if driver is not None:
            while driver.current_url != game_url:
                driver.get(game_url)
                random_sleep(min_time=1)

        maintenance = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[2]/div/p")
            )
        )

        maintenance = maintenance.text

        random_sleep()
        if maintenance == "Farm Maintenance":
            print("|| Em Manutenção! Tente novamente mais tarde")
            return True

        return False
    except:
        random_sleep(3)
        print("|| Jogo liberado! Pode jogar")
        return False
