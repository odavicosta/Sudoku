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
        print(str(i + 1) + ' ||', '|' + ' X | X | X ||'*3, i + 1)
        if ((i + 1) % 3 == 0):
            print('  ++-------------++-----------++-----------++ ')

    # Aqui imprimimos a última linha (igual a primeira), correspondente a numeração das colunas
    print('     | ',end='')
    for i in range(0, 9, 3):
        print(letras[i + 1] + ' | ', end='')
        print(letras[i + 2] + ' | ', end='')
        print(letras[i + 3] + ' || ', end='')

tabuleiro()
