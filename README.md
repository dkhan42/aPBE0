# aPBE0
ML model for predicting the optimal exact exachange ratio to be used in the PBE0 functional

Python libraries required : 
* Numpy
* Numba
* Joblib
* cMBDF (https://github.com/dkhan42/cMBDF)
* qml2 (https://github.com/dkhan42/qml2/tree/develop)
* Pyscf (only for the `get_atomization` function)

Usage :

```
from get_exchange import get_predictions
opt_exchange = get_predictions(charges, coords)
```
where `charges` and `coords` are arrays containing atomic numbers and atomic coordinates for each molecule

To obtain aPBE0 atomization energy for a molecule (in Hartree) with the predicted exact exchange :

```
from get_exchange import get_atomization
energy = get_atomization(elements, coords, opt_exchange, basis)
```

where `elements` is the array (strings) of chemical symbols in the molecule and `exchange` is the predicted exact exchange fraction 
