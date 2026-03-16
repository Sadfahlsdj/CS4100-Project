import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from itertools import chain
from torch.utils.data import TensorDataset, DataLoader
import os


# take in data, process it
def prepare_data(filepath, seq_length=10):
    processed_path = 'data/chord_bases_processed.pt'  # checkpointing
    if os.path.exists(processed_path):
        print(f"--- Loading existing pre-processed data from {processed_path} ---")
        checkpoint = torch.load(processed_path)
        return (checkpoint['X'], checkpoint['y'], checkpoint['vocab'],
                checkpoint['c2i'], checkpoint['i2c'])

    with open(filepath) as f:
        valid_chords = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii',
                        'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        chords = list(chain(*[[c for c in l.strip().split() if c in valid_chords] for l in f.readlines()]))

    vocab = sorted(list(set(chords)))
    chord_to_int = {c: i for i, c in enumerate(vocab)}
    int_to_chord = {i: c for i, c in enumerate(vocab)}

    # runtime sucks if i use the whole dataset (len around 11mil)
    full_data = torch.LongTensor([chord_to_int[c] for c in chords])[:500000]
    X = full_data.unfold(0, seq_length, 1)[:-1]
    y = full_data[seq_length:]

    torch.save({  # save to file
        'X': X,
        'y': y,
        'vocab': vocab,
        'c2i': chord_to_int,
        'i2c': int_to_chord
    }, 'data/chord_bases_processed.pt')

    return X, y, vocab, chord_to_int, int_to_chord


# actual model
class ChordLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super(ChordLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # batch_first=True means input shape is (batch, seq, feature)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, num_layers=2)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, (_, __) = self.lstm(embedded)
        # forward step
        last_time_step = lstm_out[:, -1, :]
        out = self.fc(self.dropout(last_time_step))
        return out
