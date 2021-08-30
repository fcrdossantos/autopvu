from datetime import datetime


def log(*args):
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    log(f" [{now}]", *args)
