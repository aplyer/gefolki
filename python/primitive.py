# Version corrigee par F. Janez pour qu elle corresponde a la version matlab
# le 14 juin 2017
from scipy import signal
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
        # V2 pour etre equivalent a la version matlab
        #interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 3, mode = 'nearest')
	   interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 3, mode = 'linear')
 
    # a priori plus utilise
    conv2   = lambda I, w    : ndimage.convolve(I, w, mode = 'nearest')
    
    # V2 : pour etre equivalent avec procedure matlab
    conv2bis   = lambda I, w    : signal.convolve2d(I, w, mode = 'valid')
    
    # a priori plus utilise
    gradients = lambda I    : (conv2(I,np.array([[1,0,-1]])), conv2(I, np.array([[1,0,-1]]).T))

# V2 : petit changement pour se conformer a matlan mais dont l impact n a pas ete mesure
# conv2Sep  = lambda I, w : conv2(conv2(I,w),w.T)
# a priori plus utilise
conv2Sep  = lambda I, w : conv2(conv2(I,w.T),w)

