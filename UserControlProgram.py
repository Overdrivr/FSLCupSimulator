import numpy as np

class CarControl:
    def __init__(self):
        self.P = 0.03
    def mainloop(self,lineposition):
        #TODO : Fix it
        if lineposition == np.NaN:
            print("ISSUE")
            return 0,100

        error = -lineposition

        direction = error * self.P
        speed = 100
        return direction,speed
