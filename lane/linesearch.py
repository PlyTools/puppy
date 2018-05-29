import numpy as np
import pandas as pd
import os.path
import scipy
import math
import cv2
import sys
import time
import re


def func(p, img, refPos):
    a,b,c,d = p
    tmpVar1 = ((refPos[0]-d)-c)
    tmpVar2 = ((refPos[0]-d)+c)

    y = np.arange(200)
    A =  a
    B =  (b-2*a*tmpVar1)
    C =  (a*tmpVar1**2.0 - b*(tmpVar1) + refPos[1] -y)
    BB = (b-2*a*tmpVar2)
    CC = (a*tmpVar2**2.0 - b*(tmpVar2) + refPos[1] -y)

    core = B**2-4*A*C
    y = y[core >= 0]

    core = core[core >= 0]
    x11 = ((-B + np.sqrt(core)) / (2*A)).astype(int)
    x12 = ((-B - np.sqrt(core)) / (2*A)).astype(int)
    x21 = ((-BB + np.sqrt(core)) / (2*A)).astype(int)
    x22 = ((-BB - np.sqrt(core)) / (2*A)).astype(int)


    return [x11, x12, x21, x22, y]


def loss(p, img, refPos):
    x11, x12, x21, x22, y = func(p, img, refPos)
    idx1 = filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x11, y]).reshape(-1,2, order='F'))
    idx2 = filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x12, y]).reshape(-1,2, order='F'))
    idx3 = filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x21, y]).reshape(-1,2, order='F'))
    idx4 = filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x22, y]).reshape(-1,2, order='F'))
    Idx = np.array(list(idx1) + list(idx2) + list(idx3) + list(idx4))
    Idxnear = Idx[Idx[:,1] > 170]
    return np.sum(img[Idx[:,1], Idx[:,0]]>0) + 10* np.sum(img[Idxnear[:,1], Idxnear[:,0]]>0)


def getBestParams(img, params, refPos):
    la,lb,lc,ld = params
    l_loss = []
    l_param = []
    for aa in la:
        for bb in lb:
            for cc in lc:
                for dd in ld:
                    pp = [aa,bb,cc,dd]
                    l = loss(pp, img, refPos)
                    l_param.append(pp)
                    l_loss.append(l)

    np_params = np.array(l_param)
    l_best = pd.DataFrame({
           "Loss" : np.array(l_loss),
              "A" : np_params[:,0],
              "B" : np_params[:,1],
              "C" : np_params[:,2],
              "D" : np_params[:,3]  }
    ).sort_values(['Loss'], ascending=False).iloc[0].values
    return func(l_best[0:4], img, refPos), l_best


def PrevFilter(d, l_errors):
    if len(l_errors)==0:
        return d
    else:
        return d*0.5 + np.array(l_errors[-1]*0.5).mean()