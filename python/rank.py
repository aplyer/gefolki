import numpy as np


def rank_inf(I,rad):
    nl, nc = I.shape
    R = np.zeros([nl,nc])
    for i in range(1,rad+1):
        for j in range(rad+1):
            tmp = np.concatenate([I[i:,j:], np.zeros([nl-i,j])], axis=1)
            tmp = np.concatenate([tmp,np.zeros([i,nc])],axis = 0)
            idx = (tmp < I)
            R[idx] = R[idx]+1
            if j is 0:
                K = I[:-i,:]
            else:
                K = I[:-i, :-j]
            tmp = np.concatenate([np.zeros([nl-i,j]),K],axis = 1)
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
            idx = (tmp < I)
            R[idx] = R[idx]+1
    for i in range(rad+1):
        for j in range(1,rad+1):
            if i is 0:
                K = I[:,j:]
            else:
                K = I[:-i,j:]
            tmp = np.concatenate([K, np.zeros([nl-i,j])],axis = 1)
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
            idx = (tmp < I)
            R[idx] = R[idx]+1
            tmp = np.concatenate([np.zeros([nl-i,j]),I[i:,:-j]], axis=1)
            tmp = np.concatenate([np.zeros([i,nc]),tmp],axis = 0)
            idx = (tmp < I)
            R[idx] = R[idx]+1
    return R

def rank_sup(I,rad):
    nl, nc = I.shape
    R = np.zeros([nl,nc])
    for i in range(1,rad+1):
        for j in range(rad+1):
            tmp = np.concatenate([I[i:,j:], np.zeros([nl-i,j])], axis=1)
            tmp = np.concatenate([tmp,np.zeros([i,nc])],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
            if j is 0:
                K = I[:-i,:]
            else:
                K = I[:-i, :-j]
            tmp = np.concatenate([np.zeros([nl-i,j]),K],axis = 1)
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
    for i in range(rad+1):
        for j in range(1,rad+1):
            if i is 0:
                K = I[:,j:]
            else:
                K = I[:-i,j:]
            tmp = np.concatenate([K, np.zeros([nl-i,j])],axis = 1)
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
            tmp = np.concatenate([np.zeros([nl-i,j]),I[i:,:-j]], axis=1)
            tmp = np.concatenate([np.zeros([i,nc]),tmp],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
    return R








