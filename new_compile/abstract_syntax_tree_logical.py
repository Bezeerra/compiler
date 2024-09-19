import ast

class SAMGenerator(ast.NodeVisitor):
    def __init__(self, context=None):
        self.instructions = []
        self.context = context if context else {}

    def visit_BoolOp(self, node):
        self.visit(node.values[0])
        for value in node.values[1:]:
            self.visit(value)
            op_type = type(node.op)
            if op_type == ast.And:
                self.instructions.append("TIMES")
            elif op_type == ast.Or:
                self.instructions.append("ADD")
            else:
                self.instructions.append("UNKNOWN_BOOL_OP")
        if isinstance(node.op, ast.Or):
            self.instructions.append("PUSHIMM 0")
            self.instructions.append("GREATER")

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        op_type = type(node.op)
        if op_type == ast.Add:
            self.instructions.append("ADD")
        elif op_type == ast.Sub:
            self.instructions.append("SUB")
        elif op_type == ast.Mult:
            self.instructions.append("TIMES")
        elif op_type == ast.Div:
            self.instructions.append("DIV")
        else:
            self.instructions.append("UNKNOWN_OP")

    def visit_Compare(self, node):
        self.visit(node.left)
        self.visit(node.comparators[0])

        op_type = type(node.ops[0])
        if op_type == ast.Gt:  # >
            self.instructions.append("GREATER")
        elif op_type == ast.Lt:  # <
            self.instructions.append("LESS")
        elif op_type == ast.GtE:  # >=
            self.instructions.append("LESS")
            self.instructions.append("NOT")
        elif op_type == ast.LtE:  # <=
            self.instructions.append("GREATER")
            self.instructions.append("NOT")
        elif op_type == ast.Eq:  # ==
            self.instructions.append("EQUAL")
        elif op_type == ast.NotEq:  # !=
            self.instructions.append("EQUAL")
            self.instructions.append("NOT")
        else:
            self.instructions.append("UNKNOWN_COMPARISON")

    def visit_Constant(self, node):
        self.instructions.append(f"PUSHIMM {node.value}")

    def visit_Name(self, node):
        var_name = node.id
        if var_name in self.context:
            value = self.context[var_name]
            self.instructions.append(f"PUSHABS {value}")
        else:
            print(f"ERROR: Variable {var_name} not in context")

    def visit_Expr(self, node):
        self.visit(node.value)

def generate_sam_logical_code(expr, context=None):
    tree = ast.parse(expr, mode='eval')
    generator = SAMGenerator(context)
    generator.visit(tree.body)
    return generator.instructions

# expression1 = "(a > b) or (a > c)"
# context = {"a": 1, "b": 2, "c": 3}
# sam_instructions1 = generate_sam(expression1, context)
#
# print("Instruções SAM para ((a > b) OR (a > c)):")
# for instruction in sam_instructions1:
#     print(instruction)
#
# expression2 = "(a > b) and (a > c) or (a > b) or (a > c)"
# sam_instructions2 = generate_sam(expression2, context)
#
# print("\nInstruções SAM para ((a > b) AND (a > c)):")
# for instruction in sam_instructions2:
#     print(instruction)
