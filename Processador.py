from Componentes import *
from Functions import arraybin_to_dec


class Processador:

    def __init__(self):
        self.regis = Registradores()
        self.ula = ULA()
        self.deslocador = Deslocador()
        self.mp = mp
        self.mc = mc
        self.decoders = Decoders()
        self.logica = CaixaLogica()
        self.interface = None

    def subciclo_1(self):
        # ======================== Subciclo 1: Busca da Instrução ========================

        # MIR pega Microinstrução da MC pelo MPC
        self.regis.mir = self.mc[arraybin_to_dec(self.regis.mpc)]

        # Demais Componentes recebem Bits de MIR
        self.regis.AMUX[0] = self.regis.mir[0]
        self.logica.COND = self.regis.mir[1:3]
        self.ula.f = self.regis.mir[3:5]
        self.deslocador.cond = self.regis.mir[5:7]

        # self.regis.mbr[0] = self.regis.mir[7]
        # self.regis.mar[0] = self.regis.mir[8]

        # Bits 9 e 10 -> RD e WR
        self.decoders.c = self.regis.mir[11:16]
        self.decoders.b = self.regis.mir[16:20]
        self.decoders.a = self.regis.mir[20:24]
        # Bits 24 até 31 -> ADDR


    def subciclo_2(self):
        # ======================== Subciclo 2: Identificação da Intrução ========================

        # Latchs recebem valores de Registradores da Via de Dados
        self.regis.latchA = self.regis.regs[arraybin_to_dec(self.decoders.a)]
        self.regis.latchB = self.regis.regs[arraybin_to_dec(self.decoders.b)]


        # Calculado valor de AMUX:
        self.regis.valor_AMUX()

    def subciclo_3(self):
        # ======================== Subciclo 3: Realização da Operação ========================

        # ULA recebe Operandos A e B e executa Operação
        self.ula.setA(self.regis.AMUX[1])
        self.ula.setB(self.regis.latchB)
        self.ula.executar()

        # Deslocador recebe Resultado da ULA e realiza Operação
        self.deslocador.set(self.ula.r)
        self.deslocador.deslocar()

        # Caixa Lógica recebe Status D, realiza lógica e manda para MMUX
        # MMUX já determina próximo valor de MPC
        self.logica.setD(self.ula.d)
        self.logica.logicar()
        self.regis.MMUX = self.logica.retorno
        #print("MMUX:", self.regis.MMUX)
        self.regis.valor_MMUX()
        #print("MPC:", self.regis.mpc, "- i:", arraybin_to_dec(self.regis.mpc))
        
        
        # Bit para MAR = 1 -> MAR := Valor de LatchB
        if self.regis.mir[8] == 1:
            #rint("Entrou no Bit do MAR")
            #print("MIR:", self.regis.mir)
            self.regis.mar = self.regis.latchB
            #print("MAR:", self.regis.mar)
            

        # RD = 1 -> MBR := MP[MAR] (Leitura da Memória Principal)
        if self.regis.mir[9] == 1:
            self.regis.mbr = self.mp[arraybin_to_dec(self.regis.mar[4:])]

    def subciclo_4(self):
        # ======================== Subciclo 4: Gravação do resultado ========================

        # Diferentes Gravações de Resultados
        
        # Bit para MBR = 1 -> MBR := Valor de Deslocador
        if self.regis.mir[7] == 1:
                self.regis.mbr = self.deslocador.a

        # WR = 1 -> MP[MAR] := MBR (Escrita na Memória)
        if self.regis.mir[10] == 1:
            #print("Onde deu Erro")
            #print("MAR:", self.regis.mar)
            index = arraybin_to_dec(self.regis.mar[4:])
            self.mp[index] = self.regis.mbr

            # atualizar na interface
            self.interface.regs_and_mem.edit_row(self.interface.regs_and_mem.memor_table, index, arraybin_to_dec(self.regis.mbr), "memoria")

        # En.C = 1 -> Registrador[Decoder C] := Valor de Deslocador
        if self.regis.mir[11] == 1:
            self.regis.regs[arraybin_to_dec(self.decoders.c[1:])] = self.deslocador.a
