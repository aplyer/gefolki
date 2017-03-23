import numpy as np

from scipy.io import loadmat
from scipy.ndimage import imread

import pylab as pl

from algorithm import GEFolki, EFolki, Folki # three optical flow algorithms
from tools import wrapData # to apply registration


def demo():
    radar    = imread('../datasets/radar_bandep.png')
    Ilidari  = imread('../datasets/lidar_georef.png')

    pl.figure()
    pl.imshow(radar)
    pl.title('Radar in pauli color')


    pl.figure()
    pl.imshow(Ilidari)
    pl.title('Lidar in colormap jet')



    Iradar = radar[:,:,0] # Selection of first band in Colored Pauli Basis, Red=hh-vv
    Iradar = Iradar.astype(np.float32)/255
    Ilidar = Ilidari.astype(np.float32)/255
    
  
    
    u, v = EFolki(Iradar, Ilidar, iteration = 2, radius = [32,24,16,8], rank = 4, levels = 5)
    N = np.sqrt(u**2+v**2)
    pl.figure()
    pl.imshow(N)
    pl.title('Norm of LIDAR to RADAR registration')
    pl.colorbar() 
    
  
    Ilidar_resampled=wrapData(Ilidar,u,v)
    
    
    C = np.dstack((Ilidar,Iradar,Ilidar))
    pl.figure()
    pl.imshow(C)
    pl.title('Imfuse of RADAR and LIDAR')

     
    D = np.dstack((Ilidar_resampled,Iradar,Ilidar_resampled))
    pl.figure()
    pl.imshow(D)
    pl.title('Imfuse of RADAR and LIDAR after coregistration')





if __name__ == '__main__':
    demo()
    pl.show()
else:
    pl.interactive(True)
    demo()
