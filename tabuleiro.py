grade = [
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x']
]

linhas = {1: grade[0], 2: grade[1], 3: grade[2], 4: grade[3], 5: grade[4], 6: grade[5], 7: grade[6], 8: grade[7], 9: grade[8]}


def tabuleiro():
    letras = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I'}    # Para as letras das colunas

    print('\n     | ',end='')
    for i in range(0, 9, 3):    # Esse for imprime a primeira linha, correspondente a numeração das colunas
        print(letras[i + 1] + ' | ', end='')
        print(letras[i + 2] + ' | ', end='')
        print(letras[i + 3] + ' || ', end='')
    print('\n  ++-------------++-----------++-----------++ ')

    # Esse for imprime as linhas do tabuleiro, separando cada a 3 colunas com || e a cada 3 linhas com ++--...--++
    for i in range(9):
        print(str(i + 1) + ' ||', '|' + f' {linhas[i+1][0]} | {linhas[i+1][1]} | {linhas[i+1][2]} || {linhas[i+1][3]} | {linhas[i+1][4]} | {linhas[i+1][5]} || {linhas[i+1][6]} | {linhas[i+1][7]} | {linhas[i+1][8]} ||', i + 1)
        if ((i + 1) % 3 == 0):
            print('  ++-------------++-----------++-----------++ ')

    # Aqui imprimimos a última linha (igual a primeira), correspondente a numeração das colunas
    print('     | ',end='')
    for i in range(0, 9, 3):
        print(letras[i + 1] + ' | ', end='')
        print(letras[i + 2] + ' | ', end='')
        print(letras[i + 3] + ' || ', end='')

    print('\n')

tabuleiro()

game = True
while (game == True): 
    col, lin = map(int, input('col e lin: ').split())
    while (col < 1 or col > 9 or lin < 1 or lin > 9):    # verifica se a coluna e linha estão entre 1 e 9
        print('Coluna e linha devem ser números entre 1 e 9.')
        col, lin = map(int, input('col e lin: ').split())
    
    num = int(input('número 1-9: '))
    while (num < 1 or num > 9):    # verifica se o número está entre 1 e 9
        print('O número deve ser de 1 a 9.')
        num = int(input('número 1-9: '))

    for elemento in linhas[lin]: # verifica se o número já não está na linha.
        while num == elemento or num < 1 or num > 9:
            if num == elemento:
                print("Jogada Inválida")
                num = int(input('número 1-9: '))
            elif num < 1 or num > 9:
                print('O número deve ser de 1 a 9.')
                num = int(input('número 1-9: '))
    
    for i in range(9): # verifica se o númer já não está na coluna.
        while grade[i][col - 1] == num or num < 1 or num > 9:
            if num == grade[i][col - 1]:
                print("Jogada Inválida")
                num = int(input('número 1-9: '))
            elif num < 1 or num > 9:
                print('O número deve ser de 1 a 9.')
                num = int(input('número 1-9: '))

    for i in range(9):
        if col == i + 1:
            for j in range(9):
                if lin == j + 1:
                    linhas[j + 1][i] = num

    tabuleiro()
