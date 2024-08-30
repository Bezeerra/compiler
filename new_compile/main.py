import os
import re
from pathlib import Path

from new_compile.grammar import create_grammar
from new_compile.ll_1_check import predict_algorithm, is_ll1


class token_sequence:
    def __init__(self, ts: list) -> None:
        self.__ts = ts
        self.__idx = 0

    def peek(self) -> str:
        return self.__ts[self.__idx]

    def advance(self) -> None:
        self.__idx = self.__idx + 1

    def match(self, token: str) -> None:
        if self.peek() == token:
            self.advance()
        else:
            print('Expected ', token)
            exit(0)


regex_table = {
    r'^let$': 'let',
    r'^f32$|^f32;$': 'floatcl',
    r'^i32$|^i32;$': 'intcl',
    r'^[a-zA-Z][a-zA-Z0-9]*:$': 'id',  # deveria ter um regex específico para pegar o :, pensar depois
    r'^=$': 'assign',
    r'^\+$': 'plus',
    r'^[0-9]+$': 'inum',
    r'^[0-9]+\.[0-9]+$': 'fnum'
}


def lexical_analyser(filepath) -> list:
    with open(filepath, 'r') as f:
        token_sequence = []
        tokens = []
        for line in f:
            tokens = tokens + line.split(' ')
        for t in tokens:
            t = t.strip()
            found = False
            for regex, category in regex_table.items():
                if re.match(regex, t):
                    token_sequence.append(category)
                    if t.endswith(':'):
                        token_sequence.append('colon')
                    elif t.endswith(';'):
                        token_sequence.append('semicolon')
                    found = True
            if not found:
                print('Lexical error: ', t)
                exit(0)
    token_sequence.append('$')
    return token_sequence

def main():
    # tokens = lexical_analyser(os.path.join(Path(__file__).parent, 'example.be'))
    # ts = token_sequence(tokens)
    G = create_grammar()
    p_alg = predict_algorithm(G)
    print(is_ll1(G, p_alg))


if __name__ == '__main__':
    main()
