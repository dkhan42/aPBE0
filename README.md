# aPBE0 
# `.xyz` files for all molecules from the QM5, QM9, QM7b, W4-17 datasets used for training and testing in the paper along with text files containing relevant aopt, apred, reference energies etc. are available in separate folders within the `train_test_data.tar.xz` file. Each folder for the dataset contains a `readme.txt` file explaining the reported data.
# The "qmspin" folder also contains the 4 carbene structures stores separately for which no aopt value could be obtained by optimizing the singlet states alone such that the MRCISD+Q gap could be recovered
# Text files containing predicted a value, aPBE0 energy, PBE0 energy, and mean absolute error (MAE) across all subsets from GMTKN55 reported in figure 3 are available in the `gmtkn55_data.tar.xz` file along with a 'readme.txt` description.

CCSD(T) training data for the 1169 amons used to generate training labels is available in the `cc_train_data.npz` file. Chemical symbols, coordinates, CCSD total energies, CCSD(T) total energies, CCSD(T) atomization energies (all in Hartree) for each molecule are available in the `elements`, `coordinates`, `eccsd`, `eccsdt`, `hccsdt` arrays respectively in the same order.

Spin gap test set used in figure 2 from the QMspin dataset is available in `qmspin_test_set.npz` along with MRCISD+Q spin gap energies.

HOMO-LUMO gap test set used in figure 3 from the QM7b dataset is available in `qm7b_test_set.npz` along with GW HOMO, LUMO and HOMO-LUMO gap eigenvalues.

All energies are reported in Hartrees.

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

# References
Please consider citing the following work :

Khan, D., Price, A. J. A., Ach, M. L., Trottier, O., & von Lilienfeld, O. A. (2024). Adaptive hybrid density functionals. arXiv preprint arXiv:2402.14793.

