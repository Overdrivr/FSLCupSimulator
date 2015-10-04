import math
import numpy as np
from mathutils import seg_intersect
from TimingUtils import timeit

class Car:
    def __init__(self,startx,starty):
        self.orientation = 90
        self.orientationvector = [0,0]
        self.x = []
        self.y = []
        self.x.append(startx)
        self.y.append(starty)
        self.camerawidth = 30
        self.sqrdcamwidth = self.camerawidth * self.camerawidth
        self.camleftx = []
        self.camlefty = []
        self.camrightx = []
        self.camrighty = []
        self._compute_camera_limits()
        self.speed = 0
        self.delta = 0
        self.direction_max_rotation_speed = 10000 # 200 degrees per second
        self.direction_target = 0
        self.direction_min = -45
        self.direction_max = 45
        self._compute_applied_direction(0.01)

    # Move the car forward
    def step(self,step):
        # Update direction vector
        self._compute_applied_direction(step)
        # Update car position
        dx = self.speed * step * self.orientationvector[0]
        dy = self.speed * step * self.orientationvector[1]

        self.x.append(self.x[-1] + dx)
        self.y.append(self.y[-1] + dy)
        self.delta += step

    # Rotates car direction by delta amount
    def setdirection(self,direction):
        self.direction_target = direction
        if direction > self.direction_max:
            self.direction_target = self.direction_max
        if direction < self.direction_min:
            self.direction_target = self.direction_min

    def setspeed(self,speed):
        self.speed = speed

    # Simulates camera position reading
    def lineposition(self,trackx,tracky):
        # Update camera field of view
        self._compute_camera_limits()

        #camera_right_limit = np.array((self.camrightx[-1],self.camrighty[-1]))
        #camera_left_limit = np.array((self.camleftx[-1],self.camlefty[-1]))

        carpos = np.array((self.x[-1],self.y[-1]))
        # Search intersection between camera and line
        for i in range(len(trackx)-1):
            pointA = np.array((trackx[i],  tracky[i]))
            pointB = np.array((trackx[i+1],tracky[i+1]))

            va = carpos-pointA
            vb = carpos-pointB

            da = va[0]*va[0] + va[1]*va[1]
            db = vb[0]*vb[0] + vb[1]*vb[1]

            # if distance to car > to camerawidth for both points, discard
            if da > self.sqrdcamwidth and db > self.sqrdcamwidth :
                continue

            a = seg_intersect(self.cam_right_limit,self.cam_left_limit,pointA,pointB)
            if a is not None:
                d = np.linalg.norm(carpos-a)
                d1 = np.linalg.norm(self.cam_right_limit-a)
                d2 =  np.linalg.norm(self.cam_left_limit-a)
                if d2>d1:
                    d *= -1

                # Todo : fix it
                if abs(d) > self.camerawidth:
                    return 0
                return d

        # Search in last segment

        # Nothing found
        return np.NaN

    def _compute_camera_limits(self):
        # Calculate orthogonal vector
        dx = - self.camerawidth * self.orientationvector[1]
        dy =   self.camerawidth * self.orientationvector[0]

        orthogonal_vector = np.array((dx,dy))
        car_position = np.array((self.x[-1],self.y[-1]))

        self.cam_right_limit = car_position + orthogonal_vector
        self.cam_left_limit =  car_position - orthogonal_vector

        #print("position",car_position)
        #print("direction",self.orientationvector)
        #print("orthogonal",orthogonal_vector)
        #print("left",self.cam_left_limit)
        #print("right",self.cam_right_limit)
        #print("-----------------------")

        self.camrightx.append(self.cam_right_limit[0])
        self.camrighty.append(self.cam_right_limit[1])
        self.camleftx.append(self.cam_left_limit[0])
        self.camlefty.append(self.cam_left_limit[1])

    def _compute_applied_direction(self,delta):
        result = 0
        # If requested rotation speed > max rotation speed
        if self.direction_target > delta * self.direction_max_rotation_speed:
             result = delta * self.direction_max_rotation_speed
             self.direction_target -= result

        elif self.direction_target < - delta * self.direction_max_rotation_speed:
            result -= delta * self.direction_max_rotation_speed
            self.direction_target += result
        else:
            result = self.direction_target
            self.direction_target = 0
            
        self.orientation += result

        #print(self.orientation)

        # Calculate orthogonal vector
        self.orientationvector[0] = math.cos(math.radians(self.orientation))
        self.orientationvector[1] = math.sin(math.radians(self.orientation))
