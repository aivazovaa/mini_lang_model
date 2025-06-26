import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import pickle

SEQ_LENGTH = 20
EMBEDDING_DIM = 128
RNN_UNITS = 256
BATCH_SIZE = 64
EPOCHS = 10

def load_data(file_path):
    programs, tokens = [], set()
    with open(file_path, 'r') as f:
        for line in f:
            tks = line.strip().split()
            programs.append(tks)
            tokens.update(tks)
    token_list = sorted(tokens)
    token_to_idx = {t: i+1 for i, t in enumerate(token_list)}
    idx_to_token = {i+1: t for i, t in enumerate(token_list)}
    vocab_size = len(token_to_idx) + 1

    sequences = [[token_to_idx[t] for t in prog] for prog in programs]
    padded = pad_sequences(sequences, maxlen=SEQ_LENGTH, padding='post', truncating='post')

    X, y = [], []
    for seq in padded:
        for i in range(1, len(seq)):
            X.append(seq[:i])
            y.append(seq[i])
    X = pad_sequences(X, maxlen=SEQ_LENGTH, padding='post', truncating='post')
    y = to_categorical(np.array(y), num_classes=vocab_size)
    return X, y, vocab_size, token_to_idx, idx_to_token

def build_model(vocab_size):
    model = models.Sequential([
        layers.Embedding(input_dim=vocab_size, output_dim=EMBEDDING_DIM),
        layers.LSTM(RNN_UNITS, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(RNN_UNITS),
        layers.Dropout(0.2),
        layers.Dense(vocab_size, activation='softmax')
    ])
    return model

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python train.py <data_file>")
        exit(1)
    data_file = sys.argv[1]
    X_train, y_train, vocab_size, token_to_idx, idx_to_token = load_data(data_file)
    model = build_model(vocab_size)
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_split=0.1)
    model.save('language_model.h5')
    with open('token_to_idx.pkl', 'wb') as f:
        pickle.dump(token_to_idx, f)
    with open('idx_to_token.pkl', 'wb') as f:
        pickle.dump(idx_to_token, f)
    print('Training complete.')