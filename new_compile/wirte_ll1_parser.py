from grammar import GrammarEx

def write_ll1_parser(g:GrammarEx):
    for X in g.nonterminals():
        print(f'\ndef {X}(self, ts: token_sequence, p: predict_algorithm):')
        first = True
        for rule in g.productions_for(X):
            rhs = g.rhs(rule)
            if first:
                print(f'\tif',end=' ')
                first = False
            else:
                print(f'\telif',end= ' ')
            print(f'ts.peek() in p.predict({rule}):')
            if len(rhs)==0:
                print('\t\treturn')
            for Y in rhs:
                if g.is_terminal(Y):
                    print(f"\t\tts.match('{Y}')")
                else:
                    print(f'\t\tself.{Y}(ts,p)')

        print('\telse:')
        print(f"\t\tprint(\"Syntax Error at '{X}'\")")
        print(f'\t\tsys.exit(0)')


