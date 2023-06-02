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

class PS1DengoKeyPresser:
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

    def press(self, notch):
        pyautogui.keyDown("w") # wは押しっぱなし
        bits = self.NOTCH2BITS[notch]
        for i in range(8):
            if bits & (1 << i):
                pyautogui.keyDown(self.BIT2KEY[i])
            else:
                pyautogui.keyUp(self.BIT2KEY[i])

def main():
    controllerInputGetter = ZuikiControllerInputGetter()
    keyPresser = PS1DengoKeyPresser()
    while True:
        # print(controllerInputGetter.getNotch())
        # pygame.time.wait(10)
        keyPresser.press()


if __name__ == "__main__":
    main()