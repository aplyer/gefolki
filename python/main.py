#!/usr/bin/python

import numpy as np

from scipy.io import loadmat
from scipy.ndimage import imread

import pylab as pl

from algorithm import GEFolki, EFolki, Folki
from tools import wrapData

from PIL import Image


def demo():
    print("Debut recalage Lidar/Radar\n")
    radar = imread('../datasets/radar_bandep.png')
    Ilidari = imread('../datasets/lidar_georef.png')

    pl.figure()
    pl.imshow(radar)
    pl.title('Radar in pauli color')

    pl.figure()
    pl.imshow(Ilidari)
    pl.title('Lidar in colormap jet')

    Iradar = radar[:, :, 0]
    Iradar = Iradar.astype(np.float32)/255
    Ilidar = Ilidari.astype(np.float32)/255

    u, v = EFolki(Iradar, Ilidar, iteration=2, radius=[32, 24, 16, 8], rank=4, levels=5)
    N = np.sqrt(u**2+v**2)
    pl.figure()
    pl.imshow(N)
    pl.title('Norm of LIDAR to RADAR registration')
    pl.colorbar()

    Ilidar_resampled = wrapData(Ilidar, u, v)

    C = np.dstack((Ilidar, Iradar, Ilidar))
    pl.figure()
    pl.imshow(C)
    pl.title('Imfuse of RADAR and LIDAR')

    D = np.dstack((Ilidar_resampled, Iradar, Ilidar_resampled))
    pl.figure()
    pl.imshow(D)
    pl.title('Imfuse of RADAR and LIDAR after coregistration')

    print("Fin recalage Lidar/Radar \n\n")

    print("Debut recalage optique/Radar\n")
    radar = imread('../datasets/radar_bandep.png')
    Ioptique = imread('../datasets/optiquehr_georef.png')

    pl.figure()
    pl.imshow(radar)
    pl.title('Radar in pauli color')

    pl.figure()
    pl.imshow(Ioptique)
    pl.title('Optique')

    Iradar = radar[:, :, 0]
    Iradar = Iradar.astype(np.float32)
    Ioptique = Ioptique[:, :, 1]
    Ioptique = Ioptique.astype(np.float32)

    u, v = GEFolki(Iradar, Ioptique, iteration=2, radius=range(32, 4, -4), rank=4, levels=6)

    N = np.sqrt(u**2+v**2)
    pl.figure()
    pl.imshow(N)
    pl.title('Norm of OPTIC to RADAR registration')
    pl.colorbar()

    Ioptique_resampled = wrapData(Ioptique, u, v)

    C = np.dstack((Ioptique/255, Iradar/255, Ioptique/255))
    pl.figure()
    pl.imshow(C)
    pl.title('Imfuse of RADAR and OPTIC')

    D = np.dstack((Ioptique_resampled/255, Iradar/255, Ioptique_resampled/255))
    pl.figure()
    pl.imshow(D)
    pl.title('Imfuse of RADAR and OPTIC after coregistration')
    print("Fin recalage optique/Radar \n\n")


if __name__ == '__main__':
    demo()
    pl.show()
else:
    pl.interactive(True)
    demo()
