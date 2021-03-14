from time import sleep
import pyautogui


def clear_screen(t):
    sleep(t)
    pyautogui.hotkey('ctrl', 'l')
    sleep(1)


