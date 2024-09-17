from typing import Any



class CategoryValue:
    def __init__(self, category, value = None):
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


class LogicalOperation(CategoryValue):
    expression: bool


class TokenWhile(CategoryValue):
    def __init__(self, category, value, logical_operation):
        super().__init__(category, value)
        self.logical_operation = logical_operation


class TokenVariable(CategoryValue):
    def __init__(self, category, value):
        super().__init__(category, value)

class TokenAddressMemory(CategoryValue):
    def __init__(self, category, value, address):
        super().__init__(category, value)
        self.address = address

class Tokenize:
    def __init__(self):
        self.ept = {} # utilizado como contexto de loop;

    @staticmethod
    def make_operations(operator: str, condition_one, condition_two) -> bool:
        logical_map = {
            "==": condition_one == condition_two,
            "!=": condition_one != condition_two,
            ">=": condition_one >= condition_two,
            "<=": condition_one <= condition_two,
            ">": condition_one > condition_two,
            "<": condition_one < condition_two,
        }
        return logical_map[operator]


    def parser_logical_operation(self, operation, conditions = {}, count = 0):
        for l in operation:
            if l == "(":
                count += 1
                if conditions.get(count):
                    conditions[count] = l
            conditions[count] += l
            if l == ")":
                count -= 1

    def create_logical_operation(self, logical_operation: str):
        #  while((a >= 10) || (c > 15)){ }
        ...

    def create_token(self, re_search, category, token):
        if "while" in category:
            token = TokenWhile(
                category=category,
                logical_operation=self.parser_logical_operation(re_search.group(0))
            )
        else:
            token = TokenVariable(category, token)
        return token
