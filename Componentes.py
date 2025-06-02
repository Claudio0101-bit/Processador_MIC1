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
        self.ac = 0
        self.pc = 0
        self.sp = 0

        self.mar = 0
        self.mbr = 0

# Classe referente à Unidade Lógica-Aritmética (ULA)
class ULA:
    # Operandos A e B
    def __init__(self):
        self.a = 0
        self.b = 0