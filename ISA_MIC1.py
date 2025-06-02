'''
Comentários por Cláudio Pires Salgado

Arquivo: ISA_MIC1.py

    Arquivo de código em Python voltado para o armazenamento das
    Macroinstruções da ISA MIC-1 em uma estrutura de dados do Python,
    assim como outras variáveis futuramente necessárias.

    *** Observações sobre as Macroinstruções da ISA MIC-1:

    --- Em binário, cada instrução corresponde a 16 bits, caso a instrução
    não corresponda a 16 bits, os bits restantes correspondem ao valor usado
    na instrução em si.

    --- Nos comentários abaixo, o valor de X possui 12 bits e o valor de Y
    possui 8 bits.

    --- Estrutura usada para guardar as Macroinstruções: Dicionário.

    --- O sentido de cada instrução está comentado ao seu lado.
'''

inst = {
    'LODD': '0000', # ac:= m[x]
    'STOD': '0001', # m[x]:= ac
    'ADDD': '0010', # ac:= ac + m[x]
    'SUBD': '0011', # ac:= ac - m[x]
    'JPOS': '0100', # If ac >= 0, then pc:= x
    'JZER': '0101', # If ac = 0, then pc:= x
    'JUMP': '0110', # pc:= x
    'LOCO': '0111', # ac:= x {0<= x <=4095}
    'LODL': '1000', # ac:= m[sp + x]
    'STOL': '1001', # m[sp + x]:= ac
    'ADDL': '1010', # ac:= ac + m[sp + x]
    'SUBL': '1011', # ac:= ac - m[sp + x]
    'JNEG': '1100', # If ac < 0, then pc:= x
    'JNZE': '1101', # If ac != 0, then pc:= x
    'CALL': '1110', # sp:= sp-1 ; m[sp]:= pc ; pc:= x
    'PSHI': '1111000000000000', # sp:= sp-1 ; m[sp]:= m[ac]
    'POPI': '1111001000000000', # m[ac]:= m[sp] ; sp:= sp+1
    'PUSH': '1111010000000000', # sp:= sp-1 ; m[sp]:= ac
    'POP' : '1111011000000000', # ac:= m[sp] ; sp:= sp+1
    'RETN': '1111100000000000', # pc:= m[sp] ; sp:= sp+1
    'SWAP': '1111101000000000', # tmp:= ac ; ac:= sp ; sp:= tmp
    'INSP': '11111100', # sp:= sp + y {0<= y <=255}
    'DESP': '11111110' # sp:= sp - y {0<= y <=255}
}









