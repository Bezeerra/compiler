import sys

from new_compile.grammar import GrammarEx
from new_compile.ll_1_check import predict_algorithm
from new_compile.main import token_sequence
from new_compile.read_program import read_program
# from new_compile.t_gpt import is_ll1
from new_compile.wirte_ll1_parser import write_ll1_parser


def print_grammar(G: GrammarEx) -> None:
    print('Terminais:', ' '.join([x for x in G.terminals()]))
    print('Não-terminais:', ' '.join([X for X in G.nonterminals()]))
    # print(G.productions())
    print('Produções:', ' '.join(
        ['id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p)) for p in G.productions()]))


def create_grammar() -> GrammarEx:
    G = GrammarEx()

    # Terminais
    G.add_terminal('let')  # 0
    G.add_terminal('id')  # 1
    G.add_terminal(':')  # 2
    G.add_terminal('i32')  # 3
    G.add_terminal('f32')  # 4
    G.add_terminal('&str')  # 5
    G.add_terminal('=')  # 6
    G.add_terminal(';')  # 7
    G.add_terminal('if')  # 8
    G.add_terminal('else')  # 9
    G.add_terminal('endif')  # 10
    G.add_terminal('while')  # 11
    G.add_terminal('endwhile')  # 12
    G.add_terminal('(')  # 13
    G.add_terminal(')')  # 14
    G.add_terminal('{')  # 15
    G.add_terminal('}')  # 16
    G.add_terminal('+')  # 17
    G.add_terminal('-')  # 18
    G.add_terminal('*')  # 19
    G.add_terminal('/')  # 20
    G.add_terminal('==')  # 21
    G.add_terminal('!=')  # 22
    G.add_terminal('>')  # 23
    G.add_terminal('>=')  # 24
    G.add_terminal('<')  # 25
    G.add_terminal('<=')  # 26
    G.add_terminal('OR')  # 27
    G.add_terminal('AND')  # 28
    G.add_terminal('NOT')  # 29
    G.add_terminal('$')  # 30
    G.add_terminal('print')
    G.add_terminal('"string"')
    G.add_terminal('"')
    G.add_terminal(',')
    G.add_terminal('num')
    G.add_terminal('fnum')
    G.add_terminal('func')
    G.add_terminal('return')

    # Não-terminais
    G.add_nonterminal('Prog')  # 31
    G.add_nonterminal('Decls')  # 32
    G.add_nonterminal('Decl')  # 33
    G.add_nonterminal('DeclPrime')  # 34
    G.add_nonterminal('Type')  # 35
    G.add_nonterminal('Stmt')  # 36
    G.add_nonterminal('IfStmt')  # 37
    G.add_nonterminal('ElsePart')  # 38
    G.add_nonterminal('WhileStmt')  # 39
    G.add_nonterminal('ExprL')  # 40
    G.add_nonterminal('ExprLTail')  # 41
    G.add_nonterminal('simpleExprL')  # 42
    G.add_nonterminal('simpleExprLTail')  # 43
    G.add_nonterminal('ExprR')  # 44
    G.add_nonterminal('ExprRPrime')  # 45
    G.add_nonterminal('ExprRTerm')  # 46
    G.add_nonterminal('ExprRTermPrime')  # 47
    G.add_nonterminal('Factor')  # 48
    G.add_nonterminal('relationOperator')  # 49
    G.add_nonterminal('ExtPrint')

    # Produções
    G.add_production('Prog', ['Decls', '$'])  # 50
    G.add_production('Decls', ['Decl', 'Decls'])  # 51
    G.add_production('Decls', ['Stmt', 'Decls'])  # 52
    G.add_production('Decls', [])  # 53
    G.add_production('Decl', ['let', 'id', ':', 'Type', 'DeclPrime'])  # 54
    G.add_production('Decl', ['print', '(', 'Factor' , 'ExtPrint', ')', ';'])
    G.add_production('Decl', ['func', 'id', '(', 'ExtPrint', ')', '{', 'Decls', 'return', '}'])
    G.add_production('ExtPrint', [',', 'Factor'])
    G.add_production('ExtPrint', ['Factor', 'ExtPrint'])
    G.add_production('ExtPrint', [])
    G.add_production('Type', ['i32'])  # 55
    G.add_production('Type', ['f32'])  # 56
    G.add_production('Type', ['&str'])  # 57
    G.add_production('DeclPrime', [';'])  # 58
    G.add_production('DeclPrime', ['=', 'ExprL', ';'])  # 59
    G.add_production('Stmt', ['IfStmt'])  # 60
    G.add_production('Stmt', ['WhileStmt'])  # 61
    G.add_production('IfStmt',
                     ['if', '(', 'ExprL', ')', '{', 'Decls', '}', 'ElsePart', 'endif'])  # 62
    G.add_production('ElsePart', ['else', '{', 'Decls', '}'])  # 63
    G.add_production('ElsePart', [])  # 64
    G.add_production('WhileStmt', ['while', '(', 'ExprL', ')', '{', 'Decls', '}', 'endwhile'])  # 65
    G.add_production('ExprL', ['NOT', 'ExprL'])  # 66
    G.add_production('ExprL', ['simpleExprL', 'ExprLTail'])  # 67
    G.add_production('ExprLTail', ['OR', 'ExprL'])  # 68
    G.add_production('ExprLTail', ['AND', 'ExprL'])  # 69
    G.add_production('ExprLTail', [])  # 70
    G.add_production('simpleExprL', ['ExprR', 'simpleExprLTail'])  # 71
    G.add_production('simpleExprLTail', ['relationOperator', 'ExprR'])  # 72
    G.add_production('simpleExprLTail', [])  # 73
    G.add_production('ExprR', ['ExprRTerm', 'ExprRPrime'])  # 74
    G.add_production('ExprRPrime', ['+', 'ExprRTerm', 'ExprRPrime'])  # 75
    G.add_production('ExprRPrime', ['-', 'ExprRTerm', 'ExprRPrime'])  # 76
    G.add_production('ExprRPrime', [])  # 77
    G.add_production('ExprRTerm', ['Factor', 'ExprRTermPrime'])  # 78
    G.add_production('ExprRTermPrime', ['*', 'Factor', 'ExprRTermPrime'])  # 79
    G.add_production('ExprRTermPrime', ['/', 'Factor', 'ExprRTermPrime'])  # 80
    G.add_production('ExprRTermPrime', [])  # 81
    G.add_production('Factor', ['id'])  # 82
    G.add_production('Factor', ['num'])  # 82
    G.add_production('Factor', ['fnum'])  # 82
    G.add_production('Factor', ['"string"'])
    G.add_production('Factor', ['(', 'ExprL', ')'])  # 83
    G.add_production('relationOperator', ['=='])  # 84
    G.add_production('relationOperator', ['!='])  # 85
    G.add_production('relationOperator', ['>'])  # 86
    G.add_production('relationOperator', ['>='])  # 87
    G.add_production('relationOperator', ['<'])  # 88
    G.add_production('relationOperator', ['<='])  # 89

    return G


class Produce:
    def __init__(self):
        self.full_table = {}
        self.math_expression= []
        self.logical_expression = []
        self.functions = []
        self.in_context = []
        self.start_func_context = None
        self.start_produce_index_func = None
        self.functions_in_func = []
        self.if_context = 0
        self.while_context = 0
        self.else_context = 0
        self.address_memory = 150
        self.start_set_value = False
        self.start_if_logical_operation = False
        self.start_while_logical_operation = False
        self.variable = None


    def get_address_memory(self):
        self.address_memory += 1
        return self.address_memory

    def write_sam_code(self, text: str) -> None:
        with open("sam_example.sam", "a") as f:
            f.write(text)

    def Prog(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(59):
            self.Decls(ts, p)
            ts.match('$')
        else:
            print("Syntax Error at 'Prog'")
            sys.exit(0)

    def Decls(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(60):
            self.Decl(ts, p)
            self.Decls(ts, p)
        elif ts.peek() in p.predict(61):
            self.Stmt(ts, p)
            self.Decls(ts, p)
        elif ts.peek() in p.predict(62):
            return
        else:
            print("Syntax Error at 'Decls'")
            sys.exit(0)

    def Decl(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(63):
            ts.match('let')
            ts.match('id')
            ts.match(':')
            self.Type(ts, p)
            self.DeclPrime(ts, p)
        elif ts.peek() in p.predict(64):
            ts.match('print')
            ts.match('(')
            self.Factor(ts, p)
            self.ExtPrint(ts, p)
            ts.match(')')
            ts.match(';')
        elif ts.peek() in p.predict(65):
            ts.match('func')
            ts.match('id')
            ts.match('(')
            self.ExtPrint(ts, p)
            ts.match(')')
            ts.match('{')
            self.Decls(ts, p)
            ts.match('return')
            ts.match('}')
        else:
            print("Syntax Error at 'Decl'")
            sys.exit(0)

    def DeclPrime(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(72):
            ts.match(';')
        elif ts.peek() in p.predict(73):
            ts.match('=')
            self.ExprL(ts, p)
            ts.match(';')
        else:
            print("Syntax Error at 'DeclPrime'")
            sys.exit(0)

    def Type(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(69):
            ts.match('i32')
        elif ts.peek() in p.predict(70):
            ts.match('f32')
        elif ts.peek() in p.predict(71):
            ts.match('&str')
        else:
            print("Syntax Error at 'Type'")
            sys.exit(0)

    def Stmt(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(74):
            self.IfStmt(ts, p)
        elif ts.peek() in p.predict(75):
            self.WhileStmt(ts, p)
        else:
            print("Syntax Error at 'Stmt'")
            sys.exit(0)

    def IfStmt(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(76):
            ts.match('if')
            ts.match('(')
            self.ExprL(ts, p)
            ts.match(')')
            ts.match('{')
            self.Decls(ts, p)
            ts.match('}')
            self.ElsePart(ts, p)
            ts.match('endif')
        else:
            print("Syntax Error at 'IfStmt'")
            sys.exit(0)

    def ElsePart(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(77):
            ts.match('else')
            ts.match('{')
            self.Decls(ts, p)
            ts.match('}')
        elif ts.peek() in p.predict(78):
            return
        else:
            print("Syntax Error at 'ElsePart'")
            sys.exit(0)

    def WhileStmt(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(79):
            ts.match('while')
            ts.match('(')
            self.ExprL(ts, p)
            ts.match(')')
            ts.match('{')
            self.Decls(ts, p)
            ts.match('}')
            ts.match('endwhile')
        else:
            print("Syntax Error at 'WhileStmt'")
            sys.exit(0)

    def ExprL(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(80):
            ts.match('NOT')
            self.ExprL(ts, p)
        elif ts.peek() in p.predict(81):
            self.simpleExprL(ts, p)
            self.ExprLTail(ts, p)
        else:
            print("Syntax Error at 'ExprL'")
            sys.exit(0)

    def ExprLTail(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(82):
            ts.match('OR')
            self.ExprL(ts, p)
        elif ts.peek() in p.predict(83):
            ts.match('AND')
            self.ExprL(ts, p)
        elif ts.peek() in p.predict(84):
            return
        else:
            print("Syntax Error at 'ExprLTail'")
            sys.exit(0)

    def simpleExprL(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(85):
            self.ExprR(ts, p)
            self.simpleExprLTail(ts, p)
        else:
            print("Syntax Error at 'simpleExprL'")
            sys.exit(0)

    def simpleExprLTail(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(86):
            self.relationOperator(ts, p)
            self.ExprR(ts, p)
        elif ts.peek() in p.predict(87):
            return
        else:
            print("Syntax Error at 'simpleExprLTail'")
            sys.exit(0)

    def ExprR(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(88):
            self.ExprRTerm(ts, p)
            self.ExprRPrime(ts, p)
        else:
            print("Syntax Error at 'ExprR'")
            sys.exit(0)

    def ExprRPrime(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(89):
            ts.match('+')
            self.ExprRTerm(ts, p)
            self.ExprRPrime(ts, p)
        elif ts.peek() in p.predict(90):
            ts.match('-')
            self.ExprRTerm(ts, p)
            self.ExprRPrime(ts, p)
        elif ts.peek() in p.predict(91):
            return
        else:
            print("Syntax Error at 'ExprRPrime'")
            sys.exit(0)

    def ExprRTerm(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(92):
            self.Factor(ts, p)
            self.ExprRTermPrime(ts, p)
        else:
            print("Syntax Error at 'ExprRTerm'")
            sys.exit(0)

    def ExprRTermPrime(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(93):
            ts.match('*')
            self.Factor(ts, p)
            self.ExprRTermPrime(ts, p)
        elif ts.peek() in p.predict(94):
            ts.match('/')
            self.Factor(ts, p)
            self.ExprRTermPrime(ts, p)
        elif ts.peek() in p.predict(95):
            return
        else:
            print("Syntax Error at 'ExprRTermPrime'")
            sys.exit(0)

    def Factor(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(96):
            ts.match('id')
        elif ts.peek() in p.predict(97):
            ts.match('num')
        elif ts.peek() in p.predict(98):
            ts.match('fnum')
        elif ts.peek() in p.predict(99):
            ts.match('"string"')
        elif ts.peek() in p.predict(100):
            ts.match('(')
            self.ExprL(ts, p)
            ts.match(')')
        else:
            print("Syntax Error at 'Factor'")
            sys.exit(0)

    def relationOperator(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(101):
            ts.match('==')
        elif ts.peek() in p.predict(102):
            ts.match('!=')
        elif ts.peek() in p.predict(103):
            ts.match('>')
        elif ts.peek() in p.predict(104):
            ts.match('>=')
        elif ts.peek() in p.predict(105):
            ts.match('<')
        elif ts.peek() in p.predict(106):
            ts.match('<=')
        else:
            print("Syntax Error at 'relationOperator'")
            sys.exit(0)

    def ExtPrint(self, ts: token_sequence, p: predict_algorithm):
        if ts.peek() in p.predict(66):
            ts.match(',')
            self.Factor(ts, p)
        elif ts.peek() in p.predict(67):
            self.Factor(ts, p)
            self.ExtPrint(ts, p)
        elif ts.peek() in p.predict(68):
            return
        else:
            print("Syntax Error at 'ExtPrint'")
            sys.exit(0)

# Exemplo de uso
if __name__ == '__main__':
    G = create_grammar()
    # write_ll1_parser(G)
    predict_alg = predict_algorithm(G)
    tokens = read_program("code.rs")
    produce = Produce()
    ts = token_sequence(tokens, produce)
    produce.Prog(ts, predict_alg)
    for function in produce.functions:
        print(function)

