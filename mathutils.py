#
# line segment intersection using vectors
# see Computer Graphics by F.S. Hill
#
import numpy as np
import math

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    if denom == 0:
        return None
    num = np.dot( dap, dp )
    length = (num / denom.astype(float))
    if length > math.sqrt(db[0] * db[0] + db[1]*db[1]):
        return None
    return length*db + b1
