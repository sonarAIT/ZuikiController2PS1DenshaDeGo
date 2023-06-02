import pygame

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

def main():
    controllerInputGetter = ZuikiControllerInputGetter()
    while True:
        print(controllerInputGetter.getNotch())
        pygame.time.wait(10)

if __name__ == "__main__":
    main()