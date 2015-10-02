import numpy as np
from CircuitLoader import load_circuit
from CarModel import Car
from UserControlProgram import CarControl
from TimingUtils import timeit

import Tkinter as Tk

import matplotlib, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

x,y = load_circuit('circuit1.png')

car = Car(128,400)
distance = []
distance.append(car.lineposition(x,y))

pilot = CarControl()

car.setspeed(10)

steps = 10000
step = 1.0/1000

elapsed = 0

camera_refresh_rate = 0.01
last_camera_refresh = 0

#Plot des donnes
textsize = 18
figure1 = Figure(figsize=(6,6),dpi=90)
figure1.set_tight_layout(True)

ax1 = figure1.add_subplot(111)
ax1.set_xlabel('X',fontsize=textsize)
ax1.set_ylabel('Y',fontsize=textsize)
ax1.tick_params(axis='both', which='major', labelsize=textsize)

#x,y
line_car_position, = ax1.plot([],[],'r-',linewidth=1.0,label='track')
#car.x,car.y
line_line_position = ax1.plot([],[],'b-*',linewidth=1.0,label='line position')
# car.camrightx,car.camrighty
line_cam_right_position = ax1.plot([],[],'g-+',linewidth=1.0,label='camera right position')
# car.camleftx,car.camlefty
line_cam_left_position = ax1.plot([],[],'g-+',linewidth=1.0,label='camera left position')

root = Tk.Tk()
dataPlot = FigureCanvasTkAgg(figure1,master=root)
dataPlot.show()
dataPlot.get_tk_widget().grid(column=0,row=0,sticky='WENS',columnspan=5)
root.mainloop()

"""
figure2 = plt.figure(figsize=(6,6),dpi=90)
figure2.set_tight_layout(True)

ax2 = figure2.add_subplot(111)
ax2.set_xlabel('X',fontsize=textsize)
ax2.set_ylabel('Y',fontsize=textsize)
ax2.tick_params(axis='both', which='major', labelsize=textsize)
ax2.plot(range(len(distance)),distance,'r-',linewidth=1.0,label='distance to line')
ax2.relim()
"""
#plt.autoscale(enable=True,tight=False)
#plt.show()

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
        car.setdirection(direction)
        #car.setdirection(percent)

        # Register data for plotting
        distance.append(linepos)

    elapsed += step
