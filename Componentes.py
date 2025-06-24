'''
Comentários por Cláudio Pires Salgado

Arquivo: Componentes.py

    Arquivo de código em Python voltado para a programação de funções, classes e/ou
    variáveis que dizem respeito aos demais componentes presentes no Processador.
    que serão utilizadas para os demais arquivos de código.

'''

from Functions import soma_ULA, inv_ULA

# Classe única referente aos Registradores do Processador
class Registradores:

    def __init__(self):
        '''
        Registradores da Via de Dados da ULA: recebem valores vindos do Deslocador
        e jogam seus valores para um dos Latchs (A e B)
        '''
        self.pc = 0  # Program Counter
        self.ac = 0  # Acumulador
        self.sp = 0  # Stack Pointer
        self.ir = 0  # Instrução atual
        self.tir = 0
        self.ze = 0  # Registrador 0
        self.ma1 = +1  # Registrador +1
        self.me1 = -1  # Registrador -1
        self.am = 0  # AMASK
        self.sm = 0  # SMASK
        # Registradores Auxiliares (de A a F)
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0

        '''
            Registradores de Acesso à Memória Principal: 
        MAR: recebe valor apenas de Latch B
        MBR: recebe valor do Deslocador e joga valor para AMUX 
        '''
        self.mar = 0  # Registrador de Endereços (Memory Adress Register)
        self.mbr = 0  # Registrador de Dados (Memory Buffer Register)

        '''
            Registradores de transição, associados à ULA:
        Latch A: recebe valor dos Registradores e joga para AMUX
        Latch B: recebe valor dos Registradores e joga para MAR ou para ULA
        AMUX: recebe valor ou de Latch A ou de MBR e joga para ULA
        '''
        self.latchA = 0
        self.latchB = 0
        self.AMUX = 0

        '''
        Registradores da Via de Dados da UC
        '''
        self.mpc = 0  # Micro Program Counter
        self.mir = 0  # Micro-instrução atual
        self.MMUX = 0  # MMUX


    # Função que definirá o valor de AMUX (valor de Latch A ou de MBR)
    def valor_AMUX(self, cond):
        pass


        ''' 
        Está faltando Decoders(A,B,C).
        Eu (Cláudio) não lembro muito a teoria desses componentes, então devo revisar
        antes de implementá-los, mas com liberdade para quem quiser implementá-los.
        '''

# Classe referente à Unidade Lógica-Aritmética (ULA)
class ULA:

    # Operandos A e B (Talvez desnecessário)
    def __init__(self):
        self.a = []
        self.b = []

    # Setters dos dois Operandos da ULA
    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def set(self, a, b):
        self.a = a
        self.b = b

    # Função de Execução da ULA com base na condição F (em Array) dada pela UC
    def executar(self, f):

        # 00 -> SOMA --- Sem desvios e sem condicionais
        if f == [0, 0]:
            return soma_ULA(self.a, self.b)

        # 01 -> AND --- Desvio se Resultado for Negativo
        if f == [0, 1] and (self.a + self.b) < 0:
            pass

        # 10 -> IDENTIDADE (A) --- Desvio se Resultado for Zero
        if f == [1, 0] and (self.a + self.b) == 0:
            return self.a

        # 11 -> INVERTER A --- Desvio sem condicionais
        if f == [1, 1]:
            return inv_ULA(self.a)


# Memória Principal (Uma lista de 4096 elementos, índice = endereço)
# Palavras de 16 bits em forma de Array Binário
mp = []
for i in range(4096):
    mp.append([0 for _ in range(16)])

# Classe referente ao Deslocador
class Deslocador:

    # Um único Operando (Talvez desnecessário)
    def __init__(self):
        self.a = []

    def set(self, a):
        self.a = a

    # Função de Deslocamento de 1 bit do Descolador com base na condição dada pela UC
    def deslocar(self, cond):

        if cond == 0:  # Retornar o número (Array Binário) inalterado
            return self.a

        if cond == 1:  # Deslocar um bit para a esquerda
            if not all(b in (0, 1) for b in self.a):
                raise ValueError("Array do Deslocador [Função deslocar()] não corresponde a um Array Binário.")

            if len(self.a) == []:
                return []

            # Remove o primeiro bit (mais significativo) e adiciona um 0 no final
            return self.a[1:] + [0]
