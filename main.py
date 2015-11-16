from TimingUtils import timeit
import Tkinter as Tk
import matplotlib, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Simulation
import threading

lock = threading.Lock()
simu = Simulation.Simulation(lock)

#Plot des donnes
textsize = 18
figure1 = Figure(figsize=(10,10),dpi=90)
figure1.set_tight_layout(True)

ax1 = figure1.add_subplot(211)
ax1.set_xlabel('X',fontsize=textsize)
ax1.set_ylabel('Y',fontsize=textsize)
ax1.tick_params(axis='both', which='major', labelsize=textsize)
ax1.set_xlim([0, 1000])
ax1.set_ylim([0, 1000])
#ax1.set_autoscale_on(True)
#x,y
line_track, = ax1.plot([],[],'r-',linewidth=1.0,label='track')
line_track.set_data(simu.x,simu.y)
#car.x,car.y
line_car_position, = ax1.plot([],[],'b-',linewidth=1.0,label='car position')
# car.camrightx,car.camrighty
line_cam_right_position, = ax1.plot([],[],'g-+',linewidth=1.0,label='camera right position')
# car.camleftx,car.camlefty
line_cam_left_position, = ax1.plot([],[],'g-+',linewidth=1.0,label='camera left position')


ax2 = figure1.add_subplot(212)
ax2.set_ylim([-10, 260])
#ax2.tick_params(axis='both', which='major', labelsize=textsize)
line_line, = ax2.plot([],[],'b-',linewidth=1.0,label='line')
#ax2.set_xlim([0, 1000])
#ax2.set_ylim([-50, 50])

#ax1.set_autoscale_on(True)
#x,y
#line_direction, = ax2.plot([],[],'r-',linewidth=1.0,label='direction')

root = Tk.Tk()
dataPlot = FigureCanvasTkAgg(figure1,master=root)
#NavigationToolbar2TkAgg(dataPlot, root)
dataPlot.show()
dataPlot.get_tk_widget().grid(column=0,row=0,sticky='WENS',columnspan=5)

refreshrate = 100
def refresh():

    lock.acquire()
    line_car_position.set_data(simu.car.x,simu.car.y)
    line_cam_right_position.set_data(simu.car.camrightx,simu.car.camrighty)
    line_cam_left_position.set_data(simu.car.camleftx,simu.car.camlefty)
    line_line.set_data(range(len(simu.line)),simu.line)
    ax2.set_xlim([0, len(simu.line)])
    lock.release()

    #line_direction.set_data
    #ax1.relim()
    #ax1.autoscale_view(False,False,True)
    try:
        dataPlot.draw()
    except:
        print("X : ",len(simu.car.x))
        print("Y : ",len(simu.car.y))

    root.after(refreshrate,refresh)

def onExit():
    simu.stop()
    root.destroy()

# Stop simulation on exit
root.wm_protocol ("WM_DELETE_WINDOW", onExit)
# Start refresh cyclic event
root.after(refreshrate,refresh)
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
