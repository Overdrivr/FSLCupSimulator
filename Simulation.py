import numpy as np
from CircuitLoader import load_circuit
from CarModel import Car
from CameraModel import Camera
from UserControlProgram import CarControl
import threading

class Simulation:
    def __init__(self,threadlock):
        self.x,self.y,self.img = load_circuit('circuit1.png')

        self.car = Car(128,400)

        self.camera = Camera()
        self.line = []

        self.distance = []
        self.distance.append(self.car.lineposition(self.x,self.y))

        self.pilot = CarControl()

        self.car.setspeed(10)

        self.steps = 30000
        self.step = 1.0/1000

        self.elapsed = 0

        self.camera_refresh_rate = 0.01
        self.last_camera_refresh = 0

        self.early_stop = False

        self.threadlock = threadlock

        self.t = threading.Thread(target=self.simulate)
        self.t.start()

    def simulate(self):
        for i in range(self.steps):
            # Cancel simulation on early stop
            if self.early_stop:
                break

            percent = (i * 100.0) / self.steps
            if percent > 0:
                if percent % 10 == 0:
                    print("Simulated "+str(percent)+" %")

            self.threadlock.acquire()
            # Move simulator in time
            self.car.step(self.step)
            self.threadlock.release()

            # Camera reading
            if self.elapsed - self.last_camera_refresh > self.camera_refresh_rate:
                self.line = self.camera.get_line((self.car.camleftx[-1],self.car.camlefty[-1]),(self.car.camrightx[-1],self.car.camrighty[-1]),self.img)
                self.last_camera_refresh = self.elapsed
                self.threadlock.acquire()
                linepos = self.car.lineposition(self.x,self.y)
                self.threadlock.release()

                if linepos is np.NaN:
                    print("Line lost.")
                    self.early_stop = True

                # Ask user program new values for direction and speed
                direction,speed = self.pilot.mainloop(linepos)

                # Update car settings according to user values
                self.car.setspeed(speed)
                self.car.setdirection(direction)
                #car.setdirection(percent)

                # Register data for plotting
                self.distance.append(linepos)

            self.elapsed += self.step
        print("Simulation complete.")

    def stop(self):
        self.early_stop = True
