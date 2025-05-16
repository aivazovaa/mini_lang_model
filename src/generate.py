import torch
from vocab import VOCAB, INV_VOCAB

VALID_VARS = ['x', 'y', 'i', 'j']
VALID_VALS = VALID_VARS + ['0', '1', '2', '5', '10']

EXPECTED_NEXT = {
    'FOR': VALID_VARS,
    'IF': VALID_VARS,
    'ASSIGN': VALID_VARS,
    '==': VALID_VALS,
    '!=': VALID_VALS,
    '<': VALID_VALS,
    '>': VALID_VALS,
    '<=': VALID_VALS,
    '>=': VALID_VALS,
    '+': VALID_VALS,
    '-': VALID_VALS,
    'PRINT': VALID_VARS,
    'THEN': ['PRINT', 'ASSIGN']
}

def generate(model, prompt, max_len=5, temperature=1.0):
    model.eval()
    ids = [VOCAB.get(tok, VOCAB['<UNK>']) for tok in prompt]
    res = ids.copy()

    for _ in range(max_len):
        inp = torch.tensor([res], dtype=torch.long)
        with torch.no_grad():
            logits = model(inp)
        probs = torch.softmax(logits[0] / temperature, dim=-1)

        # Фильтрация
        mask = torch.ones_like(probs)
        if res:
            prev_tok = INV_VOCAB[res[-1]]
            allowed = EXPECTED_NEXT.get(prev_tok, None)
            if allowed:
                for idx in range(len(probs)):
                    tok = INV_VOCAB.get(idx, '<UNK>')
                    if tok not in allowed:
                        mask[idx] = 0
                if mask.sum() == 0:
                    mask = torch.ones_like(probs)
                probs *= mask
                probs /= probs.sum()

        next_id = torch.multinomial(probs, 1).item()
        if next_id == VOCAB['<EOS>']:
            break
        res.append(next_id)

    return [INV_VOCAB[i] for i in res[len(ids):]]
