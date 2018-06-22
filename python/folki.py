import numpy as np
from rank import rank_inf as rank_filter_inf
from rank import rank_sup as rank_filter_sup
from PIL import Image
from primitive import *
from adapthist import *
import scipy


def conv2SepMatlabbis(I, fen):

    rad = int((fen.size-1)/2)
    ligne = np.zeros((rad, I.shape[1]))
    I = np.append(ligne, I, axis=0)
    I = np.append(I, ligne, axis=0)

    colonne = np.zeros((I.shape[0], rad))
    I = np.append(colonne, I, axis=1)
    I = np.append(I, colonne, axis=1)

    res = conv2bis(conv2bis(I, fen.T), fen)
    return res


def FolkiIter(I0, I1, iteration=5, radius=8, talon=1.e-8, uinit=None, vinit=None):
   
    W = lambda x: conv2Sep(x, np.ones([2*radius+1, 1]))/(2*radius + 1)
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
    D = Ixx*Iyy - Ixy**2
    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))
    for i in range(iteration):
        i1w = interp2(I1, x+u, y+v)
        it = I0 - i1w + u*Ix + v*Iy
        Ixt = W(Ix * it)
        Iyt = W(Iy * it)
        u = (Iyy * Ixt - Ixy * Iyt)/D
        v = (Ixx * Iyt - Ixy * Ixt)/D
        unvalid = np.isnan(u) | np.isinf(u) | np.isnan(v) | np.isinf(v)
        u[unvalid] = 0
        v[unvalid] = 0
    return u, v


def EFolkiIter(I0, I1, iteration=5, radius=[8, 4], rank=4, uinit=None,vinit=None):
    talon=1.e-8
    if rank > 0:
        I0 = rank_filter_sup(I0, rank)
        I1 = rank_filter_sup(I1, rank)

    if uinit is None:
        u = np.zeros(I0.shape)
    else:
        u = uinit
    if vinit is None:
        v = np.zeros(I1.shape)
    else:
        v = vinit

    Iy, Ix = np.gradient(I0)

    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))

    for rad in radius:

        burt1D = np.array(np.ones([1, 2*rad+1]))/(2*rad + 1)
        W = lambda x: conv2SepMatlabbis(x, burt1D)

        Ixx = W(Ix*Ix) + talon
        Iyy = W(Iy*Iy) + talon
        Ixy = W(Ix*Iy)
        D = Ixx*Iyy - Ixy**2

        for i in range(iteration):
            i1w = interp2(I1, x+u, y+v)

            it = I0 - i1w + u*Ix + v*Iy
            Ixt = W(Ix * it)
            Iyt = W(Iy * it)
            u = (Iyy * Ixt - Ixy * Iyt)/D
            v = (Ixx * Iyt - Ixy * Ixt)/D
            unvalid = np.isnan(u) | np.isinf(u) | np.isnan(v) | np.isinf(v)
            u[unvalid] = 0
            v[unvalid] = 0
    return u, v


def GEFolkiIter(I0, I1, iteration=5, radius=[8, 4], rank=4, uinit=None, vinit=None):

    if rank > 0:
        R0 = rank_filter_sup(I0, rank)
        R1i = rank_filter_inf(I1, rank)
        R1s = rank_filter_sup(I1, rank)

    H0 = I0
    H1 = I1

    from skimage.transform import resize

    x = I0.shape[1]
    res_x = x % 8
    add_x = 8 - x % 8 if res_x > 0 else 0

    y = I0.shape[0]
    res_y = y % 8
    add_y = 8 - y % 8 if res_y > 0 else 0

    if res_x > 0 or res_y > 0:
        toto = resize(I0, (y+add_y, x+add_x), order=1)
    else:
        toto = I0

    toto = toto*255
    toto = toto.astype(np.uint8)
    H0 = equalize_adapthist(toto, 8, clip_limit=1, nbins=256)

    if res_x > 0 or res_y > 0:
        H0 = resize(H0, (y, x), order=1)

    H0 = H0.astype(np.float32)
    H0 = H0/H0.max()

    x = I1.shape[1]
    res_x = x % 8
    add_x = 8 - x % 8 if res_x > 0 else 0

    y = I1.shape[0]
    res_y = y % 8
    add_y = 8 - y % 8 if res_y > 0 else 0

    if res_x > 0 or res_y > 0:
        toto = resize(I1, (y+add_y, x+add_x), order=1)
    else:
        toto = I1

    toto = toto*255
    toto = toto.astype(np.uint8)
    H1 = equalize_adapthist(toto, 8, clip_limit=1, nbins=256)

    if res_x > 0 or res_y > 0:
        H1 = resize(H1, (y, x), order=1)

    H1 = H1.astype(np.float32)
    H1 = H1/H1.max()

    if uinit is None:
        u = np.zeros(I0.shape)
    else:
        u = uinit
    if vinit is None:
        v = np.zeros(I1.shape)
    else:
        v = vinit

    Iy, Ix = np.gradient(R0)

    cols, rows = I0.shape[1], I0.shape[0]
    x, y = np.meshgrid(range(cols), range(rows))
    for rad in radius:

        burt1D = np.array(np.ones([1, 2*rad+1]))/(2*rad + 1)
        W = lambda xin: conv2SepMatlabbis(xin, burt1D)

        Ixx = W(Ix*Ix)
        Iyy = W(Iy*Iy)
        Ixy = W(Ix*Iy)
        D = Ixx*Iyy - Ixy**2

        for i in range(iteration):

            dx = x + u
            dy = y + v
            dx[dx < 0] = 0
            dy[dy < 0] = 0
            dx[dx > cols-1] = cols-1
            dy[dy > rows-1] = rows-1

            H1w = interp2(H1, dx, dy)

            crit1 = conv2SepMatlabbis(np.abs(H0-H1w), np.ones([2*rank+1, 1]))
            crit2 = conv2SepMatlabbis(np.abs(1-H0-H1w), np.ones([2*rank+1, 1]))

            R1w = interp2(R1s, x+u, y+v)
            R1w_1 = interp2(R1i, x+u, y+v)

            R1w[crit1 > crit2] = R1w_1[crit1 > crit2]
            it = R0 - R1w + u*Ix + v*Iy
            Ixt = W(Ix * it)
            Iyt = W(Iy * it)
            u = (Iyy * Ixt - Ixy * Iyt)/D
            v = (Ixx * Iyt - Ixy * Ixt)/D
            unvalid = np.isnan(u) | np.isinf(u) | np.isnan(v) | np.isinf(v)
            u[unvalid] = 0
            v[unvalid] = 0

    return u, v
