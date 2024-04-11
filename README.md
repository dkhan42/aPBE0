# aPBE0
CCSD(T) training data for the 1169 amons used to generate training labels is available in the `cc_train_data.npz` file.

Chemical symbols, coordinates, CCSD total energies, CCSD(T) total energies, CCSD(T) atomization energies (all in Hartree) for each molecule are available in the `elements`, `coordinates`, `eccsd`, `eccsdt`, `hccsdt` arrays respectively in the same order.

ML model for predicting the optimal exact exachange ratio to be used in the PBE0 functional

Python libraries required : 
* Numpy
* Numba
* Joblib
* Ase (if supplying xyz files)
* cMBDF (https://github.com/dkhan42/cMBDF)
* qml2 (https://github.com/dkhan42/qml2/tree/develop)
* Pyscf (only for the `get_atomization` function)


Usage :

```
from get_exchange import get_predictions
opt_exchange = get_predictions(charges, coords)
opt_exchange = get_predictions(xyz = 'mol.xyz') #if supplying xyz file instead
```
where `charges` and `coords` are arrays containing atomic numbers and atomic coordinates for each molecule

To obtain aPBE0 atomization energy for a molecule (in Hartree) with the predicted exact exchange :

```
from get_exchange import get_atomization
energy = get_atomization(elements, coords, opt_exchange, basis)
```

where `elements` is the array (strings) of chemical symbols in the molecule and `exchange` is the predicted exact exchange fraction 
