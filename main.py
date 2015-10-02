import numpy as np
import matplotlib.pyplot as plt
from CircuitLoader import load_circuit
from CarModel import Car
from UserControlProgram import CarControl
from TimingUtils import timeit

x,y = load_circuit('circuit1.png')

car = Car(128,400)
distance = []
distance.append(car.lineposition(x,y))

pilot = CarControl()

car.setspeed(10)

steps = 1000
step = 1.0/1000

elapsed = 0

camera_refresh_rate = 0.05
last_camera_refresh = 0

for i in range(steps):
    percent = (i * 100.0) / steps
    if percent > 0:
        if percent % 10 == 0:
            print("Simulated "+str(percent)+" %")
    # Move simulator in time
    car.step(step)

    # Camera reading
    if elapsed - last_camera_refresh > camera_refresh_rate:
        last_camera_refresh = elapsed
        linepos = car.lineposition(x,y)

        # Ask user program new values for direction and speed
        direction,speed = pilot.mainloop(linepos)

        # Update car settings according to user values
        car.setspeed(speed)
        #car.setdirection(direction)
        car.setdirection(percent)

        # Register data for plotting
        distance.append(linepos)

    elapsed += step

#Plot des donnes
textsize = 18
figure1 = plt.figure(figsize=(6,6),dpi=90)
figure1.set_tight_layout(True)

ax1 = figure1.add_subplot(111)
ax1.set_xlabel('X',fontsize=textsize)
ax1.set_ylabel('Y',fontsize=textsize)
ax1.tick_params(axis='both', which='major', labelsize=textsize)
ax1.plot(x,y,'r-',linewidth=1.0,label='track')
ax1.plot(car.x,car.y,'b-*',linewidth=1.0,label='car')
ax1.plot(car.camrightx,car.camrighty,'g-+',linewidth=1.0,label='car')
ax1.plot(car.camleftx,car.camlefty,'g-+',linewidth=1.0,label='car')
ax1.relim()


figure2 = plt.figure(figsize=(6,6),dpi=90)
figure2.set_tight_layout(True)

ax2 = figure2.add_subplot(111)
ax2.set_xlabel('X',fontsize=textsize)
ax2.set_ylabel('Y',fontsize=textsize)
ax2.tick_params(axis='both', which='major', labelsize=textsize)
ax2.plot(range(len(distance)),distance,'r-',linewidth=1.0,label='distance to line')
ax2.relim()

plt.autoscale(enable=True,tight=False)
plt.show()
