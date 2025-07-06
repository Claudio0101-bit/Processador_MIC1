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
no formato: FLAG: INSTRUÇÃO VALOR/VARIÁVEL
'''
# Exemplos de Prog
prog = ["LODD n","SUBD i","JNEG saída","LODD i","SUBD n","JZER dentro",
        "JPOS saída","LOCO a","ADDD i","PSHI","POP","STOD m"]

prog2 = ["START: LOCO 16",
            "STOD var1",
            "LOCO 1",
            "STOD var2",
            "LOCO 0",
            "PUSH",
            "LOCO 1",
            "PUSH",
            "LOOP: LODL 1",
            "ADDL 0",
            "PUSH",
            "LODD var1",
            "SUBD var2",
            "STOD var1",
            "JZER END",
            "JUMP LOOP",
            "END: JUMP END"]
def gerar_e_compilar(prog, mp):

    # Lista com Linhas do Programa Compiladas (em Array de Arrays Binários)
    compilado = []

    # Dicionário para Flags, no formato 'Nome': Endereço
    flags = {}

    # Dicionário de Tuplas para Variáveis, no formato 'Nome': (Valor, Endereço)
    variaveis = {}

    # Analisando o Programa dado
    for i in range(len(prog)):

        # c -> Lista de Strings divididas de cada Linha do Programa
        c = prog[i].split(" ")

        # Tratando Instruções que não possuem Valores
        if len(c) == 1:
            mp[i] = str_to_array(inst[c[0]])
            compilado.append(mp[i])
            continue

        # Identificando se há uma Flag antes da Instrução e armazenando-a
        if ":" in c[0] and len(c) == 3:
            flags[c[0][:len(c[0]) - 1]] = i
            # Dúvida: Guardar End. de Flag já como Array Binário?
            # Se sim, i -> dec_to_arraybin(i, 12)

        # Identificando se há uma Variável ou Flag na Instrução
        not_number = c[-1].isidentifier()
        bits = 12
        # Identificando se é uma Instrução cujo Valor é de 8 bits
        if c[-2] in ("INSP", "DESP"):
            bits = 8

        # Caso com Variável ou Flag - Reservar Próximos Endereços na MP logo após Programa
        if not_number == True:

            # Tratando Casos em que Variável já foi utilizada
            if c[-1] in variaveis.keys():
                for nome_var in variaveis.keys():
                    if c[-1] == nome_var:
                        mp[i] = str_to_array(inst[c[-2]]) + dec_to_arraybin(variaveis[nome_var][1], bits)
                        compilado.append(mp[i])
                        break

            # Tratando Casos de Primeiro uso de uma Variável
            elif not c[-1].isupper():
                mp[i] = str_to_array(inst[c[-2]]) + dec_to_arraybin(len(prog) + len(variaveis), bits)
                compilado.append(mp[i])
                variaveis[c[-1]] = (0, len(prog) + len(variaveis))

            # Tratando Casos de Flags com Endereços já registrados
            if c[-1] in flags.keys():
                for nome_flag in flags.keys():
                    if c[-1] == nome_flag:
                        mp[i] = str_to_array(inst[c[-2]]) + dec_to_arraybin(flags[nome_flag], bits)
                        compilado.append(mp[i])
                        break

            # Tratando Casos de Flags ainda não registradas
            else:
                for _ in range(i, len(prog)):
                    if c[-1] + ":" in prog[_]:
                        flags[c[-1]] = _
                        mp[i] = str_to_array(inst[c[-2]]) + dec_to_arraybin(_, bits)
                        break

        # Caso sem Variável ou Flag - Apenas Instrução e Valor
        else:

            mp[i] = str_to_array(inst[c[-2]]) + dec_to_arraybin(int(c[-1]), bits)
            compilado.append(mp[i])
        print(i)

    # Retornando Lista do Programa Compilado, Dicionário de Variáveis e Lista de Flags
    return compilado, variaveis, flags

# Testando se a Função está funcionando com Prog2
compilado, variaveis, flags = gerar_e_compilar(prog2,mp)

print("Variáveis geradas: ", variaveis)
print("-------------------------------------------------")
print("MP:")
for i in range(len(prog2) + len(variaveis)):
    print(i, " : ", mp[i])
print("-------------------------------------------------")
print("Compilado: ")
for i in compilado:
    print(i)
print("Len(Compilado): ", len(compilado))
print("-------------------------------------------------")
print("Flags: ", flags)
