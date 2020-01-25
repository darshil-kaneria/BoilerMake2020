# START: Imports
import os
import time
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Conv2D, BatchNormalization, Bidirectional, Dense, Dropout, Flatten, LeakyReLU, UpSampling2D, Activation, Input, Reshape
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from tqdm import tqdm
# END: Imports

# START: build dicriminator model
def disc_model(seq_shape):
    # Base model - Will change.
    model = Sequential()
    model.add(LSTM(512, return_sequences=True, input_shape = seq_shape))
    model.add(Bidirectional(LSTM(512)))
    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(256))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(1, activation='sigmoid'))
    model.summary()

    seq = Input(self.seq_shape)
    validity = model(seq)
    return Model(seq, validity)
# END: build discriminator model

# START: build generator model
def gen_model(seq_shape):
    model = Sequential()

    model.add(Dense(256, input_dim = 1000))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))

    model.add(Dense(512))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))

    model.add(Dense(1024))
    model.add(LeakyReLU(alpha=0.2))
    model.add(BatchNormalization(momentum=0.8))

    model.add(Dense(np.prod(seq_shape), activation='tanh'))
    model.add(Reshape(seq_shape))

    noise = Input(shape=seq_shape)
    seq = model(noise)

    return Model(noise, seq)
# END: build generator model

# compute loss

# predict