import h5py
import os
from create_models import cnn_model
import argparse
from keras.callbacks import ModelCheckpoint, EarlyStopping

parser = argparse.ArgumentParser()
parser.add_argument('maxlen', help='maximum protein length', type=int)
parser.add_argument('ppi_path', help='path to the main folder', type=str)
args = parser.parse_args()

sequence_length = args.maxlen
ppi_path = args.ppi_path
batch_size = 128

model = cnn_model(conv_layers=2, filters=64, size_kernel=12,
                  pooling_multiplier=0.3, global_pooling=True,
                  learning_rate=0.001, hidden_layers=2, units=256,
                  dropout=0.5, sequence_length=sequence_length,
                  embedding_dim=20)

callback = [ModelCheckpoint(
    filepath=os.path.join(ppi_path, 'models/best_cnn_model'),
    monitor='val_acc',
    save_best_only=True),
    EarlyStopping(monitor='val_acc', patience=10)]

data_file = os.path.join(
    ppi_path, '_'.join(['output/create_tokenized_dataset',
                        str(sequence_length), '.hdf5'])
)

with h5py.File(data_file, 'r') as f:
    x1_tr, x2_tr, y_tr = (f['train/x1'], f['train/x2'], f['train/y'])
    x1_val, x2_val, y_val = (f['val/x1'], f['val/x2'], f['val/y'])
    x1_te, x2_te, y_te = (f['test/x1'], f['test/x2'], f['test/y'])

    model.fit([x1_tr, x2_tr], y_tr,
              batch_size=batch_size,
              epochs=100,
              shuffle=False,
              callbacks=callback,
              validation_data=([x1_val, x2_val], y_val))
