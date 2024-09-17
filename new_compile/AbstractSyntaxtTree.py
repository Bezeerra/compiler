import ast

class SAMGenerator(ast.NodeVisitor):
    def __init__(self, context=None):
        self.instructions = []
        self.context = context if context else {}

    def visit_BinOp(self, node):
        # Primeiro visitar os filhos (lado esquerdo e direito)
        self.visit(node.left)
        self.visit(node.right)

        # Determinar o operador e gerar a instrução SAM correta
        op_type = type(node.op)
        if op_type == ast.Add:
            self.instructions.append("ADD")
        elif op_type == ast.Sub:
            self.instructions.append("SUB")
        elif op_type == ast.Mult:
            self.instructions.append("TIMES")
        elif op_type == ast.Div:
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
        self.instructions.append(f"PUSHIMM {node.value}")

    def visit_Name(self, node):
        var_name = node.id
        if var_name in self.context:
            # Se a variável está no contexto, usamos seu valor
            value = self.context[var_name]
            self.instructions.append(f"PUSHABS {value}")
        else:
            print("ERROR VARIABLE NOT IN CONTEXT")
            # Se não, empilhamos o nome da variável
            # self.instructions.append(f"PUSHABS {var_name}")

    def visit_Expr(self, node):
        self.visit(node.value)

def generate_sam(expr, context=None):
    # Convertemos a expressão para uma árvore AST
    tree = ast.parse(expr, mode='eval')
    generator = SAMGenerator(context)
    # Visitamos a árvore e geramos as instruções SAM
    generator.visit(tree.body)
    return generator.instructions

# expression = "(5 * (1 + 4)) + 2"
# sam_instructions = generate_sam(expression)
#
# for instruction in sam_instructions:
#     print(instruction)
