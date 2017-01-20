import numpy as np


class BurtOF:
    def __init__(flow, levels = 4):
        self.flow = flow
        self.levels = 4
    def run(I0, I1):
        Py0 = [I0]
        Py1 = [I1]
        for i in range(self.levels, 0, -1):
            Py0.append(self.pyrUp(Py0[-1]))
            Py1.append(self.pyrUp(Py1[-1]))
        u = np.zeros(Py0.shape)
        v = np.zeros(Py0.shape)
        for i in range(self.levels, 0, -1):
            u,v = self.flow(Py0[i], Py1[i])
            if i > 0:
                u = 2 * self.pyrDown(u)
                v = 2 * self.pyrDown(v)
        return u, v
    def pyrUp(self, I):
        return None
    def pyrDown(self, I):
        return None

        



