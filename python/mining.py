"""
Date : 01/10/2018
"""
import numpy as np
import argparse
#from algorithm import EFolki
from skimage.io import imread
import pylab as pl
from skimage.transform import resize
#from rank import rank_sup as rank_filter_sup
from rank import rank_inf as rank_filter_inf
import rasterio

def mining(file_path_master, file_path_slave, rank, fdecimation):
    """ Load a raster.
    """
    src=rasterio.open(file_path_master)
    M=src.read()
    Master=M[0,:,:];
    
    pl.figure()
    pl.imshow(Master)
    pl.title('Master')
    
  
    S = imread(file_path_slave)
    pl.figure()
    pl.imshow(S)
    pl.title('Slave: Image to find within the Master')  
    


    Slave=S[:,:,0];
    dimx,dimy=np.shape(Master);
    dimxn,dimyn=np.shape(Slave);
    
    # Decimation

    nx = int(round(dimx/fdecimation)) 
    ny = int(round(dimy/fdecimation))
    Mg = resize(Master,(nx, ny),1,'constant')
    nsx = int(round(dimxn/fdecimation)) 
    nsy = int(round(dimyn/fdecimation))
    Sg = resize(Slave,(nsx, nsy),1,'constant')       

# Rank computation and Criterion on images after deximation
    Mg_rank = rank_filter_inf(Mg, rank) # rank sup : high value pixels have low rank
    Sg_rank = rank_filter_inf(Sg, rank)
                 
    R=np.zeros((nx-nsx-1,ny-nsy-1)); 
    indices=np.nonzero(Sg_rank);
    test2=Sg_rank[indices];

    for k in range(0,nx-nsx-1):
        for p in range(0,ny-nsy-1):
            test1=Mg_rank[k:k+nsx,p:p+nsy];
            test1=test1[indices];
            test=(test1-test2)**2
            R[k,p]=test.mean();  
        
    pl.figure()
    pl.imshow(R,vmin=np.min(R[np.nonzero(R)]),vmax=R.max(),cmap='jet')
    pl.title('Criterion after decimation')  
    
  
    ind = np.unravel_index(np.argmin(R, axis=None), R.shape)
    indx=(ind[0]*fdecimation)
    indy=(ind[1]*fdecimation)

    indx1=max(0,indx-100)
    indx1max=min(dimx,indx+dimxn+100)
    indy1=max(0,indy-100)
    indy1max=min(dimy,indy+dimyn+100)

# Rank computation and Criterion on images without deximation after preinitialization
    Master_crop = Master[indx1:indx1max,indy1:indy1max]
    M_rank_crop = rank_filter_inf(Master_crop, rank) # rank sup : high value pixels have low rank
    S_rank = rank_filter_inf(Slave, rank)

    dimxcrop,dimycrop=np.shape(M_rank_crop);
    Rfin=np.zeros((dimxcrop-dimxn-1,dimycrop-dimyn-1)); 
    indices=np.nonzero(S_rank);
    test2=S_rank[indices];

    for k in range(0,dimxcrop-dimxn-1):
        for p in range(0,dimycrop-dimyn-1):
            test1=M_rank_crop[k:k+dimxn,p:p+dimyn];
            test1=test1[indices];
            test=(test1-test2)**2
            Rfin[k,p]=test.mean();
        
# Final Extraction
    ind = np.unravel_index(np.argmin(Rfin, axis=None), Rfin.shape)
    indx2=(ind[0])
    indy2=(ind[1])
    Master_final = Master_crop[indx2:indx2+dimxn,indy2:indy2+dimyn];

    pl.figure()
    pl.imshow(Rfin,vmin=np.min(Rfin[np.nonzero(Rfin)]),vmax=Rfin.max(),cmap='jet')
    pl.title('Fine Criterion without decimation after préinitialisation')  
    
    rgb = np.dstack((Slave,Master_final,Slave))

    pl.figure()
    pl.imshow(rgb)
    pl.title('Superposition of Slave and Master Extraction')

    pl.show()

    
    xmin=indx1+indx2
    ymin=indy1+indy2
    xmax=xmin+dimxn
    ymax=xmax+dimyn

    return xmin,xmax,ymin,ymax,Master_final





def main():
    """Main function."""
    # create the parser for arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_master", type=str, default=None,
                        help="Filepath of image Sentinel 1 Master")
    parser.add_argument("--input_slave", type=str, default=None,
                        help="Filepath of Slave image to find within Master")
    parser.add_argument("--rank", type=int, default=3, help="Rank radius")
    parser.add_argument("--fdecimation", type=int, default=8, help="Decimation Factor")
    args = parser.parse_args()

    file_path_master=args.input_master
    file_path_slave=args.input_slave
    rank=args.rank
    fdecimation=args.fdecimation

    print("Execution")
    xmin,xmax,ymin,ymax,master_extract=mining(file_path_master, file_path_slave, rank, fdecimation)
    print("done")

#==============================================
if __name__ == "__main__":
    main()

#EOF
