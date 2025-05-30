import numpy as np
from numba import njit
from scipy.linalg import cho_solve

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


def KRR_local(X_train,Q_train,Y_train,X_test,Q_test,kernel,best_params):
    """
    Returns the KRR predictions for local representations. Available options for the kernels are the local Gaussian, Laplacian, Exponential-Euclidean, Matern 3/2, Matern 5/2 kernels
     as implemented in the QML-code library.
    """
    sigma,lam = best_params['length'], best_params['lambda']
    if kernel in ['gaussian','rbf','Gaussian']:
        K=kernels.get_local_symmetric_kernel(X_train,Q_train,[sigma])
    elif kernel=='laplacian':
        K=kernels.get_local_symmetric_kernel_laplacian(X_train,Q_train,[sigma])
    elif kernel=='mbdf':
        K = kernels.get_local_symmetric_kernel_mbdf(X_train, Q_train, sigma)
    elif kernel == 'matern1':
        K = kernels.get_local_symmetric_kernel_matern(X_train, Q_train, sigma, order=1)
    elif kernel == 'matern2':
        K = kernels.get_local_symmetric_kernel_matern(X_train, Q_train, sigma, order=2)
    K = get
    #K=kernels.get_local_symmetric_kernel(X_train,Q_train,[sigma])
    K+=(np.eye(K.shape[0])*lam)
    try:
            L=np.linalg.cholesky(K)
    except:
        return 'Gram Matrix is not positive definite'
    else:
        try:
            alpha=cho_solve((L,True),Y_train)
        except:
            return 'Cholesky decomposition failed, check distance matrices'
        else:
            if kernel in ['gaussian','rbf','Gaussian']:
                k=kernels.get_local_kernels(X_train,X_test,Q_train,Q_test,[sigma]).T
            elif kernel=='laplacian':
                k=kernels.get_local_kernel_laplacian(X_train,X_test,Q_train,Q_test,[sigma]).T
            elif kernel=='mbdf':
                k = kernels.get_local_kernel_mbdf(X_train, X_test, Q_train, Q_test, sigma).T
            elif kernel == 'matern1':
                k = kernels.get_local_kernel_matern(X_train, X_test, Q_train, Q_test, sigma, order=1).T
            elif kernel=='matern2':
                k = kernels.get_local_kernel_matern(X_train, X_test, Q_train, Q_test, sigma, order=2).T
            return np.dot(k.T,alpha)