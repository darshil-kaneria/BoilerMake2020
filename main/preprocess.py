import numpy as np
import os
import time
import tqdm as tqdm
import matplotlib.pyplot as plt
from music21 import converter, instrument, note, chord
import glob

notes = []
midi = None
data_path = "D:\\Work\\College\\Spring 2020\\gan-dataset\\midi-data\\midi_songs"
for file in glob.glob(os.path.join(data_path, "*.mid")):
    
    midi = converter.parse(file)
    notes_to_parse = None

    parts = instrument.partitionByInstrument(midi)
    if parts: # file has instrument parts
        notes_to_parse = parts.parts[0].recurse()
    else: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes
    # print(file)

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
        # print(notes)
    
        