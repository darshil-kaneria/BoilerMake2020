# START: Imports
import os
import time
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import CuDNNLSTM, Conv2D, BatchNormalization, Bidirectional, Dense, Dropout, Flatten, LeakyReLU, UpSampling2D, Activation, Input, Reshape
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from tqdm import tqdm
from preprocess import *
# END: Imports

X_train, Y_train = preprocess()
seq_shape = (X_train.shape[0],X_train.shape[1], X_train.shape[2]) # CHANGE THIS IF SOMETHING IS WRONG
temp_shape = X_train.shape[1] * X_train.shape[2]
print(temp_shape)
print(X_train.shape[0])
print(X_train.shape[1])
print(X_train.shape[2])
class GAN():
    def __init__(self, rows):
        self.seq_length = rows
        self.seq_shape = (self.seq_length, 1)
        self.latent_dim = 1000
        self.disc_loss = []
        self.gen_loss =[]
        
        optimizer = Adam(0.0002, 0.5)

        # Build and compile the discriminator
        self.discriminator = self.disc_model()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        # Build the generator
        self.generator = self.gen_model()

        # The generator takes noise as input and generates note sequences
        z = Input(shape=(self.latent_dim,))
        generated_seq = self.generator(z)

        # For the combined model we will only train the generator
        self.discriminator.trainable = False

        # The discriminator takes generated images as input and determines validity
        validity = self.discriminator(generated_seq)

        # The combined model  (stacked generator and discriminator)
        # Trains the generator to fool the discriminator
        self.combined = Model(z, validity)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    # START: build dicriminator model
    def disc_model(seq_shape):
        # Base model - Will change.
        model = Sequential()
        model.add(CuDNNLSTM(512, return_sequences=True, input_shape = seq_shape))
        model.add(Bidirectional(LSTM(512)))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(256))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.summary()

        seq = Input(shape=self.seq_shape)
        validity = model(seq)
        return Model(seq, validity)
    # END: build discriminator model

    # START: build generator model
    def gen_model(seq_shape):
        model = Sequential()

        model.add(Dense(256, input_dim = self.latent_dim))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))

        # model.add(Dense(np.prod(seq_shape), activation='tanh'))
        model.add(Dense(np.prod(self.seq_shape), activation='tanh'))

        model.add(Reshape(self.seq_shape))

        noise = Input(shape=(seq_shape))
        seq = model(noise)

        return Model(noise, seq)
    # END: build generator model

    # START: train

    # generator = gen_model(seq_shape)
    # discriminator = disc_model(seq_shape)


    # def train(epochs, batch_size, sample_intervals):
    #     real = np.ones((batch_size, 1))
    #     fake = np.zeros((batch_size, 1))

    #     for epoch in range(epochs):
    #         #Train discriminator
    #         random_batch_index = np.random.randint(0, X_train.shape[0], batch_size)
    #         real_sequence = X_train[random_batch_index]
    #         # add some noise to prevent overfitting
    #         noise = np.random.normal(0,1,(batch_size, self.latent_dim))
    #         generated_sequence = generator.predict(noise)

    #         # Train the discriminator
    #         disc_loss_real = discriminator.train_on_batch(real_sequence, real)
    #         disc_loss_fake = discriminator.train_on_batch(generated_sequence, fake)

    #         disc_total_loss = 0.5 * (disc_loss_real + disc_loss_fake)

    #         # Train the generator
    #         noise = np.random.normal(0,1, (batch_size, 1000))
    #         gen_loss = generator.train_on_batch(noise, real)
    def generate(self, input_notes):
        # Get pitch names and store in a dictionary
        notes = input_notes
        pitchnames = sorted(set(item for item in notes))
        int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
        
        # Use random noise to generate sequences
        noise = np.random.normal(0, 1, (1, self.latent_dim))
        predictions = self.generator.predict(noise)
        
        pred_notes = [x*(n_vocab)+() for x in predictions[0]]
        pred_notes = [int_to_note[int(x)] for x in pred_notes]
        
        create_midi(pred_notes, 'gan_final')
    def train(self, epochs, batch_size=128, sample_interval=50):

        # Load and convert the data
        notes = get_notes()
        n_vocab = len(set(notes))
        X_train, y_train = prepare_sequences(notes, n_vocab)

        # Adversarial ground truths
        real = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        
        # Training the model
        for epoch in range(epochs):

            # Training the discriminator
            # Select a random batch of note sequences
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            real_seqs = X_train[idx]

            #noise = np.random.choice(range(484), (batch_size, self.latent_dim))
            #noise = (noise-242)/242
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))

            # Generate a batch of new note sequences
            gen_seqs = self.generator.predict(noise)

            # Train the discriminator
            d_loss_real = self.discriminator.train_on_batch(real_seqs, real)
            d_loss_fake = self.discriminator.train_on_batch(gen_seqs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)


            #  Training the Generator
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))

            # Train the generator (to have the discriminator label samples as real)
            g_loss = self.combined.train_on_batch(noise, real)

            # Print the progress and save into loss lists
            if epoch % sample_interval == 0:
              print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))
              self.disc_loss.append(d_loss[0])
              self.gen_loss.append(g_loss)

if __name__ == "__main__":      
    gan = GAN(rows=100)    
    gan.train(epochs=5000, batch_size=32, sample_interval=1)

    # END: train


    # predict