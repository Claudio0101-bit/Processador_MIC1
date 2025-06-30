'''
Comentários por Cláudio Pires Salgado

Arquivo: Componentes.py

    Arquivo de código em Python voltado para a programação de funções, classes e/ou
    variáveis que dizem respeito aos demais componentes presentes no Processador
    que serão utilizadas para os demais arquivos de código.

'''

from Functions import *

# Classe única referente aos Registradores do Processador
class Registradores:

    def __init__(self):
        '''
        Lista dos Registradores da Via de Dados da ULA: recebem valores vindos do Deslocador
        e jogam seus valores para um dos Latchs (A e B)
        '''
        self.regs = [
        dec_to_arraybin(0,16),  # 0 -> PC: Program Counter
        [],  # 1 -> AC: Acumulador
        dec_to_arraybin(4095,16),  # 2 -> SP: Stack Pointer
        [],  # 3 -> IR: Instruction Register
        [],  # 4 -> TIR:
        dec_to_arraybin(0,16),  # 5 -> Zero (0)
        dec_to_arraybin(1,16),  # 6 -> Mais-um (+1)
        dec_to_arraybin(-1,16),  # 7 -> Menos-um (-1)
        [],  # 8 -> AM: AMASK
        [],  # 9 -> SM: SMASK
        [],  # 10 -> A
        [],  # 11 -> B
        [],  # 12 -> C
        [],  # 13 -> D
        [],  # 14 -> E
        []   # 15 -> F
        ]
        '''
            Registradores de Acesso à Memória Principal: 
        MAR: recebe valor apenas de Latch B, guarda bit da UC
        MBR: recebe valor do Deslocador e joga valor para AMUX, guarda bit da UC 
        '''
        self.mar = (0,[])  # Registrador de Endereços (Memory Adress Register)
        self.mbr = (0,[])  # Registrador de Dados (Memory Buffer Register)

        '''
            Registradores de transição, associados à ULA:
        Latch A: recebe valor dos Registradores e joga para AMUX
        Latch B: recebe valor dos Registradores e joga para MAR ou para ULA
        AMUX: decide entre valor ou de Latch A ou de MBR e joga para ULA
        '''
        self.latchA = []
        self.latchB = []
        self.AMUX = [0, []]
        '''
            Registradores da Via de Dados da UC
        MPC: guarda endereço para  acessar Micro-programa da Memória de Controle
        MIR: recebe Microinstrução em Binário da Memória de Controle
        MMUX: decide entre MPC incrementado ou endereço de desvio ADDR para passar para MPC 
        '''
        self.mpc = dec_to_arraybin(0,8)  # MPC: Micro Program Counter
        self.mir = dec_to_arraybin(0,32)  # MIR: Micro Instruction Register

        # Valores do MMUX: Bit da Caixa Lógica, MPC incrementado, ADDR e Índice decisivo
        self.MMUX = 0  # MMUX


    # Função que definirá o valor de AMUX (valor de Latch A ou de MBR)
    # Cond = 0 -> AMUX = Latch A
    # Cond = 1 -> AMUX = MBR
    def valor_AMUX(self):
        if self.AMUX[0] == 0:
            self.AMUX[1] = self.latchA
        if self.AMUX[0] == 1:
            self.AMUX[1] = self.mbr[1]

    # Função que definirá o valor de MMUX (MPC + 1 ou ADDR)
    # Cond_log = 0 -> MMUX = MPC + 1
    # Cond_log = 1 -> MMUX = ADDR
    def valor_MMUX(self):
        if self.MMUX == 0:
            self.mpc = soma_ULA(self.mpc, self.regs[6])
        if self.MMUX == 1:
            self.mpc = self.mir[24:]

    # Função que definirá o valor do AMASK
    # (retira os 4 primeiros bits, referentes a Instrução, sobrando os bits de enderço)
    def valor_AMASK(self):
        self.regs[8] = [0,0,0,0] + self.regs[8][4:]

    # Função que definirá o valor do AMASK
    # (retira os 8 primeiros bits, referentes a INSP e DESP, sobrando os bits de valor)
    def valor_SMASK(self):
        self.regs[9] = [0 for _ in range(8)] + self.regs[9][9:]

# Classe referente à Unidade Lógica-Aritmética (ULA)
class ULA:

    def __init__(self):
        self.a = []  # Operando A
        self.b = []  # Operando B
        self.f = []  # Operação F
        self.r = []  # Resultado R
        self.d = [0, 0]  # Status D = [N, Z]

        # Estado N (Se o resultado é Negativo, 1° bit é 1)
        # Estado Z (Se o resultado é Zero, Array de 0's)

    # Setters da ULA
    def setA(self, a):
        self.a = a

    def setB(self, b):
        self.b = b

    def setOps(self, a, b):
        self.a = a
        self.b = b

    # Setter da Operação
    def setF(self, f):
        self.f = f

    # Função de Execução da ULA com base em:
    # Operação F (em Array) dada pela UC (pelo registrador MIR)
    def executar(self):

        # F = 00 -> SOMA
        if self.f == [0, 0]:
            self.r = soma_ULA(self.a, self.b)

            # return self.r

        # F = 01 -> AND
        if self.f == [0, 1]:
            for i in range(len(self.a)):
                if self.a[i] == 1 and self.b[i] == 1:
                    self.r[i] = 1
                else:
                    self.r[i] = 0

            # return self.r

        # F = 10 -> IDENTIDADE (A)
        if self.f == [1, 0]:
            self.r = self.a

            # return self.r

        # F = 11 -> INVERTER A
        if self.f == [1, 1]:
            self.r = inv_ULA(self.a)

            # return self.r

        # Verificando Status D = [N, Z]
        self.d = status_ULA(self.r)

# Memória Principal = MP
# Endereços de 12 bits, ou seja, 2**12 = 4096 endereços
# Palavras de 16 bits em forma de Array Binário
mp = []
for i in range(2**12):
    mp.append([0 for _ in range(16)])


# Classe referente ao Deslocador
class Deslocador:

    # Um único Operando
    # Condição dada pela UC
    def __init__(self):
        self.a = []
        self.cond = []

    def set(self, a):
        self.a = a

    # Função de Deslocamento de 1 bit do Descolador com base na condição dada pela UC
    def deslocar(self):

        if self.cond == [0,0]:  # Retornar o número (Array Binário) inalterado
            self.a = self.a

        if self.cond == [1,0]:  # Deslocar um bit para a esquerda
            if not all(b in (0, 1) for b in self.a):
                raise ValueError("Array do Deslocador [Função deslocar()] não corresponde a um Array Binário.")

            if len(self.a) == []:
                self.a = []

            # Remove o primeiro bit (mais significativo) e adiciona um 0 no final
            self.a = self.a[1:] + [0]

# Classe referente aos Decoders
# Barramentos/Decoders A e B escolherão os registradores usados como Operandos
# Barramento/Decoder C escolherá onde o resultado será gravado (se for gravado)
class Decoders:
    def __init__(self):
        self.a = []  # 4 bits (0 a 15) pra escolher entre os Regs da Via de Dados
        self.b = []  # 4 bits (0 a 15) pra escolher entre os Regs da Via de Dados
        self.c = []  # 5 bits => 4 para escolher o Reg e 1(1°) para dizer se vai ser gravado

# Classe referente ao Relógio para temporização em Ciclos e Subciclos
# 1 Ciclo = 4 Subciclos
class Clock:
    def __init__(self):
        self.ciclo_atual = 0
        self.subciclo_atual = 0

        self.intervalo = 1000
        self.paused = True
        self.autoexec = False

        # trocar as funções lambda pelas funções de subciclo
        self.subciclos = [
            lambda: print("chamar subciclo 1"),
            lambda: print("chamar subciclo  2"),
            lambda: print("chamar subciclo   3"),
            lambda: print("chamar subciclo    4")
        ]

    def avanca_subciclo(self):
        self.subciclo_atual += 1
        if self.subciclo_atual == 4:
            self.subciclo_atual = 0
        # chamada da sub-rotina de subciclo
        self.subciclos[self.subciclo_atual-1]()

    def atualiza_intervalo(self, vars):
        if not self.autoexec and vars.intervalo.get().isdigit():
            self.intervalo = int(vars.intervalo.get())

    def pausa_clock(self):
        self.paused = True

    def despausa_clock(self):
        self.paused = False

    # coloca o clock em um estado que chama sem intervalos as
    # funções de subciclo, só é possível sair desse estado ao
    # término do programa, mas essa verificação não é feita ainda
    def executa_tudo(self):
        self.paused = False
        self.intervalo = 0
        self.autoexec = True
	    
# Classe referente à caixa "Lógica para o Controle de Fluxo"
# Recebe Status D da ULA e COND do MIR
# Retorna o valor que definirá se ocorre desvio ou não
class CaixaLogica:
    def __init__(self):
        self.d = []
        self.COND = []
        self.retorno = 0

    def setCOND(self, cond):
        self.COND = cond

    def setD(self, d):
        self.d = d

    # Função que define retorno lógico que define valor de MMUX
    def logicar(self):
        if self.COND == [0,0]:
            self.retorno = 0

        if self.COND == [0,1] and self.d[0] == 1:
            self.retorno = 1
        else:
            self.retorno = 0

        if self.COND == [1,0] and self.d[1] == 1:
            self.retorno = 1
        else:
            self.retorno = 0

        if self.COND == [1,1]:
            self.retorno = 1

# Memória de Controle
# Contém as 79 Microinstruções em Binário (32 bits) seguindo a seguinte ordem:
'''
Respectivos Componentes que recebem suas respectivas quantidades de bits (ordenados)
AMUX / COND / ULA / DESL / MBR / MAR / RD / WR / EnC / Bar.C / Bar.B / Bar.A / ADDR
  1     2      2     2      1     1    1    1    1       4       4       4       8
 (0)/ (1,2)/ (3,4)/ (5,6)/ (7)/  (8)/ (9) /(10) /(11) /(12-15)/(16-19)/(20-23)/(24-31)
'''
mc = (
#                            	    1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3
#        	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        	[0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 0
		[0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 1
		[1,0,1,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],  # 2
		[0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,0,0,1,1],  # 3
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1],  # 4
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1],  # 5
		[0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],  # 6
		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 7
		[1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 8
		[0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0],  # 9
		[0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  # 10
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1],  # 11
		[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0], # 12
		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 13
		[1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0], # 14
		[0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0], # 15
		[0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0], # 16
		[1,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 17
		[0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0], # 18
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1], # 19
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1], # 20
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0], # 21
		[0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0], # 22
		[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0], # 23
		[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 24
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,1,1], # 25
		[0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0], # 26
		[0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0], # 27
		[0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,0,1,0,0,0], # 28
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1], # 29
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], # 30
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0], # 31
		[0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1], # 32
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0], # 33
		[0,1,1,1,0,0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0], # 34
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0], # 35
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0], # 36
		[0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1], # 37
		[0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0], # 38
		[0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0], # 39
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,1,0], # 40
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0], # 41
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0], # 42
		[0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 43
		[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0], # 44
		[0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0], # 45
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0], # 46
	    	[0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0], # 47
		[0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0], # 48
		[0,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0], # 49
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1], # 50
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,1,1], # 51
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0], # 52
		[0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0], # 53
		[0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0], # 54
		[0,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0], # 55
		[0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0], # 56
		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 57
		[0,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0], # 58
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0], # 59
		[0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0], # 60
		[0,1,1,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0], # 61
		[0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0], # 62
		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 63
		[1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 64
		[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1], # 65
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1,0], # 66
		[0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0], # 67
		[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 68
		[1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # 69
		[0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0], # 70
		[0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0], # 71
		[0,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0], # 72
		[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0],  # 73
		[0,0,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0],  # 74
		[0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0],  # 75
		[0,0,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0],  # 76
		[0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0],  # 77
		[0,1,1,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,1,1]  # 78
)
