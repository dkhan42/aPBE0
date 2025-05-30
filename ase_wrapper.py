import numpy as np
from ase.io import read
from cMBDF import generate_mbdf
from numba import njit
from scipy.linalg import cho_solve
from joblib import Parallel, delayed

data = np.load('model.npz', allow_pickle=True)
convs = (data['rconvs'], data['aconvs'])
xtrain, qtrain, alpha, sigma = data[f'xtrain'], data[f'qtrain'], data[f'alpha'], data[f'sigma']
L = data[f'L']


@njit(parallel = True)
def local_kernel(A, B, Q1, Q2, sigma):
    n1, n2 = len(Q1), len(Q2)
    K=0
    for i in range(n1):
            k=0
            for j in range(n2):
                q1, q2 = Q1[i], Q2[j]

                if q1==q2:
                    dist = np.linalg.norm(A[i]-B[j])**2
                    k += np.exp(-dist/(2*(sigma)**2))
            K += k
    return K


def get_kernel(X1, X2, q1, q2, sigma):
    K = Parallel(n_jobs=-1)(delayed(local_kernel)(X1[i], X2, q1[i], q2, sigma) for i in range(len(q1)))
    return np.array(K)


def return_prediction(xyz, x0 = 0.7):
    '''
    Returns the predicted exact-exchange admixture fraction for aPBE0.
    inputs : 
    xyz : xyz file of the molecule
    x0 : model uncertainty threshold for reduction to default PBE0 (0.25 exact-exchange fraction)

    output : predicted exact-exchange fraction modulated by model uncertainty (scalar) 
    '''
    Atoms = read(xyz)
    charges = Atoms.get_atomic_numbers()
    coords = Atoms.get_positions()

    with open(xyz, 'r') as f:
        lines = f.readlines()
        comment_line = lines[1].strip()
        charge, multiplicity = map(int, comment_line.split()[:2]) #reading molecular charge, multiplicity

    if len(charges)>1:
        rep = generate_mbdf(np.array([charges]),np.array([coords]),convs,n_atm=2.0,pad=100)[0]
        Ne = np.sum(charges)
        Ne-=charge

        k = get_kernel(xtrain, rep, qtrain, charges, sigma) #query kernel
        sk = local_kernel(rep, rep, charges, charges, sigma) #self-kernel

        #calculating uncertainty
        alpha2 = cho_solve((L,True),k) 
        variance = (sk - np.dot(k,alpha2))
        unc = 1 - (variance/sk)
        cutoff = 1-(0.5 * (1 + np.tanh(5000 * (unc - x0))))

        #predicted deviation from PBE0 fraction (0.25)
        pred = (np.dot(k,alpha)/Ne)/100

        return 0.25 + (cutoff*pred)
    else:
        return 0.25 #if only one atom is present, return default PBE0 fraction
