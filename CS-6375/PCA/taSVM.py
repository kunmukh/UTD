# coding:utf-8
import math
import numpy as np
from cvxopt import solvers,matrix
from pdb import set_trace
solvers.options['show_progress'] = False

class SlackSVM:
    def fit(self,X,Y,c):
        assert(Y.shape == (X.shape[0],))
        n_feature = X.shape[1]
        n_sample = Y.size
        n_paras = n_feature + 1 + n_sample
        # construct P
        P = np.zeros(n_paras)
        for i in range(n_feature):
            P[i]=1
        P = np.diag(P)

        # construct q
        q = np.zeros(n_paras)
        for i in range(n_sample):
            q[n_feature+1+i]=c

        # construct G phase 1, consider y(wx+b)>=1-ksi
        G = []
        for i in range(n_sample):
            # form: y_i*x_i,y_i,0..0,1,0..0
            tmp = np.zeros(n_paras)
            x_i = X[i,:]
            y_i = Y[i]
            tmp[0:n_feature] = y_i*x_i
            tmp[n_feature] = y_i
            tmp[n_feature+1+i] = 1
            G.append(tmp)

        # construct G phase 2, consider ksi >= 0
        for i in range(n_sample):
            tmp = np.zeros(n_paras)
            tmp[n_feature+1+i] =1
            G.append(tmp)
        G = np.array(G)

        # construct h
        h=np.zeros(n_sample*2)
        for i in range(n_sample):
            h[i]=1

        # transform Gx >= h to Gx <= h
        G=-G; h=-h

        P = matrix(P)
        q = matrix(q)
        G = matrix(G)
        h = matrix(h)
        ret = solvers.qp(P,q,G,h)
        solution = ret['x']

        # decompose solution to w,b,ksi
        w = solution[0:n_feature]
        w = np.array(w).flatten()
        b = float(solution[n_feature])
        # ksi = list(solution[n_feature+1:])
        # verify(X,Y,w,b,ksi)
        self.W  = w
        self.b = b
        return self

    def predict(self,X):
        assert(X.shape[1] == self.W.size)
        W = self.W.reshape(-1,1)
        t = np.dot(X,W) + self.b
        t = t.flatten()
        t[t>0] = 1
        t[t<0] = -1
        return t

    def evaluate(self,X,Y):
        assert(Y.shape == (X.shape[0],))
        t = self.predict(X)
        n_right = np.sum( t == Y )
        accuracy = float(n_right)/t.size
        return accuracy


# the function that used to verify the results of qp solver
def verify(X,Y,w,b,ksi):
    n_sample = Y.size
    for i in range(n_sample):
        y_i = Y[i]
        x_i = X[i,:]
        val = y_i*(np.sum(w*x_i)+b) + ksi[i]
        if  val < 1:
            print("ERROR FIND :",val)
            exit(0)
    return 0


class SVMta():
    def __init__(self):
        self.clr = None

    def fit(self, X_t, Y_t, c):
        self.clr = SlackSVM().fit(X_t, Y_t, c)

    def predict(self, X_t, Y_t):
        return self.clr.evaluate(X_t, Y_t)