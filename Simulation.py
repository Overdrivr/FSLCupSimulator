import numpy as np
from CircuitLoader import load_circuit
from CarModel import Car
from UserControlProgram import CarControl
import threading

class Simulation:
    def __init__(self):
        self.x,self.y = load_circuit('circuit1.png')

        self.car = Car(128,400)
        self.distance = []
        self.distance.append(self.car.lineposition(self.x,self.y))

        self.pilot = CarControl()

        self.car.setspeed(10)

        self.steps = 10000
        self.step = 5.0/1000

        self.elapsed = 0

        self.camera_refresh_rate = 0.01
        self.last_camera_refresh = 0

        self.early_stop = False

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
            # Move simulator in time
            self.car.step(self.step)

            # Camera reading
            if self.elapsed - self.last_camera_refresh > self.camera_refresh_rate:
                self.last_camera_refresh = self.elapsed
                linepos = self.car.lineposition(self.x,self.y)

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
