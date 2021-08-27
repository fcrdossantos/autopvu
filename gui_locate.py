import os
import pyautogui
import pydirectinput
import mss
import cv2
import numpy as np

# Regions that will be used to analyse the screen
def regions(region="full"):
    if region == "icon_mask":
        return (0, 0, 1920, 100)

    if region == "mask_open":
        return (1000, 0, 920, 900)

    if region == "button_unlock":
        return (1000, 150, 920, 750)

    if region == "full":
        return (0, 0, 1920, 1080)

    return False


pyautogui.PAUSE = 1

if os.getenv("DEBUG", "FALSE").lower() in ("true", "1"):
    if not os.path.exists("print") and not os.path.isdir("print"):
        os.makedirs("print")
    pyautogui.screenshot("print/icon.png", region=regions("icon_mask"))
    pyautogui.screenshot("print/mask.png", region=regions("mask_open"))
    pyautogui.screenshot("print/unlock.png", region=regions("button_unlock"))


def take_ss(region, name=None):
    with mss.mss() as sct:
        sct_img = sct.grab(region)

        if name is not None:
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=name)
        return sct_img


def locate(image, region=regions(), grayscale=False, confidence=0.8):
    image_path = f"images/{image}"

    with mss.mss() as sct:

        ss = np.array(sct.grab(region))
        ss = ss[:, :, :3]

        needle = cv2.imread(image_path)

        if grayscale:
            ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
            needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)

        needle_h, needle_w = needle.shape[:2]
        # print(needle_h, needle_w)

        result = cv2.matchTemplate(ss, needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # print(min_val, max_val, min_loc, max_loc)

        if max_val > confidence:
            # print("max > confidence", max_val, confidence, max_val > con)
            position_x = max_loc[0] + needle_w // 2
            position_y = max_loc[1] + needle_h // 2
            return position_x, position_y

        return False


# Locate the image but also perform a click
def locate_click(image, region=regions(), grayscale=False, confidence=0.75):
    pos = locate(image, region, grayscale, confidence)

    if pos is not None and pos is not False:
        pos_x = pos[0]
        pos_y = pos[1]

        pydirectinput.moveTo(pos_x, pos_y)
        pydirectinput.click(pos_x, pos_y)
        print(f"|| Clicando na posição: ({pos_x},{pos_y})")

        return True

    return False
