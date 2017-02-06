import numpy as np

from scipy.io import loadmat
from scipy.ndimage import imread

import pylab as pl

from algorithm import GEFolki, EFolki, Folki # three optical flow algorithms
from tools import wrapData # to apply registration


def demo():
    radar    = imread('../datasets/radar_bandep.png')
    Ioptique = imread('../datasets/optiquehr_georef.png')
    Ilidari  = imread('../datasets/lidar_georef.png')

    pl.figure()
    pl.imshow(radar)
    pl.title('Radar in pauli color')

    pl.figure()
    pl.imshow(Ioptique)
    pl.title('RGB visible aerial image')

    pl.figure()
    pl.imshow(Ilidari)
    pl.title('Lidar in colormap jet')

    HH1 = loadmat('../datasets/radar_bandel_hh1.mat')['Radar_bandeL_HH1']
    HH2 = loadmat('../datasets/radar_bandel_hh2.mat')['Radar_bandeL_HH2']


    pl.figure()
    pl.imshow(np.abs(np.log(np.abs(HH1))), 'gray', vmin = 0, vmax = 2.4)

    pl.figure()
    pl.imshow(np.abs(np.log(np.abs(HH1))), 'gray', vmin = 0, vmax = 2.4)
    pl.title('HH of first radar')


    pl.figure()
    pl.imshow(np.abs(np.log(np.abs(HH2))), 'gray', vmin = 0, vmax = 2.4)
    pl.title('HH of second radar')

    A = np.mean(radar, 2).astype(np.float32)
    B = Ilidari.astype(np.float32)

    u, v = GEFolki(np.abs(HH1), np.abs(HH2), iteration = 5, radius = [16,32], rank = 4, levels = 3)
    N = np.sqrt(u**2+v**2)
    pl.figure()
    pl.imshow(N)
    pl.title('Norme of HH2 to HH1 registration')




if __name__ == '__main__':
    demo()
    pl.show()
else:
    pl.interactive(True)
    demo()
