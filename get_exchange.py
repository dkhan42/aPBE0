import numpy as np
from qml.kernels import get_local_kernel
from cMBDF import generate_mbdf

def get_predictions(charges,coords):
    data = np.load('trained_model.npz', allow_pickle=True)
    xtrain, qtrain, alpha = data['xtrain'], data['qtrain'], data['alpha']
    rep = generate_mbdf(charges,coords,n_atm=2.0,pad=50)
    Ne = np.array([np.sum(arr) for arr in charges])
    k = get_local_kernel(xtrain,rep,qtrain,charges,1638.4).T
    return (np.dot(k.T,alpha)/Ne)/100
