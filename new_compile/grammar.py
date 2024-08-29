class GrammarEx():
    def __init__(self):
        self.__terminals = {}
        self.__nonterminals = {}
        self.__productions = {}
        self.__id = 0

    def add_terminal(self, x: str) -> int:
        if x in self.__nonterminals:
            raise ValueError()
        self.__terminals[x] = self.__id
        self.__id = self.__id + 1
        return self.__terminals[x]

    def add_nonterminal(self, X: str):
        if X in self.__terminals:
            raise ValueError()
        self.__nonterminals[X] = self.__id
        self.__id = self.__id + 1
        return self.__nonterminals[X]

    def grammar(self, S: str) -> None:
        self.add_nonterminal(S)

    def add_production(self, A: str, rhs: list) -> int:
        self.__productions[self.__id] = {'lhs': '', 'rhs': []}
        self.__productions[self.__id]['lhs'] = A
        self.__productions[self.__id]['rhs'] = rhs
        self.__id = self.__id + 1
        return self.__id - 1

    def terminals(self) -> iter:
        return iter(self.__terminals)

    def nonterminals(self) -> iter:
        return iter(self.__nonterminals)

    def productions(self) -> iter:
        return iter(self.__productions)

    def is_terminal(self, X: str) -> bool:
        return X in self.__terminals

    def rhs(self, p: int) -> list:
        return self.__productions[p]['rhs']

    def lhs(self, p: int) -> str:
        return self.__productions[p]['lhs']

    def occurrences(self, X: str) -> list:
        l = []
        for k, v in self.__productions.items():
            for i, rhs in enumerate(v['rhs']):
                if (rhs == X):
                    l.append((k, i))
        return l

    def productions_for(self, A: str) -> list:
        l = []
        for k, v in self.__productions.items():
            if v['lhs'] == A:
                l.append(k)
        return l

    def production(self, O: tuple[int, int]) -> int:
        return O[0]

    def tail(self, p: int, i: int) -> list:
        return self.__productions[p]['rhs'][i+1:]


def create_grammar() -> GrammarEx:
    G = GrammarEx()

    # Terminais
    G.add_terminal('let')  # 0
    G.add_terminal('id')  # 1
    G.add_terminal('colon')  # 2
    G.add_terminal('i32')  # 3
    G.add_terminal('f32')  # 4
    G.add_terminal('&str')  # 5
    G.add_terminal('=')  # 6
    G.add_terminal('semicolon')  # 7
    G.add_terminal('if')  # 8
    G.add_terminal('else')  # 9
    G.add_terminal('endif')  # 10
    G.add_terminal('while')  # 11
    G.add_terminal('endwhile')  # 12
    G.add_terminal('lparen')  # 13
    G.add_terminal('rparen')  # 14
    G.add_terminal('lbrace')  # 15
    G.add_terminal('rbrace')  # 16
    G.add_terminal('plus')  # 17
    G.add_terminal('minus')  # 18
    G.add_terminal('times')  # 19
    G.add_terminal('divide')  # 20
    G.add_terminal('==')  # 21
    G.add_terminal('!=')  # 22
    G.add_terminal('>')  # 23
    G.add_terminal('>=')  # 24
    G.add_terminal('<')  # 25
    G.add_terminal('<=')  # 26
    G.add_terminal('&&')  # 27
    G.add_terminal('||')  # 28
    G.add_terminal('!')  # 29
    G.add_terminal('$')  # 30

    # Não-terminais
    G.add_nonterminal('Prog')  # 31
    G.add_nonterminal('Decls')  # 32
    G.add_nonterminal('Decl')  # 33
    G.add_nonterminal('Type')  # 35
    G.add_nonterminal('DeclPrime')  # 36
    G.add_nonterminal('Stmt')  # 37
    G.add_nonterminal('IfStmt')  # 38
    G.add_nonterminal('ElsePart')  # 39
    G.add_nonterminal('WhileStmt')  # 40
    G.add_nonterminal('ExprL')  # 41
    G.add_nonterminal('ExprLPrime')  # 42
    G.add_nonterminal('ExprR')  # 43
    G.add_nonterminal('ExprM')  # 44
    G.add_nonterminal('ExprPrime')  # 45
    G.add_nonterminal('Term')  # 46
    G.add_nonterminal('TermPrime')  # 47
    G.add_nonterminal('Factor')  # 48
    G.add_nonterminal('OP')  # 49

    # Produções
    G.add_production('Prog', ['Decls', '$'])  # 50
    G.add_production('Decls', ['Decl', 'Decls'])  # 51
    G.add_production('Decls', ['Stmt', 'Decls'])  # 52
    G.add_production('Decls', [])  # 53
    G.add_production('Decl', ['let', 'id', 'colon', 'Type', 'DeclPrime'])  # 54
    G.add_production('Type', ['i32'])  # 57
    G.add_production('Type', ['f32'])  # 58
    G.add_production('Type', ['&str'])  # 59
    G.add_production('DeclPrime', ['semicolon'])  # 60
    G.add_production('DeclPrime', ['=', 'ExprL', 'semicolon'])  # 61
    G.add_production('Stmt', ['IfStmt'])  # 62
    G.add_production('Stmt', ['WhileStmt'])  # 63
    G.add_production('Stmt', ['Decl'])  # 64
    G.add_production('IfStmt',
                     ['if', 'lparen', 'ExprL', 'rparen', 'lbrace', 'Decls', 'rbrace', 'ElsePart', 'endif'])  # 65
    G.add_production('ElsePart', ['else', 'lbrace', 'Decls', 'rbrace'])  # 66
    G.add_production('ElsePart', [])  # 67
    G.add_production('WhileStmt', ['while', 'lparen', 'ExprL', 'rparen', 'lbrace', 'Decls', 'rbrace', 'endwhile'])  # 68
    G.add_production('ExprL', ['!', 'ExprL'])  # 69
    G.add_production('ExprL', ['ExprR'])  # 70
    G.add_production('ExprL', ['ExprLPrime'])  # 71
    G.add_production('ExprL', ['id'])  # 72
    G.add_production('ExprLPrime', ['ExprL', '&&', 'ExprL'])  # 73
    G.add_production('ExprLPrime', ['ExprL', '||', 'ExprL'])  # 74
    G.add_production('ExprR', ['ExprM', 'OP', 'ExprM'])  # 75
    G.add_production('ExprM', ['Term', 'ExprPrime'])  # 76
    G.add_production('ExprPrime', ['OP', 'Term', 'ExprPrime'])  # 77
    G.add_production('ExprPrime', [])  # 78
    G.add_production('Term', ['Factor', 'TermPrime'])  # 79
    G.add_production('TermPrime', ['OP', 'Factor', 'TermPrime'])  # 80
    G.add_production('TermPrime', [])  # 81
    G.add_production('Factor', ['id'])  # 82
    G.add_production('Factor', ['lparen', 'ExprL', 'rparen'])  # 83
    G.add_production('OP', ['plus'])  # 84
    G.add_production('OP', ['minus'])  # 85
    G.add_production('OP', ['times'])  # 86
    G.add_production('OP', ['divide'])  # 87
    G.add_production('OP', ['=='])  # 88
    G.add_production('OP', ['!='])  # 89
    G.add_production('OP', ['>'])  # 90
    G.add_production('OP', ['>='])  # 91
    G.add_production('OP', ['<'])  # 92
    G.add_production('OP', ['<='])  # 93

    return G
