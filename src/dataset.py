import random
from vocab import VOCAB
import torch

def generate_example():
    templates = []

    for var in ['i', 'j']:
        for start in ['0', '1']:
            for end in ['5', '10']:
                templates.append(['FOR', var, start, end, 'PRINT', var])

    for var in ['x', 'y', 'i', 'j']:
        for comp in ['<', '>', '<=', '>=', '==', '!=']:
            for val in ['0', '1', '5', '10']:
                templates.append(['IF', var, comp, val, 'THEN', 'PRINT', var])

    for dst in ['x', 'y']:
        for src in ['x', 'y', 'i', 'j']:
            for op in ['+', '-']:
                for val in ['1', '2', '5', 'x', 'y', 'i', 'j']:
                    templates.append(['ASSIGN', dst, src, op, val])

    for var in ['x', 'y', 'i', 'j']:
        templates.append(['PRINT', var])

    return random.choice(templates)

def encode(tokens):
    return [VOCAB.get(tok, VOCAB['<UNK>']) for tok in tokens + ['<EOS>']]

def create_dataset(n=20000):
    sequences = [generate_example() for _ in range(n)]
    X, Y = [], []

    for seq in sequences:
        if seq[0] in ['FOR']:
            prompt = seq[:4]     # ['FOR', var, start, end]
            cont = seq[4:]
        elif seq[0] in ['IF']:
            then_index = seq.index('THEN')
            prompt = seq[:then_index]  # ['IF', var, comp, val]
            cont = seq[then_index+1:]
        else:
            prompt = seq[:1]     # 'PRINT', 'ASSIGN'
            cont = seq[1:]

        if not cont or len(cont) < 2:
            continue

        enc_prompt = encode(prompt)
        enc_cont = encode(cont)
        for i in range(1, len(enc_cont)):
            X.append(torch.tensor(enc_prompt + enc_cont[:i]))
            Y.append(torch.tensor(enc_cont[i]))

    return X, Y
