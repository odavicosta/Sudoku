# _-- EQUIPE SUDOKU: AP3 --_
# Diego Rebouças Castelo - 581920
# Francisco Samuel de S. Silva - 579982
# Davi Fernandes da Costa - 585460

import re # Importa o módulo de expressões regulares para validação de formato de texto

# --- Definições de Cores ANSI para Terminal ---
# Essas são sequências de escape que permitem imprimir texto com cores diferentes no terminal.
# O 'RESET' retorna a cor do texto ao padrão do terminal.
RESET = "\033[0m"
VERMELHO = "\033[91m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
MAGENTA = "\033[95m"
CIANO = "\033[96m"

# Dicionários criados usando "compreensão de dicionário" para mapear letras (A-I) para índices numéricos (0-8) e vice-versa.
COLUNA_PARA_INDICE = {chr(ord('A') + i): i for i in range(9)} # Dicionário: 'A': 0, 'B': 1, ..., 'I': 8
INDICE_PARA_COLUNA = {i: chr(ord('A') + i) for i in range(9)} # Dicionário: 0: 'A', 1: 'B', ..., 8: 'I'

def converter_coluna_char_para_indice(char_coluna):
    """
    Converte a letra da coluna (ex: 'A', 'b') para seu índice numérico (0-8).
    Utiliza o dicionário COLUNA_PARA_INDICE para a conversão.
    A função .upper() garante que a entrada seja tratada como maiúscula.
    """
    return COLUNA_PARA_INDICE.get(char_coluna.upper())

# --- Funções de Validação de Regras do Sudoku ---

def valido_na_linha(tabuleiro, linha, numero, ignorar_coluna=-1):
    """
    Verifica se um 'numero' pode ser colocado em uma 'linha' específica do 'tabuleiro'
    sem violar a regra de não repetição na linha.
    'ignorar_coluna' é usado para ignorar a própria célula que está sendo testada,
    evitando que ela seja considerada uma duplicata de si mesma.
    Retorna True se o número não estiver duplicado na linha (exceto na coluna ignorada), False caso contrário.
    """
    # 'all()' retorna True se todos os elementos de um iterável forem True.
    # Aqui, verifica para cada coluna 'c' na linha:
    #   - Se 'tabuleiro[linha][c]' é diferente de 'numero' OU se 'c' é a coluna a ser ignorada.
    # Isso significa que é válido se o número não está lá, OU se está na posição que estamos ignorando.
    return all(tabuleiro[linha][c] != numero or c == ignorar_coluna for c in range(9))

def valido_na_coluna(tabuleiro, coluna, numero, ignorar_linha=-1):
    """
    Verifica se um 'numero' pode ser colocado em uma 'coluna' específica do 'tabuleiro' sem violar a regra de não repetição na coluna.
    'ignorar_linha' é usado para ignorar a própria célula que está sendo testada.
    Retorna True se o número não estiver duplicado na coluna (exceto na linha ignorada), False caso contrário.
    """
    return all(tabuleiro[r][coluna] != numero or r == ignorar_linha for r in range(9))

def valido_no_bloco(tabuleiro, linha, coluna, numero, ignorar_linha=-1, ignorar_coluna=-1):
    """
    Verifica se um 'numero' pode ser colocado na célula (linha, coluna) sem violar a regra de não repetição no bloco 3x3 a que a célula pertence.
    'ignorar_linha' e 'ignorar_coluna' são usados para ignorar a própria célula que está sendo testada.
    Retorna True se o número não estiver duplicado no bloco (exceto na célula ignorada), False caso contrário.
    """
    # Calcula a linha e coluna de início do bloco 3x3.
    # Ex: para linha 0,1,2 -> linha_inicial_bloco = 0; para linha 3,4,5 -> linha_inicial_bloco = 3.
    linha_inicial_bloco = (linha // 3) * 3
    coluna_inicial_bloco = (coluna // 3) * 3

    # Itera por todas as células dentro do bloco 3x3.
    for r in range(linha_inicial_bloco, linha_inicial_bloco + 3):
        for c in range(coluna_inicial_bloco, coluna_inicial_bloco + 3):
            # Se a célula atual do loop não é a célula que estamos ignorando E o número já existe, é inválido.
            if (r, c) != (ignorar_linha, ignorar_coluna) and tabuleiro[r][c] == numero:
                return False
    return True # Se o loop terminar, nenhuma duplicata foi encontrada no bloco.

def validar_movimento(tabuleiro, linha, coluna, numero):
    """
    Verifica se a tentativa de colocar um 'numero' na célula (linha, coluna)
    é válida de acordo com as três regras do Sudoku: linha, coluna e bloco 3x3.
    Esta função temporariamente remove o número da célula para validá-lo contra outros
    números do tabuleiro, e depois restaura o valor original.
    Retorna True se o movimento é válido, False caso contrário.
    """
    # Verifica se o número está no intervalo permitido (1 a 9).
    if not (1 <= numero <= 9):
        return False
    
    # Salva o valor atual da célula para restaurá-lo depois.
    valor_original = tabuleiro[linha][coluna]
    # Temporariamente define a célula como vazia (0) para que a validação não compare o número com ele mesmo na sua própria posição.
    tabuleiro[linha][coluna] = 0 

    # Combina as três verificações auxiliares (_e_valido_na_linha, _e_valido_na_coluna, _e_valido_no_bloco).
    # O movimento é válido se todas as três condições forem verdadeiras.
    e_valido = (
        valido_na_linha(tabuleiro, linha, numero) and
        valido_na_coluna(tabuleiro, coluna, numero) and
        valido_no_bloco(tabuleiro, linha, coluna, numero)
    )
    
    # Restaura o valor original na célula do tabuleiro.
    tabuleiro[linha][coluna] = valor_original 
    return e_valido

def validar_sudoku_completo(tabuleiro):
    """
    Verifica se um 'tabuleiro' de Sudoku completo (sem células vazias) está preenchido corretamente, ou seja, sem violar nenhuma regra.
    Retorna True se o tabuleiro estiver completo e válido, False caso contrário.
    """
    for r in range(9): # Itera por todas as linhas
        for c in range(9): # Itera por todas as colunas
            if tabuleiro[r][c] == 0:
                # Se encontrar qualquer célula vazia (0), o Sudoku não está completo, então é inválido.
                return False 
            
            numero = tabuleiro[r][c] # Pega o número da célula atual.
            
            # Valida o 'numero' atual contra as regras, ignorando a própria célula (r, c) para evitar que ele seja considerado uma duplicata de si mesmo.
            if not (valido_na_linha(tabuleiro, r, numero, c) and
                    valido_na_coluna(tabuleiro, c, numero, r) and
                    valido_no_bloco(tabuleiro, r, c, numero, r, c)):
                # Se qualquer uma das verificações falhar, o Sudoku é inválido.
                return False
    
    # Se todos os loops forem concluídos e nenhuma falha for encontrada, o Sudoku é completo e válido.
    return True