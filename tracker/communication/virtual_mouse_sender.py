import pyautogui

class VirtualMouseSender:
    def __init__(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0

    def move(self, dx: int, dy: int):
        pyautogui.moveRel(dx, dy, duration=0)

    def left_click(self):
        pyautogui.click(button="left")

    def right_click(self):
        pyautogui.click(button="right")

    def middle_click(self):
        pyautogui.click(button="middle")

    def left_press(self):
        pyautogui.mouseDown(button="left")

    def left_release(self):
        pyautogui.mouseUp(button="left")

    def right_press(self):
        pyautogui.mouseDown(button="right")

    def right_release(self):
        pyautogui.mouseUp(button="right")

    def scroll(self, amount: int):
        pyautogui.scroll(amount)

    def close(self):
        pass
