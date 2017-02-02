import numpy as np
# define if use scipy or opencv primitives
USE_OPENCV = True

if USE_OPENCV:
    import cv2
    interp2 = lambda  I,x,y : cv2.remap(I,x.astype(np.float32),y.astype(np.float32),cv2.INTER_LINEAR)
    conv2   = lambda  I,w   : cv2.filter2D(I,-1,w)
else:
    from scipy import ndimage
    interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 1, mode = 'nearest')
    conv2   = lambda I, w    : ndimage.convolve(I, w, mode = 'constant')

gradients = lambda I    : (conv2(I,np.array([[-1,0,1]])), conv2(I, np.array([[-1,0,1]]).T))
conv2Sep  = lambda I, w : conv2(conv2(I,w),w.T)


