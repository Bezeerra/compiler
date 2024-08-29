from new_compile.grammar import GrammarEx


class follow_algorithm:
    def __init__(self, G: GrammarEx) -> None:
        self.__G = G
        self.__first_alg = first_algorithm(G)
        self.__empty_string_alg = derives_empty_string_algorithm(G)
        self.__visited = {}
        self.__symbol_derives_empty = {}

    def run(self, A: str) -> set:
        self.__empty_string_alg.run()
        self.__symbol_derives_empty = self.__empty_string_alg.symbol_derives_empty()
        for X in self.__G.nonterminals():
            self.__visited[X] = False
        return self.internal_follow(A)

    def internal_follow(self, A: str) -> set:
        ans = set()
        if not self.__visited[A]:
            self.__visited[A] = True
            for (p, i) in self.__G.occurrences(A):
                tail = self.__G.tail(p, i)
                ans.update(self.__first_alg.run(tail))
                if self.all_derive_empty(tail):
                    lhs = self.__G.lhs(self.__G.production((p, i)))
                    ans.update(self.internal_follow(lhs))
        return ans

    def all_derive_empty(self, gamma: list) -> bool:
        for X in gamma:
            if self.__G.is_terminal(X) or not self.__symbol_derives_empty[X]:
                return False
        return True


class first_algorithm:
    def __init__(self, G: GrammarEx) -> None:
        self.__G = G
        self.__visited = {}
        self.__symbol_derives_empty = {}

    def internal_first(self, alfa: list):
        if alfa == []:
            return set()
        X = alfa[0]
        beta = alfa[1:]
        if self.__G.is_terminal(X):
            return set([X])
        ans = set()
        if not self.__visited[X]:
            self.__visited[X] = True
            for p in self.__G.productions_for(X):
                rhs = self.__G.rhs(p)
                ans.update(self.internal_first(rhs))
        if self.__symbol_derives_empty[X]:
            ans.update(self.internal_first(beta))
        return ans

    def run(self, alfa: list) -> set:
        for X in self.__G.nonterminals():
            self.__visited[X] = False
        alg_empty = derives_empty_string_algorithm(self.__G)
        alg_empty.run()
        self.__symbol_derives_empty = alg_empty.symbol_derives_empty()
        return self.internal_first(alfa)



class derives_empty_string_algorithm:
    def __init__(self, G: GrammarEx) -> None:
        self.__symbol_derives_empty = {}
        self.__rule_derives_empty = {}
        self.__count = {}
        self.__queue = []
        self.__G = G

    def __check_for_empty(self, p: int) -> None:
        if self.__count[p] == 0:
            self.__rule_derives_empty[p] = True
            A = self.__G.lhs(p)
            if not self.__symbol_derives_empty[A]:
                self.__symbol_derives_empty[A] = True
                self.__queue.append(A)

    def symbol_derives_empty(self) -> dict:
        return self.__symbol_derives_empty

    def rule_derives_empty(self) -> dict:
        return self.__rule_derives_empty

    def run(self):
        for A in self.__G.nonterminals():
            self.__symbol_derives_empty[A] = False
        for p in self.__G.productions():
            self.__rule_derives_empty[p] = False
            self.__count[p] = 0
            self.__count[p] += len(self.__G.rhs(p))
            self.__check_for_empty(p)
        while len(self.__queue):
            X = self.__queue.pop(0)
            for occ in self.__G.occurrences(X):
                p = self.__G.production(occ)
                self.__count[p] -= 1
                self.__check_for_empty(p)


class predict_algorithm:
    def __init__(self, G: GrammarEx) -> None:
        self.__G = G
        self.__first_alg = first_algorithm(self.__G)
        self.__follow_alg = follow_algorithm(self.__G)
        derives_empty_alg = derives_empty_string_algorithm(self.__G)
        derives_empty_alg.run()
        self.__rule_derives_empty = derives_empty_alg.rule_derives_empty()

    def predict(self, p: int) -> set:
        ans = self.__first_alg.run(self.__G.rhs(p))
        if self.__rule_derives_empty[p]:
            A = self.__G.lhs(p)
            ans.update(self.__follow_alg.run(A))
        return ans


def is_ll1(G: GrammarEx, pred_alg: predict_algorithm) -> bool:
    for A in G.nonterminals():
        pred_set = set()
        for p in G.productions_for(A):
            pred = pred_alg.predict(p)
            if not pred_set.isdisjoint(pred):
                return False
            pred_set.update(pred)
    return True
