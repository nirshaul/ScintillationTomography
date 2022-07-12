# Class for controlling the motor

from gpiozero import LED
from time import sleep

class Motor:
    def __init__(self):
        self.R = LED(27) # 27 - Right,
        self.L = LED(17) # 17 - Left,
        self.U = LED(15) # 15 - Up
        self.D = LED(18) # 18 - Down   
    
    def ResetAll(self):
        self.U.off()
        self.D.off()
        self.R.off()
        self.L.off()
    
    def MotorMove(self, Dir, timeMove, timeStay, nMovements):
        self.ResetAll()
        Motor = getattr(self, Dir) 
        idxMovements = 1
        while idxMovements <= nMovements :
            Motor.on()
            sleep(timeMove)
            Motor.off()
            sleep(timeStay)
            idxMovements = idxMovements + 1

#m = Motor()
#timeMove   = 1
#timeStay   = 1
#nMovements = 1
# 
# m.MotorMove("L", timeMove, timeStay, nMovements)
# m.MotorMove("R", timeMove, timeStay, nMovements)
# m.MotorMove("U", timeMove, timeStay, nMovements)
#m.MotorMove("D", timeMove, timeStay, nMovements)





    

