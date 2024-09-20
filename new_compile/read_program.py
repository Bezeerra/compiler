import re

class CategoryValue:
    def __init__(self, category, value):
        self.category = category
        self.value = value

    def __getattr__(self, name):
        if name == 'category':
            return self.category
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __iter__(self):
        yield self.category

    def __str__(self):
        return self.category

    def __repr__(self):
        return self.category

    def __eq__(self, other):
        if isinstance(other, CategoryValue):
            return self.category == other.category
        else:
            return self.category == other

    def __hash__(self):
        return hash(self.category)


# Passo 1: Atualizar o regex_table com os novos operadores
regex_table = [
    # Palavras-chave
    (r'^func$', 'func'),
    (r'^return$', 'return'),
    (r'^,$', ','),
    (r'^let$', 'let'),  # Palavra-chave let
    (r'^i32$', 'i32'),  # Tipo i32
    (r'^f32$', 'f32'),  # Tipo f32
    (r'^while$', 'while'),  # Palavra-chave while
    (r'^endwhile$', 'endwhile'),  # Palavra-chave endif
    (r'^if$', 'if'),  # Palavra-chave if
    (r'^else$', 'else'),  # Palavra-chave else
    (r'^endif$', 'endif'),  # Palavra-chave endif
    (r'^print$', 'print'),  # Palavra-chave print
    (r'^"[A-Za-z_][A-Za-z0-9_]*"$', '"string"'),

    # Números e identificadores
    (r'^\d+\.\d+$', 'fnum'),
    (r'^\d+$', 'num'),
    (r'^[A-Za-z_][A-Za-z0-9_]*$', 'id'),

    (r'^[A-Za-z_][A-Za-z0-9_]*$', 'func_name'),  # Palavra-chave endif
    # Operadores relacionais e de igualdade (padrões mais longos primeiro)
    (r'^>=$', '>='),
    (r'^<=$', '<='),
    (r'^!=$', '!='),
    (r'^==$', '=='),
    (r'^>$', '>'),
    (r'^<$', '<'),

    # Operadores aritméticos e outros símbolos
    (r'^\+$', '+'),
    (r'^\-$', '-'),
    (r'^\*$', '*'),
    (r'^=$', '='),
    (r'^;$', ';'),
    (r'^:$', ':'),
    (r'^\($', '('),
    (r'^\)$', ')'),
    (r'^\{$', '{'),
    (r'^\}$', '}'),

]

def make_group_name(category):
    replacements = {
        '>=': 'GE',
        '<=': 'LE',
        '!=': 'NE',
        '==': 'EQ',
        '>': 'GT',
        '<': 'LT',
        '=': 'ASSIGN',
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'MULTIPLY',
        '\\': 'BACKSLASH',
        ';': 'SEMICOLON',
        ':': 'COLON',
        '(': 'LPAREN',
        ')': 'RPAREN',
        '{': 'LBRACE',
        '}': 'RBRACE',
    }
    if category in replacements:
        return replacements[category]
    else:
        return re.sub(r'\W', '_', category)

def read_program(file_path: str) -> list[CategoryValue]:
    group_names = {}
    token_specification = []
    for regex, category in regex_table:
        adjusted_regex = regex.strip('^$')
        group_name = make_group_name(category)
        # Garantir que o nome do grupo seja único
        if group_name in group_names:
            count = 1
            new_group_name = f"{group_name}_{count}"
            while new_group_name in group_names:
                count += 1
                new_group_name = f"{group_name}_{count}"
            group_name = new_group_name
        group_names[group_name] = category
        token_specification.append((group_name, adjusted_regex))

    token_specification.extend([
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('COMMENT', r'//.*'),
        ('MISMATCH', r'.'),
    ])

    group_names.update({
        'NEWLINE': 'NEWLINE',
        'SKIP': 'SKIP',
        'COMMENT': 'COMMENT',
        'MISMATCH': 'MISMATCH',
    })

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []

    with open(file_path, 'r') as f:
        code = f.read()

    get_token = re.compile(tok_regex).match
    pos = 0
    line = 1
    while pos < len(code):
        mo = get_token(code, pos)
        if not mo:
            print(f'Erro léxico: {code[pos]!r} na linha {line}')
            exit(0)
        kind = mo.lastgroup
        category = group_names[kind]
        value = mo.group(kind)
        if kind == "id" and get_token(code, mo.span()[1]).group() == '(':
            category = 'func_name'
        if category == 'NEWLINE':
            line += 1
        elif category in ('SKIP', 'COMMENT'):
            pass  # Ignorar espaços em branco e comentários
        elif category == 'MISMATCH':
            print(f'Erro léxico: {value!r} na linha {line}')
            exit(0)
        else:
            tokens.append(CategoryValue(category=category, value=value))
        pos = mo.end()
    tokens.append(CategoryValue(category="$", value="$"))  # Símbolo de fim de entrada
    return tokens

if __name__ == "__main__":
    print(read_program("code.rs"))
