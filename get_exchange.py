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

def get_atomization(elements, coords, exchange, basis='cc-pvtz'):
    from pyscf import gto, dft
    a = exchange

    HF_X = a
    GGA_X = 1.0 - a
    atom_energies = {}
    elems = ['H', 'C', 'N', 'O', 'F']
    element_spins = {'H': 1, 'C': 2, 'N': 3, 'O': 2, 'F': 1}
    for element in elems:
        alpha = element_spins[element]
        mol = gto.M(atom=f'{element} 0 0 0', basis=basis, spin=(alpha), verbose=False)
        mf = dft.UKS(mol)
        mf.xc = f'{HF_X:} * HF + {GGA_X:} * GGA_X_PBE + GGA_C_PBE'
        energy = mf.kernel()
        atom_energies[element] = energy
    

    atoms = [[elements[i], coords[i]] for i in range(len(elements))]

    mol = gto.M(verbose=False)
    mol.atom = atoms
    mol.basis = basis
    mol.build()
    mol_hf = dft.RKS(mol)
    mol_hf.xc = f'{HF_X:} * HF + {GGA_X:} * GGA_X_PBE + GGA_C_PBE'
    e = mol_hf.kernel()

    for atom in elements:
        e-=atom_energies[atom]
    
    return e
