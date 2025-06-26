from tensorflow.keras import layers, models

def build_model(vocab_size, embedding_dim=128, rnn_units=256):
    model = models.Sequential([
        layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim),
        layers.LSTM(rnn_units, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(rnn_units),
        layers.Dropout(0.2),
        layers.Dense(vocab_size, activation='softmax')
    ])
    return model