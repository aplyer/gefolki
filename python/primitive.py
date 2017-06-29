# Version corrigee par F. Janez pour qu elle corresponde a la version matlab
# le 14 juin 2017
from scipy import signal
import numpy as np

USE_LINEAR = True # linear or cubic interpolate

from scipy import ndimage
if USE_LINEAR:
    interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 1, mode = 'nearest')
else:
    interp2 = lambda I, x, y : ndimage.map_coordinates( I, [ y, x], order = 3, mode = 'linear')
conv2 = lambda I, w    : signal.convolve2d(I, w, mode = 'same', boundary='fill', fillvalue=0.0)
# a priori plus utilise
gradients = lambda I    : np.gradients(I)
conv2Sep  = lambda I, w : conv2(conv2(I,w.T),w)

