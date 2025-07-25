# _-- EQUIPE SUDOKU: AP3 --_
# Diego Rebouças Castelo - 581920
# Francisco Samuel de S. Silva - 579982
# Davi Fernandes da Costa - 585460

from sudoku_funcoes_utilitarias import (validar_movimento, validar_sudoku_completo, VERDE, AZUL, AMARELO, RESET)

def encontrar_proxima_celula_vazia(tabuleiro):
    """
    Percorre o 'tabuleiro' em busca da próxima célula vazia (valor 0).
    Retorna a linha e coluna da primeira célula vazia encontrada.
    Se o tabuleiro estiver completamente preenchido, retorna (None, None).
    """
    for linha in range(9):
        for coluna in range(9):
            if tabuleiro[linha][coluna] == 0:
                return linha, coluna
    return None, None 

def resolver_sudoku_backtracking(tabuleiro):
    """
    Implementa o algoritmo de Backtracking para tentar resolver o Sudoku.
    Esta função modifica o 'tabuleiro' passado diretamente (in-place) e retorna True se encontrar UMA
    solução, False caso contrário.

    O Backtracking funciona assim:
    1. Encontra uma célula vazia.
    2. Tenta colocar um número (de 1 a 9) nela.
    3. Se o número for válido para aquela posição, ele é colocado lá.
    4. Chama a si mesma (recursivamente) para resolver o resto do tabuleiro.
    5. Se a chamada recursiva retornar True (o resto do tabuleiro foi resolvido), então a solução foi encontrada e True é propagado de volta.
    6. Se a chamada recursiva retornar False (o número atual não levou a uma solução), o número é removido e o próximo é tentado.
    7. Se todos os números de 1 a 9 forem tentados e nenhum levar a uma solução, retorna False.
    """
    linha, coluna = encontrar_proxima_celula_vazia(tabuleiro)

    # Caso base da recursão: Se não tem célula vazia, o tabuleiro está resolvido.
    if linha is None:
        return True

    # Tenta cada número de 1 a 9 na célula vazia atual.
    for numero_a_tentar in range(1, 10):
        # Verifica se o número pode ser  colocado.
        if validar_movimento(tabuleiro, linha, coluna, numero_a_tentar):
            tabuleiro[linha][coluna] = numero_a_tentar

            # Chamada recursiva: tenta resolver o restante do tabuleiro.
            if resolver_sudoku_backtracking(tabuleiro):
                return True # Se a recursão encontrou uma solução, propaga o sucesso.

            # Se a chamada recursiva não levou a uma solução, desfaz a tentativa (backtrack).
            tabuleiro[linha][coluna] = 0 # Define a célula de volta para vazia (0)
            
    return False # Se nenhum número de 1 a 9 funcionou nesta célula, não há solução para esta ramificação.

def encontrar_numero_de_solucoes(tabuleiro_original, limite_contagem=2):
    """
    Tenta encontrar soluções para o Sudoku e conta quantas encontra, parando após atingir 'limite_contagem'.
    Isso é usado para verificar se o Sudoku tem uma solução única.
    Esta função trabalha com uma cópia do tabuleiro para não modificá-lo permanentemente e p/ permitir que continue
    buscando após encontrar uma solução.

    Parâmetros:
    - tabuleiro_original: O tabuleiro inicial a ser resolvido.
    - limite_contagem: O número máximo de soluções a serem encontradas antes de parar. Nesse caso é 2, para verificar
    se há mais de uma solução.
    Retorna o número total de soluções encontradas até 'limite_contagem'.
    """
    # Cria uma cópia do tabuleiro original para não alterá-lo.
    tabuleiro_temporario = [linha[:] for linha in tabuleiro_original]
    contador_solucoes = 0 
    
    def encontrar_solucoes_recursivo(tabuleiro_atual):
        # 'nonlocal' é usado para indicar que 'contador_solucoes' não é uma variável local dessa função, mas sim
        # da função externa 'encontrar_numero_de_solucoes'.
        nonlocal contador_solucoes
        
        linha, coluna = encontrar_proxima_celula_vazia(tabuleiro_atual)

        if linha is None: # Caso base: Se o tabuleiro está preenchido, encontramos uma solução.
            contador_solucoes += 1
            return # Retorna para continuar a busca (se limite_contagem permitir)
        
        for numero_a_tentar in range(1, 10):
            if validar_movimento(tabuleiro_atual, linha, coluna, numero_a_tentar):
                tabuleiro_atual[linha][coluna] = numero_a_tentar
                
                encontrar_solucoes_recursivo(tabuleiro_atual) # Chamada recursiva para a próxima célula
                
                if contador_solucoes >= limite_contagem:
                    # Desfaz o movimento para não afetar outras ramificações da busca.
                    tabuleiro_atual[linha][coluna] = 0 
                    return # Sai desta chamada recursiva
                    
                tabuleiro_atual[linha][coluna] = 0 # Backtrack: desfaz a tentativa atual para tentar o próximo número.
        
    encontrar_solucoes_recursivo(tabuleiro_temporario) # Inicia a busca recursiva.
    return contador_solucoes # Retorna o total de soluções encontradas.


def modo_solucionador(tabuleiro_inicial, posicoes_pistas_iniciais, funcao_exibir_tabuleiro):
    """
    Implementa o Modo Solucionador.
    Ele exibe o tabuleiro inicial, pergunta ao usuário se deve proceder, tenta encontrar a solução e verifica se a
    solução é única.
    """
    print(f"{VERDE}--- Modo Solucionador ---{RESET}")
    print("Tabuleiro inicial (apenas pistas):")
    funcao_exibir_tabuleiro(tabuleiro_inicial, posicoes_pistas_iniciais)

    # Pergunta ao usuário se deseja seguir
    seguir_com_solucao = False # Variável de controle do loop
    while not seguir_com_solucao:
        resposta_usuario = input(f"{AZUL}Pistas mostradas. Deseja seguir com a solução do jogo? (S/N): {RESET}").strip().lower()
        if resposta_usuario == 's':
            seguir_com_solucao = True # Altera a condição para sair do loop
        elif resposta_usuario == 'n':
            print(f"{VERDE}Solução cancelada pelo usuário.{RESET}")
            return # Sai da função modo_solucionador
        else:
            print(f"{AMARELO}Resposta inválida. Digite 'S' para sim ou 'N' para não.{RESET}")

    print(f"{AZUL}Tentando encontrar a solução e verificar unicidade...{RESET}")
    
    # Primeiro passo: Contar o número de soluções para verificar unicidade.
    # Usamos uma cópia do tabuleiro_inicial para essa contagem, para não modificá-lo.
    num_solucoes = encontrar_numero_de_solucoes([linha[:] for linha in tabuleiro_inicial], limite_contagem=2)

    if num_solucoes > 1:
        # Se encontrou mais de uma solução, as pistas são insuficientes para uma solução única.
        funcao_exibir_tabuleiro(tabuleiro_inicial, posicoes_pistas_iniciais) # Exibe o tabuleiro original
        print(f"{AMARELO}\nNão foi possível continuar com a solução. As pistas fornecidas são insuficientes (múltiplas soluções possíveis).{RESET}")
    elif num_solucoes == 1:
        print(f"{VERDE}\nSolução única encontrada!{RESET}")
        # Agora, resolvemos o Sudoku para exibir a solução completa.
        # Criamos outra cópia do tabuleiro inicial para o resolver_sudoku_backtracking modificar.
        tabuleiro_solucao_final = [linha[:] for linha in tabuleiro_inicial]
        resolver_sudoku_backtracking(tabuleiro_solucao_final) # Resolve o Sudoku (preenche 'tabuleiro_solucao_final')
        
        funcao_exibir_tabuleiro(tabuleiro_solucao_final, posicoes_pistas_iniciais) # Exibe a solução
        
        # Confirma se a solução encontrada é completa e válida.
        if validar_sudoku_completo(tabuleiro_solucao_final):
            print(f"{VERDE}A solução encontrada é completa e válida.{RESET}")
        else:
            # Caso raro, indicaria um problema no solver ou no validador.
            print(f"{AMARELO}Atenção: A solução encontrada pode ter falhas. (Algo inesperado ocorreu).{RESET}")
    else: # num_solucoes == 0
        # Se não encontrou nenhuma solução, o Sudoku é insolúvel (pistas contraditórias).
        print(f"{AMARELO}\nNão foi possível encontrar uma solução para este Sudoku.{RESET}")
        print(f"{AMARELO}As pistas fornecidas são contraditórias e/ou levam a um Sudoku sem solução.{RESET}")
        print("Tabuleiro original com pistas:")
        funcao_exibir_tabuleiro(tabuleiro_inicial, posicoes_pistas_iniciais) # Exibe o tabuleiro original