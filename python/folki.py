import numpy as np

from rank import rank_inf as rank_filter_inf
from rank import rank_sup as rank_filter_sup

# define if use scipy or opencv primitives
USE_OPENCV = False

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




def FolkiIter(I0, I1, iteration = 5, radius = 8, talon = 1.e-8, uinit = None, vinit = None):
    W = lambda x : conv2Sep(x, np.ones([2*radius+1,1]) / 2*radius + 1)
    I0 = I0.astype(np.float32)
    I1 = I1.astype(np.float32)
    if uinit is None:
        u = np.zeros(I0.shape)
    else:
        u = uinit
    if vinit is None:
        v = np.zeros(I1.shape)
    else:
        v = vinit
    Ix, Iy = gradients(I0)
    Ixx = W(Ix*Ix) + talon
    Iyy = W(Iy*Iy) + talon
    Ixy = W(Ix*Iy)
    D   = Ixx*Iyy - Ixy**2
    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))
    for i in range(iteration):
        i1w = interp2(I1,x+u,y+v)
        it = I0 - i1w + u*Ix + v*Iy
        Ixt = W(Ix * it)
        Iyt = W(Iy * it)
        u = (Iyy * Ixt - Ixy * Iyt)/ D
        v = (Ixx * Iyt - Ixy * Ixt) /D
        unvalid = np.isnan(u)|np.isinf(u)|np.isnan(v)|np.isinf(v)
        u[unvalid] = 0
        v[unvalid] = 0
    return u,v


def EFolkiIter(I0, I1, iteration = 5, radius = [8, 4], rank = 4, uinit = None, vinit = None):
    if rank > 0:
        I0 = rank_filter_inf(I0, rank)
        I1 = rank_filter_inf(I1, rank)
    if uinit is None:
        u = np.zeros(I0.shape)
    else:
        u = uinit
    if vinit is None:
        v = np.zeros(I1.shape)
    else:
        v = vinit
    Ix, Iy = gradients(I0)
    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))
    for rad in radius:
        W = lambda x : conv2Sep(x, np.ones([2*radius+1,1]) / 2*radius + 1)
        Ixx = W(Ix*Ix)
        Iyy = W(Iy*Iy)
        Ixy = W(Ix*Iy)
        D   = Ixx*Iyy - Ixy**2
        for i in range(iteration):
            i1w = interp2(I1,x+u,y+v)
            it = I0 - i1w + u*Ix + v*Iy
            Ixt = W(Ix * it)
            Iyt = W(Iy * it)
            u = (Iyy * Ixt - Ixy * Iyt)/ D
            v = (Ixx * Iyt - Ixy * Ixt) /D
            unvalid = np.isnan(u)|np.isinf(u)|np.isnan(v)|np.isinf(v)
            u[unvalid] = 0
            v[unvalid] = 0
    return u,v


def GEFolkiIter(I0, I1, iteration = 5, radius = [8, 4], rank = 4, uinit = None, vinit = None):
    if rank > 0:
        R0 = rank_filter_sup(I0, rank)
        R1i = rank_filter_inf(I1, rank)
        R1s = rank_filter_sup(I1, rank)
    if uinit is None:
        u = np.zeros(I0.shape)
    else:
        u = uinit
    if vinit is None:
        v = np.zeros(I1.shape)
    else:
        v = vinit
    Ix, Iy = gradients(R0)
    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))
    for rad in radius:
        W = lambda x : conv2Sep(x, np.ones([2*radius+1,1]) / 2*radius + 1)
        Ixx = W(Ix*Ix)
        Iyy = W(Iy*Iy)
        Ixy = W(Ix*Iy)
        D   = Ixx*Iyy - Ixy**2
        for i in range(iteration):
            I1w = interp2(I1,x+u,y+v)
            crit1 = conv2Sep(np.abs(I0-I1w), np.ones([2*rank+1,1]))
            crit2 = conv2Sep(np.abs(1-I0-I1w), np.ones([2*rank+1,1]))
            R1w = interp2(R1s,x+u,y+v)
            R1w_i = interp2(R1i,x+u,y+v)
            R1w[crit1 > crit2] = R1w_1[crit1 > crit2]
            it = R0 - R1w + u*Ix + v*Iy
            Ixt = W(Ix * it)
            Iyt = W(Iy * it)
            u = (Iyy * Ixt - Ixy * Iyt)/ D
            v = (Ixx * Iyt - Ixy * Ixt) /D
            unvalid = np.isnan(u)|np.isinf(u)|np.isnan(v)|np.isinf(v)
            u[unvalid] = 0
            v[unvalid] = 0
    return u,v


