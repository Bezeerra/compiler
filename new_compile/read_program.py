import re
from dataclasses import dataclass
from typing import Any


regex_table = {
    r'^[0-9]': 'num',
    r'^[0-9]+\.[0-9]+$': 'fnum',
    r'^f32$': 'f32',
    r'^let$': 'let',
    r'^i32$': 'i32',
   # r'^p$': 'print',
    r'^[a-z]+$' : 'id',
    r'^=$':'=',
    r'^\+$': '+',
    r'^\-$': '-',
    r'^;$': ';',
    r'^:$': ':',
}


@dataclass
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



def read_program(file_path: str) -> list[CategoryValue]:
    tokens = []
    token_sequence = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            split_line = line.split(" ")
            for token in split_line:
                if not token:
                    continue
                if token.endswith(':') or token.endswith(';'):
                    tokens.append(token[:-1])
                    tokens.append(token[-1])
                else:
                    tokens.append(token)
        for token in tokens:
            found = False
            for regex, category in regex_table.items():
                if re.match(regex, token):
                    token_sequence.append(CategoryValue(category, token))
                    found = True
                    break
            if not found:
                print('Lexical error: ', token)
                exit(0)
    token_sequence.append("$")
    return token_sequence


if __name__ == "__main__":
    read_program("code.rs")
