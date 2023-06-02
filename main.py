import time
import pygame
import pyautogui

class ZuikiControllerInputGetter:
    def __init__(self):
        # const
        self.JOYSTICK_NAME = "One Handle MasCon for Nintendo Switch"
        self.AXIS2NOTCH = {
            9: "P5",
            8: "P4",
            6: "P3",
            4: "P2",
            2: "P1",
            0: "N",
            -2: "B1",
            -3: "B2",
            -4: "B3",
            -5: "B4",
            -6: "B5",
            -7: "B6",
            -8: "B7",
            -9: "B8",
            -10: "EB"
        }

        # init
        pygame.joystick.init()
        pygame.init()

        # get joystick id
        joystickID = -1
        for i in range(pygame.joystick.get_count()):
            if pygame.joystick.Joystick(i).get_name() == self.JOYSTICK_NAME:
                joystickID = i
                break

        # if joystick is not found
        if joystickID == -1:
            print(f"{self.JOYSTICK_NAME}が接続されていません。")
            exit()

        # get joystick
        self.joystick = pygame.joystick.Joystick(joystickID)
        self.joystick.init()

    def getNotch(self):
        pygame.event.pump()
        axis = int(self.joystick.get_axis(1) * 10)
        notch = self.AXIS2NOTCH[axis]
        return notch

    def getButtons(self):
        buttons = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        return buttons

class Zuiki2PS1Dengo:
    def __init__(self):
        self.NOTCH2BITS = {
            "P5": 0b01011011,
            "P4": 0b11001011,
            "P3": 0b11011011,
            "P2": 0b01101011,
            "P1": 0b01111011,
            "N": 0b11101011,
            "B1": 0b11101110,
            "B2": 0b11101010,
            "B3": 0b11100111,
            "B4": 0b11100011,
            "B5": 0b11100110,
            "B6": 0b11100010,
            "B7": 0b11101101,
            "B8": 0b11101001,
            "EB": 0b11100000,
        }
        self.BIT2KEY = {
            0: "2",
            1: "0",
            2: "1",
            3: "9",
            4: "i",
            5: "d",
            6: "s",
            7: "a",
        }
        self.BUTTON2KEY = {
            0: "l",
            1: "k",
            3: "j",
            4: "b",
            6: "n",
        }

    def getKeys(self, notch, buttons):
        bits = self.NOTCH2BITS[notch]
        downKeys = ["w"]
        upKeys = []
        for i in range(8):
            if bits & (1 << i):
                downKeys.append(self.BIT2KEY[i])
            else:
                upKeys.append(self.BIT2KEY[i])
        for button, key in self.BUTTON2KEY.items():
            if buttons[button]:
                downKeys.append(key)
            else:
                upKeys.append(key)
        return downKeys, upKeys

class PS1DengoKeyPresser:
    def __init__(self):
        self.WAIT_TIME = 0.05
        self.prevDownKeys = []
        self.prevUpKeys = []
        self.isWaiting = False
        self.waitStartTime = 0
        pyautogui.PAUSE = 0

    def input(self, downKeys, upKeys):
        if self.isWaiting:
            if self.waitStartTime + self.WAIT_TIME < time.time():
                self.isWaiting = False
                self.press(downKeys, upKeys)

        if self.prevDownKeys != downKeys or self.prevUpKeys != upKeys:
            self.isWaiting = True
            self.waitStartTime = time.time()
            self.prevDownKeys = downKeys
            self.prevUpKeys = upKeys

    def press(self, downKeys, upKeys):
        for key in downKeys:
            pyautogui.keyDown(key)
        for key in upKeys:
            pyautogui.keyUp(key)

def main():
    controllerInputGetter = ZuikiControllerInputGetter()
    zuiki2PS1Dengo = Zuiki2PS1Dengo()
    ps1DengoKeyPresser = PS1DengoKeyPresser()

    while True:
        notch = controllerInputGetter.getNotch()
        buttons = controllerInputGetter.getButtons()
        downKeys, upKeys = zuiki2PS1Dengo.getKeys(notch, buttons)
        ps1DengoKeyPresser.input(downKeys, upKeys)

if __name__ == "__main__":
    main()
