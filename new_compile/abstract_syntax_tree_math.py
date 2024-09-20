import ast
import re


class SAMGenerator(ast.NodeVisitor):
    def __init__(self, context=None):
        self.instructions = []
        self.is_float_numbers = False
        self.context = context if context else {}

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

        op_type = type(node.op)
        if op_type == ast.Add:
            if self.is_float_numbers:
                self.instructions.append("ADDF")
            else:
                self.instructions.append("ADD")
        elif op_type == ast.Sub:
            if self.is_float_numbers:
                self.instructions.append("SUBF")
            else:
                self.instructions.append("SUB")
        elif op_type == ast.Mult:
            if self.is_float_numbers:
                self.instructions.append("TIMESF")
            else:
                self.instructions.append("TIMES")
        elif op_type == ast.Div:
            if self.is_float_numbers:
                self.instructions.append("DIVF")
            else:
                self.instructions.append("DIV")
        elif op_type == ast.Mod:
            self.instructions.append("MOD")
        elif op_type == ast.Pow:
            self.instructions.append("POW")
        else:
            self.instructions.append("UNKNOWN_OP")

    def visit_Num(self, node):
        self.instructions.append(f"PUSHIMM {node.n}")

    def visit_Constant(self, node):
        if isinstance(node.value, float):
            self.is_float_numbers = True
            self.instructions.append(f"PUSHIMMF {node.value}")
        else:
            self.instructions.append(f"PUSHIMM {node.value}")

    def visit_Name(self, node):
        var_name = node.id
        if var_name in self.context:
            value = self.context[var_name]
            if not value:
                raise ValueError(f"Variable '{var_name}' no has value")
            self.instructions.append(f"PUSHABS {value}")
        else:
            print("ERROR VARIABLE NOT IN CONTEXT")

    def visit_Expr(self, node):
        self.visit(node.value)

def generate_sam_math_code(expr, context=None):
    tree = ast.parse(expr, mode='eval')
    generator = SAMGenerator(context)
    generator.visit(tree.body)
    return generator.instructions

# expression = "(5 * (1 + 4)) + 2"
# sam_instructions = generate_sam(expression)
#
# for instruction in sam_instructions:
#     print(instruction)
