from __future__ import absolute_import, division, print_function
import pandas as pd
import h5py
import os

maxlen = 500

ppi_path = '/lustre/scratch/dariogi1/ppi_with_lstm'

# Dataset containing the normalized protein fingerprints for all the proteins
# in Florian's dataset.
norm_prot_fps = pd.read_hdf(
    os.path.join(ppi_path, 'output/normalized_protein_fp.hdf5')
)

# Dataset containing the protein ID and the sequence for the pairs that pass
# the filtering, i.e., which have a length between 5 and 500 and without 'U's.
filtered_pairs = pd.read_hdf(
    os.path.join(ppi_path, 'output/filtered_ppi_dataset_500.hdf5')
)

x1 = norm_prot_fps.loc[filtered_pairs.uid1].values
x2 = norm_prot_fps.loc[filtered_pairs.uid2].values
y = filtered_pairs.interaction.values

x1_train = x1[:-10000]
x2_train = x2[:-10000]
y_train = y[:-10000]

x1_test = x1[-10000:]
x2_test = x2[-10000:]
y_test = y[-10000:]

print('Saving the dataset')
with h5py.File(
        os.path.join(ppi_path, 'output/create_protein_fp_dataset_500.hdf5'),
    'w') as f:

    x1_tr = f.create_dataset('train/x1', x1_train.shape, dtype=x1.dtype,
                             compression='gzip')
    x2_tr = f.create_dataset('train/x2', x2_train.shape, dtype=x2.dtype,
                             compression='gzip')
    y_tr = f.create_dataset('train/y', y_train.shape, dtype=y.dtype,
                            compression='gzip')
    x1_tr[...] = x1_train
    x2_tr[...] = x2_train
    y_tr[...] = y_train

    x1_te = f.create_dataset('test/x1', x1_test.shape, dtype=x1.dtype,
                             compression='gzip')
    x2_te = f.create_dataset('test/x2', x2_test.shape, dtype=x2.dtype,
                             compression='gzip')
    y_te = f.create_dataset('test/y', y_test.shape, dtype=y.dtype,
                            compression='gzip')
    x1_te[...] = x1_test
    x2_te[...] = x2_test
    y_te[...] = y_test
