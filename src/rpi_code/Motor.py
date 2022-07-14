#===================================================================================================#
# You are very welcome to use this code. For this, clearly acknowledge                              #
# the source of this code, and cite the paper that describes the algorithm:                         #
# N. Shaul and Y. Y. Schechner, "Tomography of Turbulence Strength Based on Scintillation Imaging", #
# Proc. of European Conference on Computer Vision (ECCV), 2022.                                     #
#                                                                                                   #
# (c) Copyright Nir Shaul 2022. The python code is available for                                    #
# non-commercial use and exploration.  For commercial use contact the                               #
# author. The author is not liable for any damages or loss that might be                            #
# caused by use or connection to this code.                                                         #
#                                                                                                   #
# Class for controlling the motor. It is part of other methods for capturing images using RPI-IDS.  #
#===================================================================================================#


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





    

