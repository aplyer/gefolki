import numpy as np
from primitive import interp2


def wrapData(I, u, v):
    '''
        Apply the [u,v] optical flow to the data I
    '''
    col, row = I.shape[1], I.shape[0]
    X, Y = np.meshgrid(range(col), range(row))
    R = interp2(I, X+u, Y+v)
    return R
