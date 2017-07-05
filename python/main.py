""" 
%     « Copyright (c) 2016, Elise Koeniguer, Aurélien Plyer (Onera) » 
%     This file is part of GeFolki.
%
%     WARNING - THIS VERSION IS COMPATIBLE WITH THE ONE DISTRIBUTED IN MATLAB -
%     FOR THE MOMENT, IT REQUIRES THE USE OF OPENCV LIBRARY - HAS BEEN TESTED ONLY WITH LINUX 
% 
%     GeFolki is free software: you can redistribute it and/or modify
%     it under the terms of the GNU General Public License as published by
%     the Free Software Foundation, either version 3 of the License, or
%     (at your option) any later version.
% 
%     GeFolki is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.
% 
%     You should have received a copy of the GNU General Public License
%     along with GeFolki in the file copying.txt.  
%     If not, see <http://www.gnu.org/licenses/gpl.txt>.
%
% ------------------------------------------------------------------------
%
%     GeFolki est un logiciel libre ; vous pouvez le redistribuer ou le
%     modifier suivant les termes de la GNU General Public License telle
%     que publiée par la Free Software Foundation ; soit la version 3 de la
%     licence, soit (à votre gré) toute version ultérieure.
% 
%     GeFolki est distribué dans l'espoir qu'il sera utile, mais SANS
%     AUCUNE GARANTIE ; sans même la garantie tacite de QUALITÉ MARCHANDE
%     ou d'ADÉQUATION à UN BUT PARTICULIER. Consultez la GNU General Public
%     License pour plus de détails.
% 
%     Vous devez avoir reçu une copie de la GNU General Public License en
%     même temps que Gefolki dans le fichier copying.txt ; si ce n'est pas
%     le cas, consultez % <http://www.gnu.org/licenses/gpl.txt
"""



import numpy as np

from scipy.io import loadmat
from scipy.ndimage import imread

import pylab as pl

from algorithm import GEFolki, EFolki, Folki # three optical flow algorithms
from tools import wrapData # to apply registration

from PIL import Image

def demo():
   # cas radar lidar
    print "Debut recalage Lidar/Radar\n"
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

    print "Fin recalage Lidar/Radar \n\n"

    # cas optique/radar
    print "Debut recalage optique/Radar\n"
    radar    = imread('../datasets/radar_bandep.png')
    Ioptique  = imread('../datasets/optiquehr_georef.png')

    pl.figure()
    pl.imshow(radar)
    pl.title('Radar in pauli color')


    pl.figure()
    pl.imshow(Ioptique)
    pl.title('Optique')

    Iradar = radar[:,:,0] # Selection of first band in Colored Pauli Basis, Red=hh-vv
    Iradar = Iradar.astype(np.float32)
    Ioptique = Ioptique[:,:,1]
    Ioptique = Ioptique.astype(np.float32)
   

    # attention : range(32,4,-4) va de 32 a 8 en diminuant de 4
    u, v = GEFolki(Iradar, Ioptique, iteration = 2, radius = range(32,4,-4), rank = 4, levels = 6)
    
    N = np.sqrt(u**2+v**2)
    pl.figure()
    pl.imshow(N)
    pl.title('Norm of OPTIC to RADAR registration')
    pl.colorbar() 
    

    Ioptique_resampled=wrapData(Ioptique,u,v)
   
     
    C = np.dstack((Ioptique,Iradar,Ioptique))
    pl.figure()
    pl.imshow(C)
    pl.title('Imfuse of RADAR and OPTIC')

     
    D = np.dstack((Ioptique_resampled,Iradar,Ioptique_resampled))
    pl.figure()
    pl.imshow(D)
    pl.title('Imfuse of RADAR and OPTIC after coregistration')
    print "Fin recalage optique/Radar \n\n"




if __name__ == '__main__':
    demo()
    pl.show()
else:
    pl.interactive(True)
    demo()
