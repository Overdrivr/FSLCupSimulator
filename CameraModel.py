import cv2

class Camera:
    def __init__(self):
        pass

    def get_line(self,cameraleft,cameraright,track):
        # Todo invert leftToRight if needed
        l =  line(cameraleft[0].astype(int),
                  cameraleft[1].astype(int),
                  cameraright[0].astype(int),
                  cameraright[1].astype(int),
                  track)

        #for i in range(len(l)):
        #    print(i,":",l[i])
        return l

# From http://stackoverflow.com/questions/5186939/algorithm-for-drawing-a-4-connected-line
def line(x0,x1,y0,y1,img):
    l = []
    dx = abs(x1 - x0)    # distance to travel in X
    dy = abs(y1 - y0)    # distance to travel in Y

    if x0 < x1:
        ix = 1           # x will increase at each step
    else:
        ix = -1          # x will decrease at each step

    if y0 < y1:
        iy = 1           # y will increase at each step
    else:
        iy = -1          # y will decrease at each step

    e = 0                # Current error

    for i in range(dx + dy):
        l.append(img[x0, y0])
        e1 = e + dy
        e2 = e - dx
        if abs(e1) < abs(e2):
            # Error will be smaller moving on X
            x0 += ix
            e = e1
        else:
            # Error will be smaller moving on Y
            y0 += iy
            e = e2
    return l
