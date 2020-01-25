# START: Imports
import os
import time
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import CuDNNLSTM, Conv2D, BatchNormalization, Bidirectional, Dense, Dropout, Flatten, LeakyReLU, UpSampling2D, Activation
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from tqdm import tqdm
# END: Imports

# START: Pre-processing
# input data shape could be (batch_size, no_of_timesteps, no_of_notes_at_a_time)


# END: Pre - processing
# START: build dicriminator model
def disc_model(self):
    # Base model - Will change.
    model = Sequential()
    model.add(CuDNNLSTM(512, return_sequences=True))
    model.add(Dropout())

    model.add(Bidirectional())
    model.add(Dropout())

    model.add(Bidirectional())
    model.add(Dense())
    model.add(Dropout())
    model.add(Dense())
    model.add(Activation('softmax'))

    model.compile(loss=, optimizer='adam')
 
# END: build discriminator model

# build generator model
# compute loss
# predict