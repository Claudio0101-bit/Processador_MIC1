'''
Comentários por Cláudio Pires Salgado

Arquivo: Functions.py

    Arquivo de código em Python voltado para a programação de funções auxiliares
    que serão utilizadas para os demais arquivos de código.

'''

# Função que recebe uma String de números e retorna um Array deles em inteiros
def str_to_array(str):
    if not str.isdigit():
        raise ValueError("String recebida em str_to_array() não contem apenas números.")
    return [int(i) for i in str]

# Função que recebe um Array de números e retorna uma String de todos eles
def array_to_str(arr):
    s = ''
    for i in arr:
        s += str(i)
    return s


# Função que recebe um número decimal e retorna uma
# Array de 8, 12 ou 16 inteiros (0 ou 1) que representa o número em Binário
def dec_to_arraybin(num, bits):

    # Se o número for negativo, ajusta para seu complemento em binário
    # assumindo o Sistema de Complemento de 2
    if num < 0:
        # Operador '<<' funciona como Deslocador para a Esquerda
        # (a << n) => a * 2^n
        num = (1 << bits) + num


    # Converte o número para uma String Binária
    s_b2 = bin(num & (2**bits - 1))[2:].zfill(bits)

    '''
    Explicação do Comando:
    --- Função bin() converte o número para String binária, mas sem bits extras 
    e começando a String com "0b", que é retirado pelo slice [2:].
    
    --- Operador & compara dois números bit a bit e retorna 1 apenas 
    se ambos os bits são 1, fazendo então uma comparação entre o número que se quer
    em binário e um número somente composto por 1, vulgo 2**bits - 1.
    
    --- Método .zfill(N)  preenche a string com zeros à esquerda para 
    que ela tenha pelo menos N caracteres.
    '''

    # Usar a String Binária para fazer o Array Binário
    arraybin = str_to_array(s_b2)

    # Retorno da função (Array Binário)
    return arraybin

# Função que recebe um Array Binário e retorna seu número decimal
def arraybin_to_dec(arraybin):

    # Usar o Array Binário para fazer a String Binária
    s_b2 = ''
    for i in range(len(arraybin)):
        s_b2 += str(arraybin[i])

    # Converte a String para Número Decimal (como se fosse positivo)
    num = int(s_b2, 2)


    # Se o bit mais à esquerda do Array Binário de 16 for 1,
    # é um valor negativo de uma variável
    if len(arraybin) == 16 and s_b2[0] == '1':
        # Ajustando para número negativo
        num = num - (1 << len(arraybin))

    # Retorno da função (Decimal)
    return num

# Função que realiza a soma da ULA (usando 2 Arrays Binários)
def soma_ULA(a, b):
    # Testando mesmo tamanho dos Arrays
    if len(a) != len(b):
        raise ValueError("Os Arrays da ULA não possuem mesmo tamanho.")

    # Resultado da Soma em Array Binário
    resultado = [0 for i in range(len(a))]
    # Variável para guardar o Carry (+1)
    carry = 0

    # Soma bit a bit dos Arrays Binários, da direita para a esquerda
    for i in range(len(a) - 1, -1, -1):
        soma = a[i] + b[i] + carry  # Soma
        resultado[i] = soma % 2  # Bit de Resultado
        carry = soma // 2  # 'Vai um' (carry)

    # Ignoramos Casos de Overflow (onde carry final = 1)
    # Retorno do Resultado
    return resultado

# Função de Inversão da ULA
def inv_ULA(a):

    # Invertendo os bits do Array dado
    a_inv = [1 - b for b in a]

    # Somando 1 usando Função de Soma da ULA
    mais1 = [0 for i in range(len(a))]
    mais1[-1] = 1

    return soma_ULA(a_inv, mais1)

def status_ULA(r):
    # Status D = [N, Z]
    d = [0,0]

    # Estado N
    if r[0] == 1:
        d[0] = 1
    # Estado Z
    if r == [0 for _ in range(len(r))]:
        d[1] = 1
    return d
