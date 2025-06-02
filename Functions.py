'''
Comentários por Cláudio Pires Salgado

Arquivo: Functions.py

    Arquivo de código em Python voltado para a programação de funções auxiliares
    que serão utilizadas para os demais arquivos de código.

'''

# Função que recebe um número decimal e retorna uma
# String de 8 ou 12 caracteres que representa o número em Binário
def b10_to_b2(num, bits):

    # Se o número for negativo, ajusta para seu complemento em binário
    # assumindo o Sistema de Complemento de 2
    if num < 0:
        # Operador '<<' funciona como Deslocador para a Esquerda
        # (a << n) => a * 2^n
        num = (1 << bits) + num

    # Converte o número para binário
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
    # Retorno da função
    return s_b2

# Função que recebe uma String binária de 8 ou 12 caracteres
# e retorna seu número decimal
def b2_to_b10(s_b2, bits):
    # Converte a String para Número Decimal (como se fosse positivo)
    num = int(s_b2, 2)

    # Se o bit mais à esquerda (MSB) 1, é um número negativo
    if s_b2[0] == '1':
        # Ajustando para número negativo
        num = num - (1 << bits)

    return num

# Testando
print(b2_to_b10('00000101', 8))    # 5
print(b2_to_b10('11111011', 8))    # -5
print(b2_to_b10('000000000101', 12)) # 5
print(b2_to_b10('111111111011', 12)) # -5







