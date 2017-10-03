
import numpy as np


def rank_sup(I, rad):
    nl, nc = I.shape
    R = np.zeros([nl, nc])
    for i in range(-rad, rad+1):  # indice de ligne
        for j in range(-rad, rad+1):  # indice de colonne
            if i != 0:
                if i < 0:
                     tmp = np.concatenate([I[-i:, :], np.zeros([-i, nc])], axis=0)
                else:
                     tmp = np.concatenate([np.zeros([i, nc]), I[:-i, :]], axis=0)
            else:
                tmp = I
            if j != 0:
                if j < 0:
                    tmp = np.concatenate([tmp[:, -j:], np.zeros([nl, -j])], axis=1)
                else:
                    tmp = np.concatenate([np.zeros([nl, j]), tmp[:, :-j]], axis=1)

            idx = (tmp > I)
            R[idx] = R[idx]+1

    return R


def rank_inf(I, rad):
    nl, nc = I.shape
    R = np.zeros([nl, nc])
    for i in range(-rad, rad+1):
        for j in range(-rad, rad+1):
            if i != 0:
                if i < 0:  # on decalle vers le haut de i lignes
                     tmp = np.concatenate([I[-i:, :], np.zeros([-i, nc])], axis=0)
                else:
                     tmp = np.concatenate([np.zeros([i, nc]), I[:-i, :]], axis=0)
            else:
                tmp = I
            if j != 0:
                if j < 0:
                    tmp = np.concatenate([tmp[:, -j:], np.zeros([nl, -j])], axis=1)
                else:
                    tmp = np.concatenate([np.zeros([nl, j]), tmp[:, :-j]], axis=1)

            idx = (tmp < I)
            R[idx] = R[idx]+1

    return R
