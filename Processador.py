from Componentes import *
from ISA_MIC1 import inst, micro_inst_text
from Assembly import gerar_e_compilar

class Processador:

    def __init__(self):
        self.regs = Registradores()
        self.ula = ULA()
        self.deslocador = Deslocador()
        self.mp = mp
        self.mc = mc
        self.decoders = Decoders()
        self.logica = CaixaLogica()
        self.programa = []