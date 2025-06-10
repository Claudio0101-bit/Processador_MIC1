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

    # Setters dos dois Operandos da ULA
    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def set(self, a, b):
        self.a = a
        self.b = b

    # Função de Execução da ULA com base na condição dada pela UC
    def executar(self, cond):

        # 00 -> Sem desvios e sem condicionais
        if cond == "00":
            return self.a + self.b

        # 01 -> Desvio se Resultado for Negativo
        if cond == "01" and (self.a + self.b) < 0:
            pass

        # 10 -> Desvio se Resultado for Zero
        if cond == "10" and (self.a + self.b) == 0:
            pass

        # 11 -> Desvio sem condicionais
        if cond == "11":
            pass


# Memória Principal (Uma lista de 4096 elementos, índice = endereço)
mp = []
for i in range(4096):
    mp.append("")

# Classe referente ao Deslocador
class Deslocador:

    # Um único Operando (Talvez desnecessário)
    def __init__(self):
        self.a = 0

    def set(self, a):
        self.a = a

    # Função de Deslocamento de 1 bit do Descolador com base na condição dada pela UC
    def deslocar(self, cond):

        if cond == "0":
            return self.a

        if cond == "1":
            return self.a << 1
