# Les modification faites par F. Janez reperables avec la mention V2
# le 14 juin 2017

import numpy as np

# V2 : procedure non verifiee
def rank_filter_inf_old(I,rad):

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

# V2 : procedure de rank avec la structure qui avait ete proposee par A. Plyer
# et qui avait ete corrigee pour donner les memes resultats que celle de matlab
def rank_filter_sup_old(I,rad):
    print 'essai'
    nl, nc = I.shape
    R = np.zeros([nl,nc])
    for i in range(1,rad+1): #indice de ligne
        for j in range(rad+1): #indice de colonne
            tmp = np.concatenate([I[i:,j:], np.zeros([nl-i,j])], axis=1) 
            tmp = np.concatenate([tmp,np.zeros([i,nc])],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
            if j is 0:
                K = I[:-i,:] # retrait de i ligne en bas
            else:
                K = I[:-i, :-j] # retrait de i lignes en bas et de j colonnes a droite
            tmp = np.concatenate([np.zeros([nl-i,j]),K],axis = 1)
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
    for i in range(rad+1):
        for j in range(1,rad+1):
            if i is 0:
                K = I[:,j:] # retrait de j colonnes a gauche
            else:
                K = I[:-i,j:] # retrait de j colonnes a gauche et de i lignes en bas
            tmp = np.concatenate([K, np.zeros([nl-i,j])],axis = 1)           
            tmp = np.concatenate([np.zeros([i,nc]), tmp],axis = 0)
           
            idx = (tmp > I)
            R[idx] = R[idx]+1
           
	    # V2 : lignes avec erreurpl.
	    # tmp = np.concatenate([np.zeros([nl-i,j]),I[i:,:-j]], axis=1)
            # tmp = np.concatenate([np.zeros([i,nc]),tmp],axis = 0) => changement ici

            tmp = np.concatenate([np.zeros([nl-i,j]),I[i:,:-j]], axis=1)
            tmp = np.concatenate([tmp, np.zeros([i,nc])],axis = 0)
            idx = (tmp > I)
            R[idx] = R[idx]+1
    return R

# V2 : nouvelle procedure proposee par F. Janez (a priori plus simple)
def rank_filter_sup(I,rad):
    nl, nc = I.shape
    R = np.zeros([nl,nc])
    for i in range(-rad,rad+1): #indice de ligne
        for j in range(-rad,rad+1): #indice de colonne
            if i!=0:
                #print i," ",j
                if i<0: # on decalle vers le haut de i lignes
                     tmp = np.concatenate([I[-i:,:], np.zeros([-i,nc])], axis=0) 
                else: # on decalle vers le bas de i lignes
                     tmp = np.concatenate([np.zeros([i,nc]), I[:-i,:]], axis=0) 
            else:
                tmp = I
                #print tmp.shape
            if j!=0:
                if j<0: # on decalle vers la gauche de j colonnes
                    tmp = np.concatenate([tmp[:,-j:], np.zeros([nl,-j])], axis=1) 
                else: # on decale vers la droite de j colonnes
                    tmp = np.concatenate([np.zeros([nl,j]), tmp[:,:-j]], axis=1)       
                #print tmp.shape
    
            idx = (tmp > I)
            R[idx] = R[idx]+1
          
                        
    return R


def rank_filter_inf(I,rad):
    nl, nc = I.shape
    R = np.zeros([nl,nc])
    for i in range(-rad,rad+1): #indice de ligne
        for j in range(-rad,rad+1): #indice de colonne
            if i!=0:
                #print i," ",j
                if i<0: # on decalle vers le haut de i lignes
                     tmp = np.concatenate([I[-i:,:], np.zeros([-i,nc])], axis=0) 
                else: # on decalle vers le bas de i lignes
                     tmp = np.concatenate([np.zeros([i,nc]), I[:-i,:]], axis=0) 
            else:
                tmp = I
                #print tmp.shape
            if j!=0:
                if j<0: # on decalle vers la gauche de j colonnes
                    tmp = np.concatenate([tmp[:,-j:], np.zeros([nl,-j])], axis=1) 
                else: # on decale vers la droite de j colonnes
                    tmp = np.concatenate([np.zeros([nl,j]), tmp[:,:-j]], axis=1)       
                #print tmp.shape
    
            idx = (tmp < I)
            R[idx] = R[idx]+1
          
                        
    return R




