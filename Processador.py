from Componentes import *
from Assembly import gerar_e_compilar

class Processador:

    def __init__(self):
        self.regis = Registradores()
        self.ula = ULA()
        self.deslocador = Deslocador()
        self.mp = mp
        self.mc = mc
        self.decoders = Decoders()
        self.logica = CaixaLogica()


    def EXECUTAR(self):
        
        while (True):
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

            # ======================== Subciclo 2: Identificação da Intrução ========================

            # Latchs recebem valores de Registradores da Via de Dados
            self.regis.latchA = self.regis.regs[arraybin_to_dec(self.decoders.a)]
            self.regis.latchB = self.regis.regs[arraybin_to_dec(self.decoders.b)]

            # Calculado valor de AMUX:
            self.regis.valor_AMUX()
            
            # ULA recebe Operandos A e B e executa Operação
            self.ula.setA(self.regis.AMUX[1])
            self.ula.setB(self.regis.latchB)
            self.ula.executar()

            # Caixa Lógica recebe Status D, realiza lógica e manda para MMUX
            # MMUX já determina próximo valor de MPC
            self.logica.setD(self.ula.d)
            self.logica.logicar()
            self.regis.MMUX = self.logica.retorno
            self.regis.valor_MMUX()

            # Deslocador recebe Resultado da ULA e realiza Operação
            self.deslocador.set(self.ula.r)
            self.deslocador.deslocar()

            # ======================== Subciclo 3: Realização da Operação ========================

            

            # ======================== Subciclo 4: Gravação o resultado ========================

            # Diferentes Gravações de Resultados
            # RD = 1 
            if self.regis.mir[9] == 1:
                
                # Bit para MAR = 1 -> MAR := Valor de LatchB 
                if self.regis.mir[8] == 1:
                    self.regis.mar = self.regis.latchB
                    self.regis.mbr = self.mp[arraybin_to_dec(self.regis.mar)]
                
            # WR = 1 
            if self.regis.mir[10] == 1:
                
                # Bit para MBR = 1 -> MBR := Valor de Deslocador
                # MP[MAR] := MBR
                if self.regis.mir[7] == 1:
                    self.regis.mbr = self.deslocador.a
                    self.mp[arraybin_to_dec(self.regis.mar)] = self.regis.mbr
                    
            # En.C = 1 -> Registrador[Decoder C] := Valor de Deslocador
            if self.regis.mir[11] == 1:
                self.regis.regs[arraybin_to_dec(self.decoders.c)] = self.deslocador.a

        
