'''
Comentários por Cláudio Pires Salgado

Arquivo: ISA_MIC1.py

    Arquivo de código em Python voltado para o armazenamento das
    Macroinstruções e das Microinstruções da ISA MIC-1 em uma estrutura de dados do Python,
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
    'LODD': '0000',  # ac:= m[x]
    'STOD': '0001',  # m[x]:= ac
    'ADDD': '0010',  # ac:= ac + m[x]
    'SUBD': '0011',  # ac:= ac - m[x]
    'JPOS': '0100',  # If ac >= 0, then pc:= x
    'JZER': '0101',  # If ac = 0, then pc:= x
    'JUMP': '0110',  # pc:= x
    'LOCO': '0111',  # ac:= x {0<= x <=4095}
    'LODL': '1000',  # ac:= m[sp + x]
    'STOL': '1001',  # m[sp + x]:= ac
    'ADDL': '1010',  # ac:= ac + m[sp + x]
    'SUBL': '1011',  # ac:= ac - m[sp + x]
    'JNEG': '1100',  # If ac < 0, then pc:= x
    'JNZE': '1101',  # If ac != 0, then pc:= x
    'CALL': '1110',  # sp:= sp-1 ; m[sp]:= pc ; pc:= x
    'PSHI': '1111000000000000',  # sp:= sp-1 ; m[sp]:= m[ac]
    'POPI': '1111001000000000',  # m[ac]:= m[sp] ; sp:= sp+1
    'PUSH': '1111010000000000',  # sp:= sp-1 ; m[sp]:= ac
    'POP' : '1111011000000000',  # ac:= m[sp] ; sp:= sp+1
    'RETN': '1111100000000000',  # pc:= m[sp] ; sp:= sp+1
    'SWAP': '1111101000000000',  # tmp:= ac ; ac:= sp ; sp:= tmp
    'INSP': '11111100',  # sp:= sp + y {0<= y <=255}
    'DESP': '11111110'  # sp:= sp - y {0<= y <=255}
}

micro_inst = {
    # (0000) ac:= m[x]
    'LODD': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 11;",  # C
             "alu := tir; if n then goto 9;",  # D
             "mar := ir; rd;",
             "rd;",
             "ac := mbr; goto 0;"  # LODD
             ),

    # (0001) m[x]:= ac
    'STOD': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 11;",  # C
             "alu := tir; if n then goto 9;",  # D
             "mar := ir; mbr := ac; wr;",
             "wr; goto 0;"  # STOD
             ),

    # (0010) ac:= ac + m[x]
    'ADDD': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 11;",  # C
             "alu := tir; if n then goto 15;",
             "mar := ir; rd;",
             "ac:= mbr + ac; goto 0;"  # ADDD
             ),

    # (0011) ac:= ac - m[x]
    'SUBD': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 11;",  # if C = 1
             "alu := tir; if n then goto 15;",  # if D = 1
             "mar := ir; rd;",
             "ac := ac + 1; rd;",
             "a := inv(mbr);",
             "ac := ac + a; goto 0;"  # SUBD
             ),

    # (0100) IF ac >= 0, then pc:= x
    'JPOS': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 25;",  # if C = 1
             "alu := tir; if n then goto 23;",  # if D = 1
             "alu := ac; if n then goto 0;",  # Teste do IF
             "pc := band(ir,amask); goto 0;"  # JPOS - Ação se IF for True
             ),

     # (0101) IF ac = 0, then pc:= x
    'JZER': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 25;",  # if C = 1
             "alu := tir; if n then goto 23;",  # if D = 1
             "alu := ac; if z then goto 22;",  # Teste do IF
             "pc := band(ir,amask); goto 0;",  # JZER - Ação se IF for True
             "goto 0;"  # Ação se IF for False
             ),

    # (0110) pc:= x
    'JUMP': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 25;",  # if C = 1
             "alu := tir; if n then goto 27;",  # if D = 1
             "pc := band(ir,amask); goto 0;"  # JUMP
            ),

    # (0111) ac:= x {0<= x <=4095}
    'LOCO': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 19;",  # if B = 1
             "tir := lshift(tir); if n then goto 25;",  # if C = 1
             "alu := tir; if n then goto 27;",  # if D = 1
             "ac := band(ir,amask); goto 0;"  # LOCO
             ),

    # (1000) ac:= m[sp + x]
    'LODL': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 35;",  # if C = 1
             "alu := tir; if n then goto 33;",  # if D = 1
             "a := ir + sp;",
             "mar := a; rd; goto 7;",
             "rd;",
             "ac := mbr; goto 0;"  # LODL
             ),

    # (1001) m[sp + x]:= ac
    'STOL': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 35;",  # if C = 1
             "alu := tir; if n then goto 33;",  # if D = 1
             "a := ir + sp;",
             "mar := a; mbr := ac; wr; goto 10;"  # STOL
             "wr; goto 0;"
             ),

    # (1010) ac:= ac + m[sp + x]
    'ADDL': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 35;",  # if C = 1
             "alu := tir; if n then goto 38;",  # if D = 1
             "a := ir + sp;",
             "mar := a; rd; goto 13;",
             "rd;",
             "ac := mbr + ac; goto 0;"  # ADDL
             ),

    # (1011) ac:= ac - m[sp + x]
    'SUBL': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 35;",  # if C = 1
             "alu := tir; if n then goto 38;",  # if D = 1
             "a := ir + sp;",
             "mar := a; rd; goto 16;",
             "ac := ac + 1; rd;",
             "a := inv(mbr);",
             "ac := ac + a; goto 0;"  # SUBL
             ),

    # (1100) IF ac < 0, then pc:= x
    'JNEG': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "alu := tir; if n then goto 44;",  # if D = 1
             "alu := ac; if n then goto 22;",  # Teste do IF
             "pc := band(ir,amask); goto 0;",  # JNEG - Ação se IF for True
             "goto 0;"  # Ação se IF for False
             ),

    # (1101) IF ac != 0, then pc:= x
    'JNZE': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "alu := tir; if n then goto 44;",  # if D = 1
             "alu := ac; if z then goto 0;",  # Teste do IF (e Ação se IF for False)
             "pc := band(ir,amask); goto 0;"  # JNZE - Ação se IF for True
             ),

    # (1110) sp:= sp-1 ; m[sp]:= pc ; pc:= x
    'CALL': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "sp := sp + (-1);",
             "mar := sp; mbr := pc; wr;",
             "pc := band(ir,amask); wr; goto 0"
             ),

    # (1111000'000000000) sp:= sp-1 ; m[sp]:= m[ac]
    'PSHI': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 59;",  # if F = 1
             "alu := tir; if n then goto 56;",  # if G = 1
             "mar := ac; rd;",
             "sp := sp + (-1); rd;",
             "mar := sp; wr; goto 10;",  # PSHI
             "wr; goto 0;"
             ),

    # (1111001'000000000) m[ac]:= m[sp] ; sp:= sp+1
    'POPI': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 59;",  # if F = 1
             "alu := tir; if n then goto 56;",  # if G = 1
             "mar := sp; sp := sp + 1; rd;",
             "rd;",
             "mar := ac; wr; goto 10;",  # POPI
             "wr; goto 0;"
             ),

    # (1111010'000000000) sp:= sp-1 ; m[sp]:= ac
    'PUSH': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 59;",  # if F = 1
             "alu := tir; if n then goto 62;",  # if G = 1
             "sp := sp + (-1);",
             "mar := sp; mbr := ac; wr; goto 10;",  # PUSH
             "wr; goto 0;"
             ),

    # ac:= (1111011'000000000) m[sp] ; sp:= sp+1
    'POP' : ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 59;",  # if F = 1
             "alu := tir; if n then goto 62;",  # if G = 1
             "mar := sp; sp := sp + 1; rd;",
             "rd;",
             "ac := mbr; goto 0;"  # POP
             ),
    # (1111100'000000000) pc:= m[sp] ; sp:= sp+1
    'RETN': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 73;",  # if F = 1
             "alu := tir; if n then goto 70;",  # if G = 1
             "mar := sp; sp := sp + 1; rd;",
             "rd;",
             "pc := mbr; goto 0"  # RETN
             ),

    # (1111101'000000000) tmp:= ac ; ac:= sp ; sp:= tmp
    'SWAP': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 73;",  # if F = 1
             "alu := tir; if n then goto 70;",  # if G = 1
             "a := ac;",
             "ac := sp;",          # SWAP
             "sp := a; goto 0;",
             ),

    # (1111110'0) sp:= sp + y {0<= y <=255}
    'INSP': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 73;",  # if F = 1
             "alu := tir; if n then goto 76;",  # if G = 1
             "a := band(ir, smask);",
             "sp := sp + a; goto 0;"  # INSP
            ),

    # (1111111'0) sp:= sp - y {0<= y <=255}
    'DESP': ("mar := pc; rd;",
             "pc := pc + 1; rd;",
             "ir := mbr; if n then goto 28;",  # if A = 1
             "tir := lshift(ir + ir); if n then goto 40;",  # if B = 1
             "tir := lshift(tir); if n then goto 46;",  # if C = 1
             "tir := lshift(tir); if n then goto 50;",  # if D = 1
             "tir := lshift(tir); if n then goto 65;",  # if E = 1
             "tir := lshift(tir); if n then goto 73;",  # if F = 1
             "alu := tir; if n then goto 76;",  # if G = 1
             "a := band(ir, smask);",
             "a := inv(a);",
             "a := a + 1; goto 75;",
             "sp := sp + a; goto 0;"  # DESP
             )
}

micro_bin = (
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
