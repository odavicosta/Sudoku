def validar_1(grade, num):
    for i in range(3):
        for j in range(3):
            if (grade[i][j] == num):
                inválido = True
                print('Número já existe no quadrante 1.')
                while (inválido == True):
                    num = int(input('número 1-9: '))
                    while (num < 1 or num > 9):
                        print('O número deve ser de 1 a 9.')
                        num = int(input('número 1-9: '))
                    if (grade[i][j] != num):
                        inválido = False

                    
def adicionar_numero(col, lin, num, linhas):
    for i in range(9):
        if col == i + 1:
            for j in range(9):
                if lin == j + 1:
                    linhas[j + 1][i] = num

export = {validar_1, adicionar_numero}