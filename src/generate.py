import sys
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import pickle
import re

SEQ_LENGTH = 20

def extract_tokens(lines):
    terms = set(['for','x','y','0','1','2','+','-','<','>','=','if','then','print','assign','<PAD>','<EOS>','<UNK>'])
    tokens = []
    for line in lines:
        parts = re.split(r"(\s+|\(|\)|:|,)", line)
        for p in parts:
            p = p.strip().lower()
            if not p:
                continue
            tokens.append(p if p in terms else '<UNK>')
    return tokens


def sample_with_temperature(preds, temperature=1.0):
    preds = np.log(preds + 1e-10) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)

def generate(prefix, model_path='language_model.h5', temperature=1.0):
    model = load_model(model_path, compile=False)
    with open('token_to_idx.pkl', 'rb') as f:
        token_to_idx = pickle.load(f)
    with open('idx_to_token.pkl', 'rb') as f:
        idx_to_token = pickle.load(f)
    current = prefix[:]
    generated = []
    for _ in range(SEQ_LENGTH):
        seq = [token_to_idx.get(t, token_to_idx.get('<UNK>', 0)) for t in current]
        padded = pad_sequences([seq], maxlen=SEQ_LENGTH, padding='post', truncating='post')
        preds = model.predict(padded, verbose=0)[0]
        next_idx = sample_with_temperature(preds, temperature)
        next_tok = idx_to_token.get(next_idx, '<UNK>')
        current.append(next_tok)
        generated.append(next_tok)
        if next_tok == '<EOS>':
            break
    return prefix, generated, current

if __name__ == '__main__':
    print("Interactive code generation. Type 'exit' to quit.")
    while True:
        print("\\nEnter partial code lines (empty line to finish):")
        lines = []
        while True:
            text = input()
            if text.lower() == "exit":
                print("Exiting.")
                sys.exit(0)
            if text == "":
                break
            lines.append(text)
        prefix = extract_tokens(lines)
        orig, gen_tokens, all_tokens = generate(prefix, temperature=0.8)
        code = ' '.join([t for t in all_tokens if t not in ['<PAD>', '<EOS>']])
        print("\\n--- Generation Result ---")
        print("Original tokens:", orig)
        print("Generated tokens:", gen_tokens)
        print("All tokens:", all_tokens)
        print("Generated code:", code)
