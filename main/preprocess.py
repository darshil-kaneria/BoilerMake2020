import numpy as np
import os
import time
import tqdm as tqdm
import matplotlib.pyplot as plt
from music21 import converter, instrument, note, chord
import glob
import keras
import operator

def preprocess():

    notes = []
    midi = None

    data_path = "D:\\Work\\College\\Spring 2020\\gan-dataset\\midi-data\\midi_songs"
    for file in glob.glob(os.path.join(data_path, "*.mid")):
        
        midi = converter.parse(file)
        notes_to_parse = None

        parts = instrument.partitionByInstrument(midi)
        # print(parts.parts[0])
        if parts: # file has instrument parts
            notes_to_parse = parts.parts[0].recurse()
        else: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes
        # print(file)
        # if(len(notes_to_parse) > max_notes_to_parse):
        #     max_notes_to_parse = len(notes_to_parse)

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
            # print(notes)

    # print(len(notes))
    sequence_length = 100   # get all pitch names
    pitchnames = sorted(set(item for item in notes))    # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    max_notes = max(note_to_int.items(), key=operator.itemgetter(1))[1]
    network_input = []
    network_output = [] 
    # create input sequences and the corresponding outputs

    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape to LSTM compatible format
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))

    # normalize input
    network_input = network_input / float(max_notes)
    network_output = keras.utils.np_utils.to_categorical(network_output)
    print(network_input[0])
    return network_input, network_output