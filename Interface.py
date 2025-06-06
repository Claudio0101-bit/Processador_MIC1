'''
Comentários por Cláudio Pires Salgado

Arquivo: Interface.py

    Arquivo de código em Python voltado para a programação da Interface Gráfica do
    Simulador do Processador com ISA MIC-1, utilizando a Biblioteca TKinter para criar
    tal interface, por programação orientada a objetos.

'''

# ================================== IMPORTAÇÕES ================================== #
import tkinter as tk
from tkinter import ttk


class TKGUI:

    def __init__(self):
        """docstring"""

        # ======================================= JANELA ================================== #
        '''
        para criar a janela e a área principal da interface usa-se a classe tk.TK
        
        as linhas de comentário com seta servem para mudar o ícone da janela, não sei se é tão importante
        então por enquanto deixei comentado
        '''
        self.root = tk.Tk() # criação da raíz onde todos os vão ser instanciados
        self.root.geometry("960x480") # definição do tamanho da tela
        self.root.title("Simulador de Microarquitetura") # título
        self.root.resizable(False, False) # não redimensionável em x e em y

        # self.img = tk.PhotoImage(file="icone.png")       <-
        # self.root.wm_iconphoto(False, self.img)          <-


        # ========================================= VARIÁVEIS ======================================= #
        '''
        aqui são criados objetos da classe tk.StringVar, esses objetos podem ser associados á widgets
        da classe tk.Label
        "code_line" guarda a linha da próxima instrução   
        '''
        self.code_line = 1
        self.bin_var = tk.StringVar()

        self.last_instr_var = tk.StringVar()
        self.next_instr_var = tk.StringVar()

        self.regis_var = tk.StringVar()
        self.memor_var = tk.StringVar()


        # ======================================= ÁREA DO CÓDIGO ===================================== #
        '''
        1 - aqui é criado o objeto "frame1" da classe Frame que ocupa (fora as bordas) 1/3 da janela
        nesse Frame é instanciado o objeto "nttabs" da classe tkk.Notebook
        
        2 - são criados dois Frames sem pai, "tab1" e "tab2", que são adicionados ao Notebook para criar um espaço
        com abas para alternar emtre frames vazios
        
        3 - em "frame1" é criado uma área de inserção de texto com o objeto "code_input" da classe tk.Text
        
        4 - em "frame2" é criado uma área de exibição de texto com o objeto "code_binar" da classe tk.Label
        esse Label está associado À variável "bin_var"
        '''
        # 1
        self.frame1 = tk.Frame(self.root, borderwidth=1)
        self.frame1.place(x=10, y=10, width=320-20, height=480-20)
        self.nttabs = ttk.Notebook(self.frame1)
        # 2
        self.tab1 = tk.Frame()
        self.tab2 = tk.Frame(background="white", relief="sunken")
        self.nttabs.add(self.tab1, text="assembly")
        self.nttabs.add(self.tab2, text="binário")
        self.nttabs.pack(fill="x")
        # 3
        self.code_input = tk.Text(
            self.tab1,
            width=36,
            height=27,
            font=("Arial", 11)
        )
        self.code_input.pack(expand=True)
        # 4
        self.code_binar = tk.Label(
            self.tab2,background="white",
            text="change text here",
            textvariable=self.bin_var,
            font=("Arial", 11),
            justify="left"
        )
        self.code_binar.place(x=0, y=0)


        # ============================================ BOTÕES ================================ #
        '''
        1 - "frame2" é um objeto tk.Frame como "frame1", talbém é instanciado na raíz
        
        2 - "exec_section" é um objeto tk.Label usado para organizar a interface, abaixo dele são instanciados
        em "frame2" vários botões(classe tk.Button)
        
        3 - "subframe" é outro frame instanciado em "frame2", ele serve para organizar outros widgets dentro dele
        
        4 - "time_label", "last_label" e "next_label", são Labels instanciados em "subframe" posicionados na coluna 0
        de uma organização em grid, para isso foi escolhida a utilização do médoto .grid
        o objeto "time_text" da classe tk.Entry e os Labels "last_instr" e "next_instr" são também instanciados em
        "subframe", mas são posicionados na culona 1
        
        5 - "spacig" é um frame vazio para fazer espaçamento, "data_section" é só mais um label para organização e
        "button_clea" é somente mais um botão
        DETALHE: se for possível definir uma borda somente acima desse Widget, "spacing" não seria necessário
        
        6 - "spacing2", "data_section", "button_erase" e "button_tradu" são respectivamente, Frame, Label, Button e
        Button
        '''
        # 1
        self.frame2 = tk.Frame(self.root, borderwidth=1)
        self.frame2.place(x=330, y=10, width=320 - 20, height=480 - 20)
        # 2
        self.exec_section = tk.Label(self.frame2, text="------------- EXECUÇÃO -------------", height=1, font=("arial", 11))
        self.exec_section.pack(pady=1)

        self.button_next = tk.Button(self.frame2, text="executar próxima", height=1, command=self.ex_next)
        self.button_next.pack(fill="x", pady=1)
        self.button_rein = tk.Button(self.frame2, text="reiniciar execussão", height=1, command=self.restart)
        self.button_rein.pack(fill="x", pady=1)
        self.button_eall = tk.Button(self.frame2, text="executar tudo", height=1, command=self.ex_all)
        self.button_eall.pack(fill="x", pady=1)
        self.button_paus = tk.Button(self.frame2, text="pausar execussão", height=1, command=self.pause)
        self.button_paus.pack(fill="x", pady=1)
        self.button_inte = tk.Button(self.frame2, text="executar em intervalos", height=1, command=self.auto_ex)
        self.button_inte.pack(fill="x", pady=1)
        # 3
        self.subframe = tk.Frame(self.frame2)
        self.subframe.pack()
        # 4
        self.time_label = tk.Label(self.subframe, font=("Arial", 11), text="Intervalo em segundos:")
        self.time_label.grid(row=0, column=0)
        self.time_text = tk.Entry(self.subframe, width=10, font=("Arial", 11))
        self.time_text.grid(row=0, column=1)

        self.last_label = tk.Label(self.subframe, font=("Arial", 11), text="ùltima instrução executada:")
        self.last_label.grid(row=1, column=0)
        self.last_instr = tk.Label(self.subframe, width=10, textvariable=self.last_instr_var, font=("Arial", 11), text="LODD &x;")
        self.last_instr.grid(row=1, column=1)

        self.next_label = tk.Label(self.subframe, font=("Arial", 11), text="Próxima instrução a executar:")
        self.next_label.grid(row=2, column=0)
        self.next_instr = tk.Label(self.subframe, width=10, textvariable=self.next_instr_var, font=("Arial", 11), text="STOD x;")
        self.next_instr.grid(row=2, column=1)
        # 5
        self.spacing = tk.Frame(self.frame2, height=5, relief="solid")
        self.spacing.pack(pady=10)

        self.data_section = tk.Label(self.frame2, text="------------- MEMÓRIA -------------", height=1, font=("arial", 11))
        self.data_section.pack(pady=1)

        self.button_clea = tk.Button(self.frame2, text="limpar memória", height=1, command=self.clear_memory)
        self.button_clea.pack(fill="x", pady=1)
        # 6
        self.spacing2 = tk.Frame(self.frame2, height=5, relief="solid")
        self.spacing2.pack(pady=10)

        self.data_section = tk.Label(self.frame2, text="------------- CÓDIGO -------------", height=1, font=("arial", 11))
        self.data_section.pack(pady=1)

        self.button_erase = tk.Button(self.frame2, text="limpar código", height=1, command=self.clear_code)
        self.button_erase.pack(fill="x", pady=1)
        self.button_tradu = tk.Button(self.frame2, text="traduzir para binário", height=1, command=self.translate)
        self.button_tradu.pack(fill="x", pady=1)


        # ========================================== ARMAZENAMENTO ============================================== #
        '''
        essa parte é organizada de forma semelhante ao "frame1", por enquanto só existe para ocupar o espaço
        '''
        self.frame3 = tk.Frame(self.root, borderwidth=1)
        self.frame3.place(x=650, y=10, width=320 - 20, height=480 - 20)
        self.rmtabs = ttk.Notebook(self.frame3)

        self.tabr = tk.Frame()
        self.tabm = tk.Frame(background="white", relief="sunken")
        self.rmtabs.add(self.tabr, text="registradores")
        self.rmtabs.add(self.tabm, text="memória")
        self.rmtabs.pack(fill="x")

        self.regist_info = tk.Text(self.tabr, font=("Arial", 11))
        self.regist_info.pack(expand=True)

        self.memory_info = tk.Label(self.tabm, background="white", font=("Arial", 11))
        self.memory_info.place(x=0, y=0)


        # ============================================= LOOP ================================================== #
        '''
        é preciso chamar o mainloop para iniciar a interface
        '''
        self.root.mainloop()


    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MÉTODOS DOS BOTÕES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< #
    '''
    funções e métodos podem ser passados como parâmetros ao criar os botões da classe tk.Button, esses botões, ao serem
    pressionados irão chamar essas funções/métodos
    NOTE: na criação dos botões, os métodos devem ser PASSADOS e não CHAMADOS dentro dos parâmetros
    '''
    def ex_next(self):
        self.code_line += 1
        self.last_instr_var.set(self.next_instr_var.get())
        self.next_instr_var.set(self.code_input.get(f"{self.code_line}.0", f"{self.code_line+1}.0").strip("\n"))
        self.next_aux()

    def next_aux(self):
        if self.next_instr_var.get() == "":
            self.code_line += 1
            self.next_instr_var.set(self.code_input.get(f"{self.code_line}.0", f"{self.code_line+1}.0").strip("\n"))
            self.next_aux()

    def restart(self):
        self.last_instr_var.set("")
        self.code_line = 1
        self.next_instr_var.set(self.code_input.get(f"{self.code_line}.0", f"{self.code_line+1}.0").strip("\n"))

    def ex_all(self):
        pass

    def pause(self):
        pass

    def auto_ex(self):
        pass

    def clear_memory(self):
        pass

    def clear_code(self):
        self.bin_var.set("")
        self.code_input.delete("1.0", "end")

    def translate(self):
        self.bin_var.set(self.code_input.get("1.0", "end"))


tkgui = TKGUI()
