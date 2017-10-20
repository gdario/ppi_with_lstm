from __future__ import absolute_import, division, print_function
import pandas as pd
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import h5py

maxlen = 500

dataset = pd.read_hdf(
    '/da/dmp/cb/dariogi1/projects/2017/squads/ppi_with_lstm/output/filtered_ppi_dataset_500.hdf5')

print('Fitting the tokenizer')
tokenizer = Tokenizer()
tokenizer.fit_on_texts(['l s a v g e p t r i k f d q n y m h c w'])

seq_indices1 = dataset.sequence1.apply(
    lambda x: [tokenizer.word_index[c.lower()] for c in x]
)
seq_indices2 = dataset.sequence2.apply(
    lambda x: [tokenizer.word_index[c.lower()] for c in x]
)

x1 = pad_sequences(seq_indices1.tolist(), maxlen=maxlen, value=-1)
x2 = pad_sequences(seq_indices2.tolist(), maxlen=maxlen, value=-1)
y = dataset.interaction.values

# Transform the indices in int32 for later use with one_hot
x1 = x1.astype('int32')
x2 = x2.astype('int32')

x1_train = x1[:-10000]
x2_train = x2[:-10000]
y_train = y[:-10000]

x1_test = x1[-10000:]
x2_test = x2[-10000:]
y_test = y[-10000:]


print('Saving the dataset')
with h5py.File(
        '/da/dmp/cb/dariogi1/projects/2017/squads/ppi_with_lstm/output/create_tokenized_dataset_500.hdf5', 'w') as f:

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
