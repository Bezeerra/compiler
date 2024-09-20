import os
import re
from pathlib import Path
from tokenize import Token

# from userpath.cli import append

from abstract_syntax_tree_math import generate_sam_math_code
from abstract_syntax_tree_logical import generate_sam_logical_code
from Tokenize_code import TokenVariable, TokenAddressMemory
from constants import LOGICAL_OPERATIONS
from grammar import create_grammar
from ll_1_check import predict_algorithm, is_ll1


class token_sequence:
    def __init__(self, ts: list, produce) -> None:
        self.__ts = ts
        self.produce = produce
        self.__idx = 0

    def peek(self) -> TokenVariable:
        return self.__ts[self.__idx]

    def advance(self) -> None:
        self.__idx = self.__idx + 1

    def logical_sam_code(self, stop_token: TokenVariable):
        if self.produce.start_while_logical_operation:
            self.produce.in_context.append("while")
            self.produce.while_context += 1
            self.produce.functions.append(f"WHILE{self.produce.while_context}:")
        else:
            self.produce.in_context.append("if")
        functions = generate_sam_logical_code(" ".join([t.value for t in self.produce.logical_expression]).strip(), self.produce.full_table)
        self.produce.functions.extend(functions)
        self.produce.logical_expression= []
        if self.produce.start_while_logical_operation and stop_token.value == "{":
            self.produce.functions.append(f"JUMPC ENDWHILE{self.produce.while_context}")
        if self.produce.start_if_logical_operation and stop_token.value == "{":
            self.produce.functions.append(f"JUMPC ELSE{self.produce.if_context}")
            self.produce.if_context += 1
        self.produce.start_if_logical_operation = False
        self.produce.start_while_logical_operation = False

    def math_sam_code(self):
        functions = generate_sam_math_code(
            " ".join([t.value for t in self.produce.math_expression]).strip(), self.produce.full_table
        )
        self.produce.functions.extend(functions)
        if address := self.produce.full_table.get(self.produce.variable):
            address_memory = address
        else:
            address_memory = self.produce.get_address_memory()
        self.produce.functions.append(f"STOREABS {address_memory}")
        self.produce.full_table[self.produce.variable] = address_memory
        self.produce.math_expression = []
        self.produce.variable = None
        self.produce.start_set_value = False


    def build_operations(self, token: TokenVariable):
        if token.value == "func":
            self.produce.start_func_context = token.value
            self.produce.start_produce_index_func = len(self.produce.functions) - 1
        if token.value == "return" and self.produce.start_func_context:
            aux = []
            aux.extend(self.produce.functions[self.produce.start_produce_index_func:])
            self.produce.functions = self.produce.functions[:self.produce.start_produce_index_func]
            self.produce.functions.extend(aux)
            self.produce.start_produce_index_func = None
        if  self.produce.else_context > 0 and token.value == '}':
            self.produce.functions.append(f"ENDIF{self.produce.if_context}:")
            self.produce.else_context+= -1
        elif self.produce.in_context and (self.produce.in_context[-1] == 'if' and  self.produce.if_context > 0 and token.value == '}'):
            self.produce.if_context -= 1
            self.produce.in_context.pop()
            self.produce.functions.append(f"JUMP ENDIF{self.produce.if_context}")
            self.produce.functions.append(f"ELSE{self.produce.if_context}:")
            if self.__ts[self.__idx+1].value == "else":
                self.produce.else_context = 1
            else:
                self.produce.functions.append(f"PUSHIMM 0")
                self.produce.functions.append(f"ADDSP -1")
                self.produce.functions.append(f"ENDIF{self.produce.if_context}:")
                if self.__ts[self.__idx+1].value == "endif":
                    self.produce.functions.append(f"PUSHIMM 0")
                    self.produce.functions.append(f"ADDSP -1")
        elif self.produce.in_context and (self.produce.in_context[-1] == "while" and self.produce.while_context > 0 and token.value == "}"):
            self.produce.in_context.pop()
            self.produce.functions.append(f"JUMP WHILE{self.produce.while_context}")
            self.produce.functions.append(f"ENDWHILE{self.produce.while_context}:")
            self.produce.while_context -= 1

        if token.category == "id" and self.__ts[self.__idx+1].value != '(':
            if not self.produce.full_table.get(token.value):
                self.produce.full_table[token.value] = None
            if self.__ts[self.__idx+1].value == ":" or self.__ts[self.__idx+1].value == "=":
                self.produce.variable = token.value
        if any(self.produce.math_expression) and token.value == ";":
            self.math_sam_code()
        elif any(self.produce.logical_expression) and token.value in [";", "{"]:
            self.logical_sam_code(token)
        elif self.produce.start_if_logical_operation or self.produce.start_while_logical_operation:
            self.produce.logical_expression.append(token)
        elif self.produce.start_set_value:
            self.produce.math_expression.append(token)
        if self.peek().value == "=":
            self.produce.start_set_value = True
        elif self.peek().value == "if":
            self.produce.start_if_logical_operation = True
        elif token.value == "while":
            self.produce.start_while_logical_operation = True

    def match(self, token: TokenVariable) -> None:
        if token == "$":
            self.produce.functions.append("STOP")
            self.advance()
            return
        self.build_operations(self.peek())
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
