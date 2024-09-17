from grammar import Grammar
from predict import predict_algorithm
from token_sequence import token_sequence

def print_grammar(G: Grammar) -> None:
    print('Terminais:', ' '.join([x for x in G.terminals()]))
    print('Não-terminais:', ' '.join([X for X in G.nonterminals()]))
    # print(G.productions())
    print('Produções:', ' '.join(
        ['id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p)) for p in G.productions()]))


def create_example_grammar()->Grammar:
    G = Grammar()
    G.add_nonterminal('S') # 0
    G.add_nonterminal('A') # 1
    G.add_nonterminal('C') # 2
    G.add_nonterminal('B') # 3
    G.add_nonterminal('Q') # 4
    G.add_terminal('$') # 5
    G.add_terminal('c') # 6
    G.add_terminal('d') # 7
    G.add_terminal('q') # 8
    G.add_terminal('a') # 9
    G.add_terminal('b') # 10
    G.add_production('S',['A','C','$']) # 11
    G.add_production('C',['c']) # 12
    G.add_production('C',[]) # 13
    G.add_production('A',['a','B','C','d']) # 14
    G.add_production('A',['B','Q']) # 15
    G.add_production('B',['b','B']) # 16
    G.add_production('B',[]) # 17
    G.add_production('Q',['q']) # 18
    G.add_production('Q',[]) # 19
    return G

def Q(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(18):
        ts.match('q')
    elif ts.peek() in p.predict(19):
        return

def C(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(12):
        ts.match('c')
    elif ts.peek() in p.predict(13):
        return

def B(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(16):
        ts.match('b')
        B(ts,p)
    elif ts.peek in p.predict(17):
        return

def A(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in p.predict(14):
        ts.match('a')
        B(ts,p)
        C(ts,p)
        ts.match('d')
    elif ts.peek in p.predict(15):
        B(ts,p)
        Q(ts,p)
    

def S(ts:token_sequence,p:predict_algorithm)->None:
    if ts.peek() in  p.predict(11):
        A(ts,p)
        C(ts,p)
        ts.match('$')

if __name__ == '__main__':
    G = create_example_grammar()
    print_grammar(G)
    predict_alg = predict_algorithm(G) 
    ts = token_sequence(['a','b','b','b','b','b','c','d','c','c','$'])
    S(ts,predict_alg)
