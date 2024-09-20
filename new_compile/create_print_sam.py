def string_to_sam(input_string):
    sam_code = []

    # Adiciona o ADDSP para alocar espaço para 1 variável
    sam_code.append("ADDSP 1")

    # Adiciona o tamanho da string na primeira posição de memória
    string_length = len(input_string) + 1  # +1 para incluir o terminador nulo
    sam_code.append(f"PUSHIMM {string_length}")  # Tamanho da string
    sam_code.append("STOREABS 0")  # Armazena o tamanho na posição 0

    # Endereço inicial da string na memória
    sam_code.append("PUSHIMM 1")
    sam_code.append("STOREABS 1")

    # Processa cada caractere da string e o converte para seu código ASCII
    memory_position = 2
    for char in input_string:
        ascii_value = ord(char)
        sam_code.append(f"PUSHIMM {ascii_value}")  # Coloca o valor ASCII do caractere na pilha
        sam_code.append(f"STOREABS {memory_position}")  # Armazena na posição de memória
        memory_position += 1

    # Adiciona o terminador nulo (0) ao final da string
    sam_code.append(f"PUSHIMM 0")
    sam_code.append(f"STOREABS {memory_position}")

    # Chama WRITESTR para escrever a string na saída
    sam_code.append("PUSHIMM 1")  # Endereço inicial da string
    sam_code.append("WRITESTR")

    return sam_code
