import random

def random_variable():
    return random.choice(['x', 'y'])

def random_constant():
    return random.choice(['0', '1', '2'])

def random_operator():
    return random.choice(['+', '-', '<', '>'])

def generate_operand():
    return random.choice([random_variable(), random_constant()])

def generate_expression(depth=0, max_depth=1):
    if depth >= max_depth or random.random() < 0.5:
        return [generate_operand()]
    else:
        return [generate_operand(), random_operator(), *generate_expression(depth+1, max_depth)]

def generate_condition():
    return [generate_operand(), random_operator(), generate_operand()]

def generate_block(depth=0, max_depth=2):
    # Block of one or multiple statements
    count = random.randint(1, 2)
    stmts = []
    for _ in range(count):
        stmts += generate_statement(depth+1, max_depth)
    return ['<PAD>'] + stmts

def generate_assignment():
    return ['assign', random_variable(), '=', *generate_expression()]

def generate_print_statement():
    return ['print', random.choice(['x', 'y', '0', '1', '2'])]

def generate_if_statement(depth=0, max_depth=2):
    return ['if', *generate_condition(), 'then'] + generate_block(depth, max_depth)

def generate_for_statement(depth=0, max_depth=2):
    return ['for', random_variable(), random_constant(), random_constant()] + generate_block(depth, max_depth)

def generate_statement(depth=0, max_depth=2):
    stmt_type = random.choice(['assign', 'print', 'if', 'for'])
    if stmt_type == 'assign':
        return generate_assignment()
    elif stmt_type == 'print':
        return generate_print_statement()
    elif stmt_type == 'if':
        return generate_if_statement(depth, max_depth)
    else:
        return generate_for_statement(depth, max_depth)

def generate_statement_list(depth=0, max_depth=2):
    stmts = generate_statement(depth, max_depth) + ['<EOS>']
    if random.random() < 0.5 and depth < max_depth:
        stmts += generate_statement(depth, max_depth) + ['<EOS>']
    return stmts

def generate_program(num_statements=1, max_depth=2):
    return generate_statement_list(0, max_depth)

def generate_dataset(num_samples, output_file, max_depth=2):
    with open(output_file, 'w') as f:
        for _ in range(num_samples):
            program = generate_program(max_depth=max_depth)
            f.write(' '.join(program) + '\n')

if __name__ == '__main__':
    generate_dataset(100000, 'data.txt')
    print('Generated 100000 samples to data.txt')
