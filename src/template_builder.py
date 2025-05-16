def apply_template(seq):
    VALID = {'x', 'y', 'i', 'j'}

    def format_body(tokens, indent='    '):
        out = ''
        i = 0
        while i < len(tokens):
            cmd = tokens[i]
            if cmd == 'PRINT':
                var = tokens[i+1] if i+1 < len(tokens) and tokens[i+1] in VALID else 'x'
                out += f'{indent}print({var});\n'
                i += 2
            elif cmd == 'ASSIGN' and i+4 < len(tokens):
                dst, src, op, val = tokens[i+1:i+5]
                out += f'{indent}{dst} = {src} {op} {val};\n'
                i += 5
            else:
                i += 1
        return out

    if not seq:
        return '// empty'

    c = seq[0]

    if c == 'FOR':
        if len(seq) < 3:
            return '// incomplete FOR header'
        var = seq[1]
        start = seq[2]
        end = seq[3] if len(seq) > 3 else '10'
        body = seq[4:] if len(seq) > 4 else []
        return f'for(int {var}={start};{var}<{end};{var}++){{\n{format_body(body)}}}'

    elif c == 'IF':
        if len(seq) < 4:
            return '// incomplete IF condition'
        var = seq[1]
        comp = seq[2]
        val = seq[3]
        body = seq[4:] if len(seq) > 4 else []
        return f'if({var} {comp} {val}){{\n{format_body(body)}}}'

    elif c == 'ASSIGN':
        if len(seq) < 5:
            return '// incomplete ASSIGN statement'
        dst, src, op, val = seq[1:5]
        return f'{dst} = {src} {op} {val};'

    elif c == 'PRINT':
        if len(seq) < 2:
            return '// incomplete PRINT statement'
        return f'print({seq[1]});'

    return '// unknown'
