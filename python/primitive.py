import numpy as np
# define if use scipy or opencv primitives
USE_OPENCV = False
USE_LINEAR = True # linear or cubic interpolate

if USE_OPENCV:
    import cv2
    if USE_LINEAR:
        interp2 = lambda  I,x,y : cv2.remap(I,x.astype(np.float32),y.astype(np.float32),cv2.INTER_LINEAR)
    else:
        interp2 = lambda  I,x,y : cv2.remap(I,x.astype(np.float32),y.astype(np.float32),cv2.INTER_CUBIC)
    conv2   = lambda  I,w   : cv2.filter2D(I,-1,w)
    gradients = lambda I    : (conv2(I,np.array([[-1,0,1]])), conv2(I, np.array([[-1,0,1]]).T))
else:
    from scipy import ndimage
    if USE_LINEAR:
        interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 1, mode = 'nearest')
    else:
        interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 3, mode = 'nearest')

    conv2   = lambda I, w    : ndimage.convolve(I, w, mode = 'mirror')
    gradients = lambda I    : (conv2(I,np.array([[1,0,-1]])), conv2(I, np.array([[1,0,-1]]).T))
conv2Sep  = lambda I, w : conv2(conv2(I,w),w.T)


