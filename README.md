# aPBE0
ML model for predicting the optimal exact exachange ratio to be used in the PBE0 functional
Requirements : https://github.com/dkhan42/cMBDF

Usage :

```
from get_exchange import get_predictions
opt_exchange = get_predictions(charges, coords)
```

To obtain aPBE0 atomization energy for a molecule (in Hartree) with the predicted exact exchange :

```
from get_exchange import get_atomization
energy = get_atomization(elements, coords, opt_exchange, basis)
```

where `elements` is the array (strings) of chemical symbols in the molecule and `exchange` is the predicted exact exchange fraction 
