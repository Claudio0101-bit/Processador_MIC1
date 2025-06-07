'''
Comentários por Cláudio Pires Salgado

Arquivo: Componentes.py

    Arquivo de código em Python voltado para a programação de funções, classes e/ou
    variáveis que dizem respeito aos demais componentes presentes no Processador.
    que serão utilizadas para os demais arquivos de código.

'''

# Classe única referente aos Registradores do Processador
class Registradores:

    def __init__(self):
        # Registradores principais para Execução
        self.ac = 0 # Acumulador
        self.pc = 0 # Program Counter
        self.mpc = 0 # Micro Program Counter
        self.sp = 0 # Stack Pointer
        self.ir = 0 # Instrução atual
        self.mir = 0 # Micro-instrução atual

        # Registradores de Acesso à Memória Principal
        self.mar = 0 # Registrador de Endereços
        self.mbr = 0 # Registrador de Dados

        # Registradores auxiliares
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.ma1 = +1
        self.me1 = -1
        self.ze = 0

        ''' 
        Está faltando Latchs(A e B), AMUX e MMUX, AM e SM e Decoders(A,B,C).
        Eu (Cláudio) não lembro muito a teoria desses componentes, então devo revisar
        antes de implementá-los, mas com liberdade para quem quiser implementá-los.
        '''

# Classe referente à Unidade Lógica-Aritmética (ULA)
class ULA:

    # Operandos A e B (Talvez desnecessário)
    def __init__(self):
        self.a = 0
        self.b = 0

# Memória Principal (Uma lista de 4096 elementos, índice = endereço)
mp = []
for i in range(4096):
    mp.append("")

# Classe referente ao Deslocador
class Deslocador:

    # Um único Operando (Talvez desnecessário)
    def __init__(self):
        self.a = 0

