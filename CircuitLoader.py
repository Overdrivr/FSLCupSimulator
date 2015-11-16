import cv2
import numpy as np

def load_circuit(filename):
    im =  cv2.imread(filename,0)
    ret,thresh = cv2.threshold(im,127,255,0)
    contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    xt = []
    yt = []

    for coords in contours[1][1]:
        xt.append(coords[0][0])
        yt.append(coords[0][1])

    x = np.array(xt)
    y = np.array(yt)

    return x,y,im
