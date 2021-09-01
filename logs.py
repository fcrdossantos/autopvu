from datetime import datetime


def log(*args):
    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    print(f"|| [{now}]", *args)
