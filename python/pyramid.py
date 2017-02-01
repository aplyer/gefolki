import numpy as np

from primitive import *


class BurtOF:
    def __init__(self, flow, levels = 4):
        self.flow = flow
        self.levels = 4
    def __call__(self, I0, I1, **kparams):
        if kparams.has_key('levels'):
            self.levels = kparams.pop('levels')
        Py0 = [I0]
        Py1 = [I1]
        for i in range(self.levels, 0, -1):
            Py0.append(self.pyrUp(Py0[-1]))
            Py1.append(self.pyrUp(Py1[-1]))
        u = np.zeros(Py0[-1].shape)
        v = np.zeros(Py0[-1].shape)
        for i in range(self.levels, -1, -1):
            print('scale : %d'%i)
            kparams['uinit'] = u
            kparams['vinit'] = v
            u,v = self.flow(Py0[i], Py1[i], **kparams)
            if i > 0:
                col, row = Py0[i-1].shape[1], Py0[i-1].shape[0]
                u = 2 * self.pyrDown(u, (row, col))
                v = 2 * self.pyrDown(v, (row, col))
        return u, v
    def pyrUp(self, I):
        a = 0.4
        burt1D = np.array([[1./4.-a/2.,1./4.,a,1./4.,1./4.-a/2.]])
        M = conv2Sep(I,burt1D)
        return M[::2,::2]
    def pyrDown(self, I, shape):
        res = np.zeros(shape)
        I = np.repeat(np.repeat(I,2,0),2,1)
        col, row = I.shape[1], I.shape[0]
        res[:row, :col] = I
        return res





