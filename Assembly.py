'''
Comentários por Cláudio Pires Salgado

Arquivo: Assembly.py

    Arquivo de código em Python voltado para a programação da
    leitura das Macroinstruções da ISA MIC-1, lidas pela Interface
    Gráfica, e o processamento dessas instruções

'''
from ISA_MIC1 import inst
from Componentes import *
from Functions import *

# Protótipo de Função de Compilação e Geração na MP
'''
Assumindo o Parâmetro 'prog' como uma lista de Strings
onde cada String corresponde a uma linha do Macro-Programa,
no formato: INSTRUÇÃO VALOR/VARIÁVEL
'''

def gerar_e_compilar(prog):

    # Armazenando quantidade de Variáveis no Programa
    quant = 0

    # Lista com Linhas do Programa Compiladas (em Binário)
    compilado = []

    # Lista de Tuplas com Nome e Endereço de Variáveis
    variaveis = []

    # Lista apenas com nomes de Variáveis para Verificação de Re-uso
    nomes_var = []

    for i in range(len(prog)):
        campos = prog[i].split(" ")

        # Tratando Instruções que não possuem Valores
        if len(campos) == 1:
            mp[i] = inst[campos[0]]
            compilado.append(mp[i])
            continue

        # Identificando se há uma Variável na Instrução
        var = campos[1].isidentifier()
        bits = 12

        # Caso com Variável - Reservar Próximo Endereço na MP logo após Programa
        if var == True:

            # Tratando Casos em que variável já foi utilizada
            if campos[1] in nomes_var:
                for j in variaveis:
                    if campos[1] == j[0]:
                        mp[i] = inst[campos[0]] + b10_to_b2(j[1], bits)
                        compilado.append(mp[i])
                        break
            # Tratando Casos de primeiro uso de uma variável
            else:
                mp[i] = inst[campos[0]] + b10_to_b2(len(prog) + quant, bits)
                compilado.append(mp[i])
                variaveis.append((campos[1], len(prog) + quant))
                nomes_var.append(campos[1])
                quant += 1


        # Caso sem Variável - Apenas Instrução e Valor
        else:
            # Identificando se é uma Instrução cujo Valor é de 8 bits
            if campos[0] in ("INSP","DESP"):
                bits = 8
            mp[i] = inst[campos[0]] + b10_to_b2(campos[1], bits)

            compilado.append(mp[i])

    # Retornando Lista do Programa Compilado e Lista de Variáveis
    return compilado, variaveis
