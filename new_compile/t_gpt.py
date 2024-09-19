class GrammarEx:
    def __init__(self):
        self.terminals = set()
        self.nonterminals = set()
        self.productions = {}
        self.first = {}
        self.follow = {}

    def add_terminal(self, terminal):
        self.terminals.add(terminal)

    def add_nonterminal(self, nonterminal):
        self.nonterminals.add(nonterminal)
        self.productions[nonterminal] = []

    def add_production(self, nonterminal, production):
        self.productions[nonterminal].append(production)

    def calculate_first(self):
        for nonterminal in self.nonterminals:
            self.first[nonterminal] = self.first_set(nonterminal)

    def first_set(self, symbol):
        if symbol in self.terminals:
            return {symbol}

        if symbol in self.first:
            return self.first[symbol]

        first_set = set()
        for production in self.productions[symbol]:
            if production == []:  # Production is ε
                first_set.add('ε')
            else:
                for s in production:
                    s_first = self.first_set(s)
                    first_set.update(s_first - {'ε'})
                    if 'ε' not in s_first:
                        break
                else:
                    first_set.add('ε')

        self.first[symbol] = first_set
        return first_set

    def calculate_follow(self):
        for nonterminal in self.nonterminals:
            self.follow[nonterminal] = set()
        start_symbol = next(iter(self.nonterminals))
        self.follow[start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for nonterminal in self.nonterminals:
                for production in self.productions[nonterminal]:
                    follow_set = self.follow[nonterminal]
                    for i in reversed(range(len(production))):
                        symbol = production[i]
                        if symbol in self.nonterminals:
                            before = len(self.follow[symbol])
                            self.follow[symbol].update(follow_set)
                            if 'ε' in self.first_set(symbol):
                                follow_set.update(self.first_set(symbol) - {'ε'})
                            else:
                                follow_set = self.first_set(symbol)
                            if len(self.follow[symbol]) > before:
                                changed = True
                        else:
                            follow_set = self.first_set(symbol)

    def is_ll1(self):
        self.calculate_first()
        self.calculate_follow()

        for nonterminal, productions in self.productions.items():
            first_sets = []
            for production in productions:
                production_first = set()
                for symbol in production:
                    production_first.update(self.first_set(symbol))
                    if 'ε' not in self.first_set(symbol):
                        break
                else:
                    production_first.add('ε')
                first_sets.append(production_first)

            for i, first_i in enumerate(first_sets):
                for j, first_j in enumerate(first_sets):
                    if i != j and first_i & first_j:
                        return False

            if 'ε' in self.first[nonterminal]:
                if self.first[nonterminal] & self.follow[nonterminal]:
                    return False

        return True

# Criando a gramática conforme especificado
G = GrammarEx()

# Terminais
G.add_terminal('let')  # 0
G.add_terminal('id')  # 1
G.add_terminal('colon')  # 2
G.add_terminal('type')  # 3
G.add_terminal('assign')  # 4
G.add_terminal('plus')  # 5
G.add_terminal('minus')  # 6
G.add_terminal('times')  # 7
G.add_terminal('divide')  # 8
G.add_terminal('lparen')  # 9
G.add_terminal('rparen')  # 10
G.add_terminal('inum')  # 11
G.add_terminal('fnum')  # 12
G.add_terminal('semicolon')  # 13
G.add_terminal('$')  # 14

# Não-terminais
G.add_nonterminal('Prog')  # 15
G.add_nonterminal('Decls')  # 16
G.add_nonterminal('Decl')  # 17
G.add_nonterminal('DeclPrime')  # 18
G.add_nonterminal('Expr')  # 19
G.add_nonterminal('ExprPrime')  # 20
G.add_nonterminal('Term')  # 21
G.add_nonterminal('TermPrime')  # 22
G.add_nonterminal('Signal')  # 23
G.add_nonterminal('Factor')  # 24

# Produções
G.add_production('Prog', ['Decls', '$'])    # 25
G.add_production('Decls', ['Decl', 'Decls'])   # 26
G.add_production('Decls', [])   # 27
G.add_production('Decl', ['let', 'id', 'colon', 'type', 'DeclPrime'])  # 28
G.add_production('DeclPrime', ['semicolon'])   # 29
G.add_production('DeclPrime',['assign', 'Expr', 'semicolon'])  # 30
G.add_production('Expr', ['Term', 'ExprPrime'])   # 31
G.add_production('ExprPrime', ['Signal', 'Term', 'ExprPrime'])   # 32
G.add_production('ExprPrime', [])    # 33
G.add_production('Term', ['Factor', 'TermPrime'])   # 34
G.add_production('TermPrime', ['Signal', 'Factor', 'TermPrime'])   # 35
G.add_production('TermPrime', [])   # 36
G.add_production('Signal', ['plus'])   # 37
G.add_production('Signal', ['minus'])    # 38
G.add_production('Signal', ['times'])   # 39
G.add_production('Signal', ['divide'])   # 40
G.add_production('Factor', ['id'])   # 41
G.add_production('Factor', ['inum'])   # 42
G.add_production('Factor', ['fnum'])  # 43
G.add_production('Factor', ['lparen', 'Expr', 'rparen'])   # 44

# Verificar se a gramática é LL(1)
# is_ll1 = G.is_ll1()
# print("A gramática é LL(1)?", is_ll1)
