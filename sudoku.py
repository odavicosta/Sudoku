# _-- EQUIPE SUDOKU: AP3 --_
# Diego Rebouças Castelo - 581920
# Francisco Samuel de S. Silva - 579982
# Davi Fernandes da Costa - 585460

import sys 
import re

from sudoku_funcoes_utilitarias import (
    RESET, VERMELHO, VERDE, AMARELO, AZUL, CIANO, MAGENTA, # Cores para mensagens no terminal
    COLUNA_PARA_INDICE, INDICE_PARA_COLUNA, # Mapeamentos de coordenadas
    converter_coluna_char_para_indice, # Funções de conversão
    valido_na_linha, valido_na_coluna, valido_no_bloco, # Funções de validação interna
    validar_movimento, validar_sudoku_completo # Funções de validação principal
)

from sudoku_solucionador import modo_solucionador 

# Variáveis Globais de Estado do Jogo
tabuleiro_original_pistas = [] # Armazena o tabuleiro com as pistas iniciais
tabuleiro_jogo_atual = []      # Armazena o estado atual do tabuleiro durante o jogo interativo
posicoes_pistas_iniciais = set() # Um conjunto que guarda as linhas/colunas das pistas originais (para saber quais células o usuário não pode alterar).

def carregar_tabuleiro(caminho_arquivo):
    """
    Carrega o tabuleiro Sudoku de um arquivo de configuração de pistas.
    O arquivo deve conter pistas no formato 'COL,LIN: NUMERO' (ex: A,3: 5).
    Realiza validações do formato do arquivo e da corretude inicial das pistas.

    Retorna uma tupla (tabuleiro_com_pistas, copia_para_jogo, posicoes_das_pistas)
    ou (None, None, None) em caso de erro.
    """
    tabuleiro = [[0 for _ in range(9)] for _ in range(9)] # Inicializa um tabuleiro 9x9 com zeros (0 = célula vazia)
    posicoes_pistas = set() # Conjunto para armazenar as (linha, coluna) das pistas
    numero_pistas = 0        # Contador de pistas lidas

    try:
        with open(caminho_arquivo, 'r') as f:
            for numero_linha, linha_conteudo in enumerate(f, 1):
                linha_conteudo = linha_conteudo.strip() # Remove espaços em branco do início e fim da linha
                

                if linha_conteudo: # Ignora linhas vazias
                    # Usa expressão regular para extrair COLUNA, LINHA e NUMERO da linha.
                    coincidencia = re.match(r'\s*([A-Ia-i])\s*,\s*([1-9])\s*:\s*([1-9])\s*$', linha_conteudo)
                    if not coincidencia:
                        print(f"Erro no arquivo {caminho_arquivo}, linha {numero_linha}: Formato inválido.")
                        return None, None, None # Retorna erro se o formato não corresponder

                    # Extrai os grupos capturados pela expressão regular.
                    char_coluna, str_linha, str_numero = coincidencia.groups()
                    
                    # Converte os valores para os tipos corretos e índices baseados em zero.
                    coluna = converter_coluna_char_para_indice(char_coluna)
                    linha = int(str_linha) - 1 # Subtrai 1 pois linhas são 1-9 para usuário, 0-8 para código
                    numero = int(str_numero)

                    tabuleiro[linha][coluna] = numero # Coloca a pista no tabuleiro
                    posicoes_pistas.add((linha, coluna)) # Adiciona a posição ao conjunto de pistas
                    numero_pistas += 1 # Incrementa o contador de pistas

        # Valida a quantidade total de pistas lidas.
        if not (1 <= numero_pistas <= 80): # Original: 'if 1 > numero_pistas > 80:' - corrigido para lógica correta 'not (1 <= num <= 80)'
            print(f"{VERMELHO}Quantidade de pistas inválida. As pistas devem estar entre 1 e 80.{RESET}")
            return None, None, None

        # Validação da grade de pistas inicial (Requisito 4 do Modo Interativo/Solucionador).
        # Verifica se as pistas fornecidas por si só não violam as regras do Sudoku.
        for r, c in posicoes_pistas: # Itera pelas posições de cada pista
            num = tabuleiro[r][c] # Obtém o número da pista
            tabuleiro_temporario = [row[:] for row in tabuleiro] # Cria uma cópia temporária do tabuleiro para validação
            # Verifica se o número da pista é válido na sua linha, coluna e bloco, ignorando a própria célula.
            if not (valido_na_linha(tabuleiro_temporario, r, num, c) and
                    valido_na_coluna(tabuleiro_temporario, c, num, r) and
                    valido_no_bloco(tabuleiro_temporario, r, c, num, r, c)):
                print(f"{VERMELHO}Configuração de dicas inváida!{RESET}")
                return None, None, None # Retorna erro se uma pista for inválida

        # Cria uma cópia do tabuleiro com as pistas para o jogo interativo (que será modificado pelo usuário).
        tabuleiro_jogo = [linha[:] for linha in tabuleiro]
        
        # Retorna o tabuleiro original (apenas pistas), a cópia para o jogo, e as posições das pistas.
        return tabuleiro, tabuleiro_jogo, posicoes_pistas

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return None, None, None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar o arquivo: {e}")
        return None, None, None

def exibir_tabuleiro(tabuleiro, posicoes_pistas):
    """
    Exibe o tabuleiro Sudoku no terminal com uma formatação visual amigável.
    Pistas iniciais são destacadas em vermelho.
    """
    # Define a linha do cabeçalho com as letras das colunas, com espaçamento para alinhar com a grade.
    cabecalho_colunas = "     A   B   C    D   E   F    G   H   I"
    print(f"\n{cabecalho_colunas}") # Imprime o cabeçalho

    # Define as linhas horizontais de separação.
    linha_fina_horizontal = "  ++---+---+---++---+---+---++---+---+---++"
    linha_grossa_horizontal = "  ++===========+=============+===========++"

    # Itera por cada linha do tabuleiro (0 a 8).
    for r in range(9):
        # Imprime a linha de separação horizontal apropriada antes de cada linha de números.
        # Se for a 3ª ou 6ª linha (r=2 ou r=5), imprime a linha grossa.
        # Caso contrário, imprime a linha fina.
        if r > 0 and r % 3 == 0:
            print(linha_grossa_horizontal)
        else:
            print(linha_fina_horizontal)
        
        # Constrói o conteúdo da linha de números.
        conteudo_linha = []
        # Adiciona o número da linha e o separador vertical esquerdo '||'.
        conteudo_linha.append(f"{r + 1} ||")
        
        # Itera por cada coluna na linha atual.
        for c in range(9):
            numero = tabuleiro[r][c] # Obtém o número da célula atual.
            numero_exibir = str(numero) if numero != 0 else ' ' # Se 0, exibe espaço em branco.
            
            # Define a cor do número: vermelho se for uma pista inicial, senão a cor padrão do terminal.
            if (r, c) in posicoes_pistas:
                codigo_cor = VERMELHO
            else:
                codigo_cor = RESET
            
            # Adiciona o número formatado com cor e espaços.
            conteudo_linha.append(f" {codigo_cor}{numero_exibir}{RESET} ")
            
            # Adiciona o separador vertical apropriado.
            # '||' para as divisões entre blocos 3x3 verticais (colunas 2 e 5).
            # '|' para as divisões internas de células dentro de um bloco.
            if (c + 1) % 3 == 0:
                if c < 9: # Não adiciona '||' após a última coluna
                    conteudo_linha.append("||")
            else:
                conteudo_linha.append("|")
        
        # Adiciona o número da linha no final da grade.
        conteudo_linha.append(f" {r + 1}")
        print("".join(conteudo_linha)) # Imprime a linha completa.

    print(linha_fina_horizontal) # Imprime a linha inferior do tabuleiro
    print(f"{cabecalho_colunas}\n") # Imprime o rodapé com as letras das colunas

def modo_interativo(caminho_arquivo_pistas_param):
    """
    Implementa o Modo Interativo do jogo Sudoku.
    Permite que o usuário jogue o Sudoku em tempo real, inserindo jogadas,
    pedindo possibilidades, apagando números e verificando o progresso.
    """
    global tabuleiro_original_pistas, tabuleiro_jogo_atual, posicoes_pistas_iniciais

    # Carrega o tabuleiro inicial do arquivo de pistas.
    tabuleiro_original_pistas, tabuleiro_jogo_atual, posicoes_pistas_iniciais = carregar_tabuleiro(caminho_arquivo_pistas_param)

    # Se houve um erro ao carregar o tabuleiro, retorna.
    if tabuleiro_original_pistas is None:
        return

    print(f"{VERDE}--- Modo Interativo ---{RESET}")
    print("Comandos:")
    print("   - Jogar: COL,LIN: NUM (Ex: A,3: 7) - Preenche uma célula.")
    print("   - Possibilidades: ?COL,LIN (Ex: ?D,3) - Mostra números possíveis para uma célula vazia.")
    print("   - Apagar: !COL,LIN (Ex: !C,4) - Apaga um número inserido pelo usuário.")
    print("   - Sair: sair - Encerra o jogo interativo.")

    jogo_interativo_ativo = True # Variável de controle para o loop principal do jogo.
    while jogo_interativo_ativo:
        exibir_tabuleiro(tabuleiro_jogo_atual, posicoes_pistas_iniciais) # Exibe o estado atual do tabuleiro.

        # Verifica se o Sudoku está completo e válido.
        if validar_sudoku_completo(tabuleiro_jogo_atual):
            print(f"{VERDE}Parabéns! Você completou o Sudoku corretamente!{RESET}")
            reiniciar_jogo = False # Variável de controle para o loop de "jogar novamente".
            while not reiniciar_jogo:
                resposta = input("Deseja jogar novamente? (S/N): ").strip().lower()
                if resposta == 's':
                    # Chama o modo_interativo recursivamente para iniciar um novo jogo do zero.
                    modo_interativo(caminho_arquivo_pistas_param)
                    return # Sai da instância atual da função, evitando loop duplicado.
                elif resposta == 'n':
                    print("Obrigado por jogar. Até a próxima!")
                    jogo_interativo_ativo = False # Define para False para sair do loop principal.
                    reiniciar_jogo = True # Define para True para sair do loop de "jogar novamente".
                else:
                    print(f"{AMARELO}Entrada inválida. Digite 'S' para sim ou 'N' para não.{RESET}")

        # O loop 'while jogo_interativo_ativo:' se encarregará da saída.
        if jogo_interativo_ativo: # Só pede entrada se o jogo ainda estiver ativo
            entrada_usuario = input("Jogada: ").strip() # Solicita a entrada do usuário.

            # --- Processamento dos Comandos do Usuário ---
            
            comando_processado = False # Flag para controlar se um comando válido foi executado
            
            if entrada_usuario.lower() == 'sair':
                print("Saindo do jogo interativo. Até a próxima!")
                jogo_interativo_ativo = False # Define para False para sair do loop principal.
                comando_processado = True
            elif entrada_usuario.startswith('?'): # Comando para pedir possibilidades.
                # Expressão regular para validar o formato '?COL,LIN' (ex: '?D,3').
                coincidencia = re.match(r'\?\s*([A-Ia-i])\s*,\s*([1-9])\s*$', entrada_usuario)
                if coincidencia:
                    char_coluna, str_linha = coincidencia.groups()
                    coluna = converter_coluna_char_para_indice(char_coluna)
                    linha = int(str_linha) - 1
                    
                    # Validação das coordenadas.
                    if not (0 <= linha < 9 and 0 <= coluna < 9):
                        print(f"{AMARELO}Coordenadas inválidas. Coluna A-I, Linha 1-9.{RESET}")
                    elif tabuleiro_jogo_atual[linha][coluna] != 0:
                        print(f"{AMARELO}A célula já está preenchida. Só é possível pedir possibilidades para células vazias.{RESET}")
                    else:
                        # Calcula as possibilidades testando cada número de 1 a 9.
                        possibilidades = [str(n) for n in range(1, 10)
                                            if validar_movimento(tabuleiro_jogo_atual, linha, coluna, n)]
                        print(f"{CIANO}Possibilidades: {', '.join(possibilidades)}{RESET}")
                else:
                    print(f"{AMARELO}Formato inválido para possibilidades. Use: ?COL,LIN (Ex: ?D,3){RESET}")
                comando_processado = True # Considera que o formato foi processado, mas inválido

            elif entrada_usuario.startswith('!'): # Comando para apagar um número.
                # Expressão regular para validar o formato '!COL,LIN' (ex: '!C,4').
                coincidencia = re.match(r'!\s*([A-Ia-i])\s*,\s*([1-9])\s*$', entrada_usuario)
                if coincidencia:
                    char_coluna, str_linha = coincidencia.groups()
                    coluna = converter_coluna_char_para_indice(char_coluna)
                    linha = int(str_linha) - 1
                    
                    # Validação das coordenadas.
                    if not (0 <= linha < 9 and 0 <= coluna < 9):
                        print(f"{AMARELO}Coordenadas inválidas. Coluna A-I, Linha 1-9.{RESET}")
                    elif (linha, coluna) in posicoes_pistas_iniciais:
                        print(f"{AMARELO}Não é possível apagar uma pista inicial!{RESET}")
                    elif tabuleiro_jogo_atual[linha][coluna] == 0:
                        print(f"{AMARELO}A célula já está vazia.{RESET}")
                    else:
                        tabuleiro_jogo_atual[linha][coluna] = 0 # Apaga o número (define como 0)
                        print(f"{VERDE}Valor apagado.{RESET}")
                else:
                    print(f"{AMARELO}Formato inválido para apagar. Use: !COL,LIN (Ex: !C,4){RESET}")
                comando_processado = True # Considera que o formato foi processado, mas inválido

            else: # Se não for 'sair', '?' ou '!', assume-se que é uma jogada de preenchimento.
                # Expressão regular para validar o formato 'COL,LIN: NUM' (ex: 'A,3: 7').
                coincidencia = re.match(r'\s*([A-Ia-i])\s*,\s*([1-9])\s*:\s*([1-9])\s*$', entrada_usuario)
                if coincidencia:
                    char_coluna, str_linha, str_numero = coincidencia.groups()
                    coluna = converter_coluna_char_para_indice(char_coluna)
                    linha = int(str_linha) - 1
                    numero = int(str_numero)

                    # Validação das coordenadas e do número.
                    if not (0 <= linha < 9 and 0 <= coluna < 9 and 1 <= numero <= 9):
                        print(f"{AMARELO}Jogada inválida: Coordenadas ou número fora do intervalo.{RESET}")
                    elif (linha, coluna) in posicoes_pistas_iniciais:
                        print(f"{AMARELO}Jogada inválida: Há uma Pista Inicial no lugar.{RESET}")
                    else:
                        valor_antigo = tabuleiro_jogo_atual[linha][coluna] # Salva o valor atual da célula
                        
                        sobrescrever_ok = True # Flag para controlar a sobrescrita
                        if valor_antigo != 0: # Se a célula já estiver ocupada por uma jogada do usuário.
                            print(f"{AMARELO}A célula já está ocupada com '{valor_antigo}'. Deseja sobrescrever (S/N)?{RESET}")
                            confirmar_sobrescrita_ok = False # Variável de controle para o loop de confirmação.
                            while not confirmar_sobrescrita_ok:
                                confirmacao = input().strip().lower()
                                if confirmacao == 's':
                                    confirmar_sobrescrita_ok = True # Sai do loop e procede com a jogada.
                                elif confirmacao == 'n':
                                    print(f"{AZUL}Sobrescrita cancelada.{RESET}")
                                    confirmar_sobrescrita_ok = True # Sai do loop de confirmação.
                                    sobrescrever_ok = False # Indica que a jogada foi cancelada
                                else:
                                    print(f"{AMARELO}Entrada inválida. Digite 'S' para sim ou 'N' para não.{RESET}")
                        
                        # e a lógica seguinte foi aninhada sob `if sobrescrever_ok`.
                        if sobrescrever_ok: # Procede com a jogada somente se a sobrescrita foi confirmada ou não era necessária
                            # Tenta fazer a jogada e valida.
                            tabuleiro_jogo_atual[linha][coluna] = numero # Coloca o número no tabuleiro.
                            if not validar_movimento(tabuleiro_jogo_atual, linha, coluna, numero):
                                tabuleiro_jogo_atual[linha][coluna] = valor_antigo # Reverte se a jogada for inválida.
                                print(f"{AMARELO}Jogada inválida.{RESET}")
                else:
                    print(f"{AMARELO}Comando inválido. Use COL,LIN: NUM, ?COL,LIN ou !COL,LIN. Digite 'sair' para encerrar.{RESET}")


def modo_batch(caminho_de_pistas_param, caminho_de_resolucao_param):
    global tabuleiro_original_pistas, tabuleiro_jogo_atual, posicoes_pistas_iniciais

    # Carrega o tabuleiro inicial
    tabuleiro_inicial, tabuleiro_jogo, posicoes_pistas = carregar_tabuleiro(caminho_de_pistas_param)
    if tabuleiro_inicial is None:
        print(f"{VERMELHO}Erro ao carregar o arquivo de pistas.{RESET}")
        return

    # Lista para armazenar jogadas inválidas
    jogadas_invalidas = []

    # Processa o arquivo de resolução
    try:
        with open(caminho_de_resolucao_param, 'r') as f:
            for num_linha, linha_conteudo in enumerate(f, 1): # Renomeado para evitar conflito com a variável `linha` da função `re.match`
                linha_conteudo = linha_conteudo.strip()
                
                if linha_conteudo: 
                    # Valida o formato da linha (ex: "A,1: 5")
                    coincidencia = re.match(r'\s*([A-Ia-i])\s*,\s*([1-9])\s*:\s*([1-9])\s*$', linha_conteudo)
                    
                    if coincidencia: 
                        char_coluna, str_linha, str_numero = coincidencia.groups()
                        coluna = converter_coluna_char_para_indice(char_coluna)
                        linha_num = int(str_linha) - 1  # Índice 0-based
                        numero = int(str_numero)

                        validar_jogada = True # Flag para determinar se a jogada deve ser aplicada

                        # Verifica coordenadas válidas
                        if not (0 <= linha_num < 9 and 0 <= coluna < 9):
                            jogadas_invalidas.append(f"A jogada {linha_conteudo} é inválida!'")
                            validar_jogada = False
                        
                        # Verifica se é uma pista inicial (não pode ser sobrescrita)
                        if validar_jogada and (linha_num, coluna) in posicoes_pistas: 
                            jogadas_invalidas.append(f"A jogada {linha_conteudo} é inválida!")
                            validar_jogada = False

                        # Valida a jogada
                        if validar_jogada and not validar_movimento(tabuleiro_jogo, linha_num, coluna, numero): 
                            jogadas_invalidas.append(f"A jogada {linha_conteudo} é inválida!")
                            validar_jogada = False

                        # Se passou todas as validações, aplica a jogada
                        if validar_jogada:
                            tabuleiro_jogo[linha_num][coluna] = numero
                    else: # Se não houver coincidência de formato
                        jogadas_invalidas.append(f"Linha {num_linha}: Formato inválido -> '{linha_conteudo}'")


    except FileNotFoundError:
        print(f"{VERMELHO}Erro: Arquivo de resolução não encontrado.{RESET}")
        return
    except Exception as e:
        print(f"{VERMELHO}Erro ao ler o arquivo de resolução: {e}{RESET}")
        return

    # Exibe o tabuleiro final
    exibir_tabuleiro(tabuleiro_jogo, posicoes_pistas)

    # Exibe jogadas inválidas (se houver)
    if jogadas_invalidas:
        for invalida in jogadas_invalidas:
            print(invalida)
    else:
        print(f"{VERDE}Todas as jogadas foram válidas!{RESET}")

    # Validação final do tabuleiro
    if validar_sudoku_completo(tabuleiro_jogo):
        print(f"{VERDE}A grade foi preenchida com sucesso!{RESET}")
    else:
        print(f"{AMARELO}A grade não foi preenchida!{RESET}")
    

def main():
    """
    Função principal do programa Sudoku.
    Controla o fluxo de execução baseado nos parâmetros da linha de comando.
    Decide entre Modo Interativo, Modo Solucionador ou Modo Batch.
    """
    numero_parametros = len(sys.argv) - 1 # Conta quantos argumentos foram passados (excluindo o nome do script).

    if numero_parametros == 0:
        # Modo de uso incorreto, nenhum parâmetro fornecido.
        print(f"{AMARELO}Modo de uso: python sudoku.py <arquivo_pistas.txt> OU python sudoku.py <arquivo_jogo.txt> <arquivo_saida.txt>{RESET}")
        sys.exit(1) # Encerra o programa com código de erro.
    elif numero_parametros == 1:
        caminho_arquivo_pistas = sys.argv[1]
        print("1. Modo Interativo")
        print("2. Modo Solucionador")
        
        escolha_valida = False # Variável de controle para o loop de escolha de modo.
        while not escolha_valida:
            escolha = input("Digite 1 ou 2: ").strip()
            if escolha == '1':
                modo_interativo(caminho_arquivo_pistas) # Chama a função do modo interativo.
                escolha_valida = True # Altera a condição para sair do loop.
            elif escolha == '2':
                # Carrega o tabuleiro para o modo solucionador.
                _tabuleiro_inicial, _tabuleiro_jogo, _posicoes_pistas_iniciais = carregar_tabuleiro(caminho_arquivo_pistas)
                if _tabuleiro_inicial is None: # Se houver erro ao carregar o tabuleiro, encerra.
                    print(f"{VERMELHO}Erro ao carregar o tabuleiro para o Modo Solucionador. Encerrando.{RESET}")
                    sys.exit(1)
                # Chama a função do modo solucionador, passando o tabuleiro e a função de exibição.
                modo_solucionador(_tabuleiro_inicial, _posicoes_pistas_iniciais, exibir_tabuleiro)
                escolha_valida = True # Altera a condição para sair do loop.
            else:
                print(f"{AMARELO}Opção inválida. Por favor, digite 1 ou 2.{RESET}")
        # A função main terminará quando 'escolha_valida' for True e o modo selecionado retornar.
    else: # Mais de um parâmetro (ou seja, 2 parâmetros para o Modo Batch).
        if numero_parametros == 2:
            # DOIS parâmetros: Ativa Modo Batch.
            caminho_de_pistas = sys.argv[1] # Primeiro parâmetro é o arquivo do jogo.
            caminho_de_resolucao = sys.argv[2] # Segundo parâmetro é o arquivo de saída.
            print(f"{AZUL}Modo Batch ativado.{RESET}")
            modo_batch(caminho_de_pistas, caminho_de_resolucao)
            # 'escolha_valida' não é mais necessária aqui, pois a função main está prestes a terminar
            # se o modo batch for executado.
        else:
            # Número de parâmetros inválido.
            print(f"{AMARELO}Número de parâmetros inválido. Use 1 ou 2 parâmetros.{RESET}")
        sys.exit(1) # Encerra o programa com código de erro.

# Garante que a função 'main()' seja chamada apenas quando o script for executado diretamente,
# e não quando for importado como um módulo em outro script.
if __name__ == "__main__":
    main()