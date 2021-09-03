# -*- coding: utf-8 -*-

import sys
import os
from datetime import datetime


def log(*args):
    args_unicode = []

    for arg in args:
        if type(arg) == str:
            args_unicode.append(arg.encode().decode("utf-8", "ignore"))
        else:
            args_unicode.append(arg)

    if os.getenv("DEBUG", "FALSE").lower() in ("false", "1"):
        sys.stdout.reconfigure(encoding="utf-8")

    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    print(f"|| [{now}]", *args_unicode)
