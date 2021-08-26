import os
import pyautogui
import pydirectinput

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


# Just locate an image in your region
def locate(image, region=regions(), grayscale=False, confidence=0.75):
    image_path = f"images/{image}"

    return pyautogui.locateOnScreen(
        image_path,
        confidence=confidence,
        region=region,
        grayscale=grayscale,
    )


# Locate the image but also perform a click
def locate_click(image, region=regions(), grayscale=False, confidence=0.75):
    btn = locate(image, region, grayscale, confidence)

    if btn is not None:
        btn_pos = pyautogui.center(btn)

        pydirectinput.moveTo(btn_pos.x, btn_pos.y)
        pydirectinput.click(btn_pos.x, btn_pos.y)
        print(f"|| Clicando na posição: ({btn_pos.x},{btn_pos.y})")

        return True

    return False
