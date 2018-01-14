import numpy as np

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
    idx1 = list(filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x11, y]).reshape(-1,2, order='F')))
    idx2 = list(filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x12, y]).reshape(-1,2, order='F')))
    idx3 = list(filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x21, y]).reshape(-1,2, order='F')))
    idx4 = list(filter(lambda x: x[0]<100 and x[0]>0, np.concatenate([x22, y]).reshape(-1,2, order='F')))
    Idx = np.array(idx1 + idx2 + idx3 + idx4)
    Idxnear = Idx[Idx[:,1] > 150]
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
    
    
    


def binImgError(binarizedImg_t, initParams, refPos):
    paramSearch = None
    seedParams = []
    paramSearch = initParams
    '''
    if len(seedParams) == 0:
        paramSearch = initParams
    else:
        lla = np.linspace(seedParams[0]-(initParams[0][1]-initParams[0][0]),
                          seedParams[0]+(initParams[0][1]-initParams[0][0]), 3)
        llb = np.linspace(seedParams[1]-(initParams[1][1]-initParams[1][0]),
                          seedParams[1]+(initParams[1][1]-initParams[1][0]), 3)
        llc = np.arange(seedParams[2]-2, seedParams[2]+3, 2)
        lld = np.arange(seedParams[3]-1, seedParams[3]+2)
        paramSearch = [lla, llb, llc, lld]
    '''
    
    coords,params = getBestParams(binarizedImg_t, paramSearch, refPos)
    score = params[4]
    return params
    '''
    if score < 50:
        print("Frame %d score is %f, too low." % (i,score))
        seedParams = []
        prevVal = 0
        if len(l_errors)>0:
            prevVal = l_errors[-1]
        l_errors.append(prevVal)

    else:
        d = params[3]
        seedParams = params
        d = PrevFilter(d, l_errors)
        l_errors.append(d)
    '''
    
def getLines(params, refPos):
    tmpVar1 = ((refPos[0]-params[3])-params[2])
    tmpVar2 = ((refPos[0]-params[3])+params[2])
    y = np.linspace(0,200,40)
    A = params[0]
    B = (params[1]-2*params[0]*tmpVar1)
    C = (params[0]*tmpVar1**2-params[1]*tmpVar1+refPos[1]-y)
    BB = (params[1]-2*params[0]*tmpVar2)
    CC = (params[0]*tmpVar2**2-params[1]*tmpVar2+refPos[1]-y)

    core =B**2-4*A*C
    y = y[core>=0]
    core = core[core>0]
    x11 = (-B+np.sqrt(core))/ (2*A)
    x12 = (-B-np.sqrt(core))/ (2*A)
    x21 = (-BB+np.sqrt(core))/ (2*A)
    x22 = (-BB-np.sqrt(core))/ (2*A)
    return x11,x12,x21,x22,y

def PrevFilter(d, l_errors):
    if len(l_errors)==0:
        return d

    else:
        return d*0.7 + np.array(l_errors[-1]*0.3).mean()
