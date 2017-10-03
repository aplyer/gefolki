
from scipy import signal
import numpy as np
from scipy.interpolate import griddata

USE_LINEAR = True

from scipy import ndimage

if USE_LINEAR:
    interp2 = lambda I, x, y : ndimage.map_coordinates( I, [y, x], order=1, mode='nearest').reshape(I.shape)
else:
    interp2 = lambda I, x, y : ndimage.map_coordinates( I, [y, x], order=3, mode='nearest')

conv2bis   = lambda I, w : signal.convolve2d(I, w, mode='valid')
conv2Sep  = lambda I, w : conv2(conv2(I, w.T), w)
