# ===================================================== IMPORTS ================================================= #
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_style as ts
from Functions import dec_to_arraybin, arraybin_to_dec
from Assembly import gerar_e_compilar
from Componentes import Clock
from Processador import Processador

register_names = ["PC", "AC", "SP", "IR", "TIR", "zer", "+um", "-um", "AM", "SM", "A", "B", "C", "D", "E", "F"]

# ==================================================== VARIABLES ================================================ #
class Variables:
    """
    Classe que reúne as variáveis:
    inst_index: posição da próxima instrução na lista
    last_instr_var: variável do tkinter que guarda a string da última instrução executada
    next_instr_var: variável do tkinter que guarda a string da próxima instrução
    regis_list: lista com os valores dos regostradores
    memor_list: lista com os valores dos endereços de memória
    regis_var: variável do tkinter que guarda os valores dos registradores
    memor_var: variável do tkinter que guarda os valores dos endereços de memória
    not_compiled: lista com as linhas de código em macroinstruções
    compiled: lista com as linhas de código em binário.
    valido: indica se há um programa válido carregado ou se ele acabou
    finalizado: indica se o programa acabou
    botoes_validades: para lógica de desabilitação e habilitação dos botões
    """

    def __init__(self):
        self.inst_index = 0
        self.intervalo = tk.StringVar()

        self.atua_instr_var = tk.StringVar()
        self.last_instr_var = tk.StringVar()
        self.next_instr_var = tk.StringVar()

        self.regis_list = []
        self.memor_list = []
        self.regis_var = tk.StringVar()
        self.memor_var = tk.StringVar()

        self.not_compiled = []
        self.compiled = []
        self.var_list = []

        self.valido = False
        self.finalizado = False
        self.botoes_validades = [
            True, # executar proxima
            True, # reiniciar ececussão
            True, # executar tudo
            False, # pausar
            True # iniciar/despausar
        ]


# =================================================== CODE_EDITOR =============================================== #
class CodeEditor:
    """
    A CLasse CodeEditor consiste em um Frame do Tkinter que contém um ttk.Notebook com 2 abas criadas adicionando
    dois Frames ao Notebook com o método add(). Então ao alternar de abas, o usuário alterna entre dois Frames,
    esses Frames possuem um Widget de Texto, mas na segunda aba ele é configurado para impedir edição do texto,
    servindo apenas para mostrar informação
    """

    def __init__(self, root):
        self.frame = tk.Frame(root, borderwidth=1)
        self.frame.place(x=10, y=10, width=250, height=460)
        self.tabs = ttk.Notebook(self.frame)

        self.tab1 = tk.Frame()
        self.tab2 = tk.Frame()
        self.tabs.add(self.tab1, text="assembly")
        self.tabs.add(self.tab2, text="binário")
        self.tabs.pack(fill="x")

        self.code_input = tk.Text(
            self.tab1,
            width=36,
            height=27,
            font=("Arial", 11)
        )
        self.code_input.pack(expand=True)

        self.code_binar = tk.Text(
            self.tab2,
            width=36,
            height=27,
            font=("Arial", 11),
            state="disabled"
        )
        self.code_binar.pack(expand=True)


# ===================================================== BUTTONS ================================================= #
class Buttons:
    """
    Essa Classe posui um Frame com alguns botões instanciados nele. Todos os botões funcionam da mesma forma: ao
    serem pressionados, ativam um método ou função. Essa classe também cria uma área para entrada de um valor com
    a classe Entry do Tkinter e alguns labels para organização e mostrar a próxima instrução e a última instrção
    executada.
    """

    def __init__(self, root, variables, interface):

        self.frame = tk.Frame(root, borderwidth=1)
        self.frame.place(x=270, y=10, width=220, height=460)

        # EXECUÇÃO --------------------------------------------------------------------------------------
        self.execussao = tk.LabelFrame(self.frame, text="Execussão")
        self.execussao.pack(fill="x")
        self.execussao.configure(pady=5)

        self.button_next = tk.Button(self.execussao, text="executar próxima", height=1, command=interface.ex_next)
        self.button_next.pack(fill="x", pady=1, padx=5)

        self.button_rein = tk.Button(self.execussao, text="reiniciar execussão", height=1, command=interface.ex_restart)
        self.button_rein.pack(fill="x", pady=1, padx=5)

        self.button_eall = tk.Button(self.execussao, text="executar tudo", height=1, command=interface.ex_all)
        self.button_eall.pack(fill="x", pady=1, padx=5)

        self.button_paus = tk.Button(self.execussao, text="pausar execussão", height=1, command=interface.ex_pause, state="disabled")
        self.button_paus.pack(fill="x", pady=1, padx=5)

        self.button_inte = tk.Button(self.execussao, text="iniciar/despausar", height=1, command=interface.ex_nexts)
        self.button_inte.pack(fill="x", pady=1, padx=5)

        self.exec_buttons = [
            self.button_next,
            self.button_rein,
            self.button_eall,
            self.button_paus,
            self.button_inte
        ]

        # INSTRUÇÕES ------------------------------------------------------------------------------------------
        self.instrucoes = tk.LabelFrame(self.frame, text="Instrução atual")
        self.instrucoes.pack(fill="x")
        self.instrucoes.configure(pady=5, padx=5)

        self.instr_table = ttk.Treeview(self.instrucoes, columns=("texto", "instr"), show="", height=2)
        self.instr_table.column("texto", width=50, stretch=tk.NO, anchor="center")
        self.instr_table.column("instr", width=150, stretch=tk.NO, anchor="center")
        self.instr_table.tag_configure(tagname="odd", background="white")
        self.instr_table.tag_configure(tagname="even", background="lightgray")
        self.instr_table.bind("<Button-1>", lambda event: "break")
        self.instr_table.pack()

        self.ciclo_table = ttk.Treeview(self.instrucoes, columns=("texto", "number"), show="", height=2)
        self.ciclo_table.column("texto", width=100, stretch=tk.NO, anchor="center")
        self.ciclo_table.column("number", width=100, stretch=tk.NO, anchor="center")
        self.ciclo_table.tag_configure(tagname="odd", background="white")
        self.ciclo_table.tag_configure(tagname="even", background="lightgray")
        self.ciclo_table.bind("<Button-1>", lambda event: "break")
        self.ciclo_table.pack()

        campos = ["macro", "micro"]
        for i in range(len(campos)):
            temp = "odd"
            if i == "":
                temp = "even"
            self.instr_table.insert("", index=tk.END, values=(campos[i], ""), tags=temp)

        campos = ["subciclo atual", "total de subciclos"]
        for i in range(len(campos)):
            temp = "odd"
            if i == "":
                temp = "even"
            self.ciclo_table.insert("", index=tk.END, values=(campos[i], "0"), tags=temp)

        self.subframe = tk.Frame(self.instrucoes)
        self.subframe.pack()

        self.time_label = tk.Label(self.subframe, font=("Arial", 11), text="Intervalo:")
        self.time_label.grid(row=0, column=0)

        self.time_text = tk.Entry(self.subframe, width=10, font=("Arial", 11), textvariable=variables.intervalo)
        self.time_text.grid(row=0, column=1)

        self.button_send = tk.Button(self.subframe, text="enviar", height=1, command=interface.update_intervalo)
        self.button_send.grid(row=0, column=2)

        # MEMÓRIA ----------------------------------------------------------------------------------------------
        self.memoria = tk.LabelFrame(self.frame, text="Memória")
        self.memoria.pack(fill="x")
        self.memoria.configure(pady=5)

        self.button_comp = tk.Button(self.memoria, text="compilar e carregar", height=1,
                                     command=interface.compile_and_load)
        self.button_comp.pack(fill="x", pady=1, padx=5)

        self.button_clea = tk.Button(self.memoria, text="limpar memória", height=1, command=interface.clear_memory)
        self.button_clea.pack(fill="x", pady=1, padx=5)

        # CÓDIGO -------------------------------------------------------------------------------------------------
        self.codigo = tk.LabelFrame(self.frame, text="Código")
        self.codigo.pack(fill="x")
        self.codigo.configure(pady=5)

        self.button_erase = tk.Button(self.codigo, text="limpar código", height=1, command=interface.clear_code)
        self.button_erase.pack(fill="x", pady=1, padx=5)


# ============================================= REGISTRADORES E MEMÓRIA ========================================= #
class RegsAndMem:
    """
    Essa Classe Duas Listas, uma com 17 posições para exibir o dado dos registradores e Uma de muitas
    posiçoes para exibir os dados dos endereços de memória. Alguns Labels também são criados para organização
    e todos esses Widgets estão em grid 2x3 num Frame.
    """

    def __init__(self, root, variables):
        self.frame = tk.Frame(root, borderwidth=1)
        self.frame.place(x=500, y=10, width=450, height=450)

        self.lbl_regis = tk.Label(self.frame, text="REGISTRADORES:", height=1, font=("arial", 11))
        self.lbl_regis.grid(row=1, column=1)

        self.lbl_regis = tk.Label(self.frame, text="MEMÓRIA:", height=1, font=("arial", 11))
        self.lbl_regis.grid(row=1, column=2)

        self.regis_table = ttk.Treeview(self.frame, columns=("address", "dado"), show="headings", height=20)
        self.regis_table.heading("address", text="regist")
        self.regis_table.heading("dado", text="dado")
        self.regis_table.column("address", width=50, stretch=tk.NO, anchor="center")
        self.regis_table.column("dado", width=150, stretch=tk.NO, anchor="center")
        self.regis_table.grid(row=2, column=1)
        self.regis_table.tag_configure(tagname="odd", background="white")
        self.regis_table.tag_configure(tagname="even", background="lightgray")

        self.subframe = tk.Frame(self.frame)
        self.subframe.grid(row=2, column=2)

        self.memor_table = ttk.Treeview(self.subframe, columns=("address", "dado"), show="headings", height=20)
        self.memor_table.heading("address", text="endereço")
        self.memor_table.heading("dado", text="dado")
        self.memor_table.column("address", width=80, stretch=tk.NO, anchor="center")
        self.memor_table.column("dado", width=140, stretch=tk.NO, anchor="center")
        self.memor_table.grid(row=0, column=0)
        self.memor_table.tag_configure(tagname="odd", background="white")
        self.memor_table.tag_configure(tagname="even", background="lightgray")

        self.scroll = ttk.Scrollbar(self.subframe, orient="vertical", command=self.memor_table.yview)
        self.memor_table.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky="ns")

        for i in range(16):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            self.regis_table.insert("", index=tk.END, values=(register_names[i], dec_to_arraybin(0, 16)), tags=temp)

        for i in range(4096):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            self.memor_table.insert("", index=tk.END, values=(i, 0), tags=temp)


    def edit_row(self, table, address, value, regis):
        """
        parametro regis:

        "registrador" -> usa o nome do registrador da lista de nomes com endereço address
        na coluna esquerda

        "memoria" -> usa o address como valor para a coluna da esuerda

        outros valores -> o valor passado é usado na coluna da esquerda
        """

        if regis == "registrador":
            table.item(table.get_children()[address], values=(register_names[address], value))
        elif regis == "memoria":
            table.item(table.get_children()[address], values=(address, value))
        else:
            table.item(table.get_children()[address], values=(regis, value))

# ================================================= MAIN INTERFACE ============================================== #


class Interface:
    """
    As 3 áreas principais da interface estão separadas em classes para facilitar a organização. Dessa forma
    a classe Interface serve apenas para criar e configurar a raíz e para Unir as outras classes.
    """

    def __init__(self, clock, process):
        self.clock = clock
        self.process = process
        self.process.interface = self
        self.clock.interface = self

        self.root = tk.Tk()  # criação da raíz onde todos os vão ser instanciados
        self.root.geometry("960x480")  # definição do tamanho da tela
        self.root.title("Simulador de Microarquitetura")  # título
        self.root.resizable(False, False)  # não redimensionável em x e em y

        self.img = tk.PhotoImage(file="icone.png")
        self.root.wm_iconphoto(False, self.img)

        self.style = ts.ThemedStyle(self.root)
        self.style.set_theme("clearlooks")
        self.style.configure("Horizontal.TScrollbar", bg="blue")

        self.variables = Variables()
        self.code_edit = CodeEditor(self.root)
        self.regs_and_mem = RegsAndMem(self.root, self.variables)
        self.buttons = Buttons(self.root, self.variables, self)

        self.root.after(0, self.relogio())
        self.root.after(0, self.update_interface_infos())
        tk.mainloop()

    def ex_next(self):
        """
        Se o clock está pausado, avança um subciclo
        """
        if self.clock.paused:
            self.clock.avanca_subciclo()

    def ex_restart(self):
        """
        O método ex_restart visa recomeçar a execussão do código. Para isso a memória é
        limpa com o método clear_memory() e o código é recarregado na memória com load().
        Também pausa o clock, habilita o despause e desabilita o pause
        """
        self.clock.subciclo_atual = 0
        self.clock.pausa_clock()
        self.clear_memory()
        self.load(False)

        self.variables.botoes_validades[4] = True
        self.variables.botoes_validades[3] = False
        self.variables.botoes_validades[0] = True

    def ex_all(self):
        """
        Pausa o clock e entre em um loop chamando cada próximo subciclo
        para evitar StackOverflow por recussão
        """
        self.clock.pausa_clock()
        # por enquanto esse loop não pode ser quebrado, já que não
        # há verificação de final de código
        while True:
            self.clock.avanca_subciclo()

    def ex_pause(self):
        """
        Pausa o clock, desabilita o pause e habilita o despause
        """
        self.clock.pausa_clock()

        self.variables.botoes_validades[4] = True
        self.variables.botoes_validades[3] = False
        self.variables.botoes_validades[0] = True

    def ex_nexts(self):
        """
        Despausa o clock, desabilita o despause e habilita o pause
        """
        self.clock.despausa_clock()
        self.variables.botoes_validades[4] = False
        self.variables.botoes_validades[3] = True
        self.variables.botoes_validades[0] = False

    def compile_and_load(self):
        """
        Esse método chama o método compile(), que se retornat True - significando que a lista de
        macroinstruções não é vazia - chama load()
        """
        if self.compile() and len(self.variables.compiled):
            self.load(True)
            self.variables.valido = True
            self.variables.finalizado = False

    def compile(self):
        """
        Esse método cria uma lista de strings obtidas de code_area.code_input, dividindo essa string
        com split(). Depois é feito um processo para transformar todas as linhas que contém somente espaços
        em strings vazias e depois todas as strings vazias são retiradas. Se a lista ficar vazia, retorna
        False, se não, chama gerar_e_compilar() e atribui valores de código em Assembly, binário e variáveis
        de memória aos campos de variables criados para guardar essas informações.
        :return: True ou False
        """
        aux_list = self.code_edit.code_input.get("1.0", "end").split("\n")
        for i in range(len(aux_list)):
            while len(aux_list[i]) > 0:
                if aux_list[i][0] == " ":
                    aux_list[i] = aux_list[i][1:]
                else:
                    break
        for _ in range(aux_list.count("")):
            aux_list.remove("")
        if aux_list:
            self.variables.compiled, self.variables.var_list, _ = gerar_e_compilar(aux_list, self.process.mp)
            self.variables.not_compiled = aux_list
            return True
        return False

    def load(self, to_bin):
        """
        Passa o Programa Compilado para tabela da memória com endereço calculado usando a funcão
        b10_to_b2(). Também cria uma string passada para o widget text que exibe o código
        compilado em code_area.code_binar. A variável to_bin diz se a função deve colocar o código
        em binário na área de código em binário ou não.
        """
        if len(self.variables.compiled):
            self.variables.valido = True
        for i in range(len(self.variables.compiled)):
            self.regs_and_mem.edit_row(self.regs_and_mem.memor_table, i, self.variables.compiled[i], "memoria")
        if to_bin:
            aux_str = ""
            for inst in self.variables.compiled:
                linha = ""
                for bit in inst:
                    linha += str(bit)
                aux_str += linha + "\n"
            self.code_edit.code_binar.configure(state="normal")
            self.code_edit.code_binar.delete("1.0", "end")
            self.code_edit.code_binar.insert("1.0", aux_str)
            self.code_edit.code_binar.configure(state="disabled")

    def clear_memory(self):
        """
        Limpa a memória percorrendo todos os itens e removendo-os
        Também reseta os registradores
        """
        # resetar o componente da memória
        self.process.mp = []
        for i in range(2 ** 12):
            self.process.mp.append([0 for _ in range(16)])

        # resetar na interface
        self.variables.memor_list = []
        for item in self.regs_and_mem.memor_table.get_children():
            self.regs_and_mem.memor_table.delete(item)
        for i in range(4096):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            self.regs_and_mem.memor_table.insert("", index=tk.END, values=(i, 0), tags=temp)

        # resetar as contagens de subciclo
        self.clock.subciclo_atual = 0
        self.clock.subciclo_total = 0

        # atualizar subciclos na interface
        self.regs_and_mem.edit_row(self.buttons.ciclo_table, 0, self.clock.subciclo_atual, "subciclo atual")
        self.regs_and_mem.edit_row(self.buttons.ciclo_table, 1, self.clock.subciclo_total, "total de subciclos")

        # programa carregado é inválido
        self.variables.valido = False

        # rresetar os registradores
        self.process.regis.__init__()



    def clear_code(self):
        """
        Limpa os Widgets de texto da área de código
        """
        self.code_edit.code_input.delete("1.0", "end")
        self.code_edit.code_binar.configure(state="normal")
        self.code_edit.code_binar.delete("1.0", "end")
        self.code_edit.code_binar.configure(state="disabled")


    def update_intervalo(self):
        """
        Atualiza o ontervalo do clock
        """
        self.clock.atualiza_intervalo(self.variables)


    def update_interface_infos(self):
        """
        Atualiza a tabela de registradores na interface e faz a logica
        de desativação dos botões
        """
        for i in range(16):
            self.regs_and_mem.edit_row(self.regs_and_mem.regis_table, i, self.process.regis.regs[i], "registrador")

        for i in range(5): # são 5 botões
            if i != 1:
                if self.variables.botoes_validades[i] and self.variables.valido:
                    self.buttons.exec_buttons[i].configure(state="normal")
                else:
                    self.buttons.exec_buttons[i].configure(state="disabled")
            elif self.variables.botoes_validades[i] and (self.variables.valido or self.variables.finalizado):
                self.buttons.exec_buttons[i].configure(state="normal")
            else:
                self.buttons.exec_buttons[i].configure(state="disabled")

        self.root.after(500, self.update_interface_infos)

    def relogio(self):

        # configuração do botão de atualizar intervalo do relógio
        if not self.variables.intervalo.get().isdigit():
            self.buttons.button_send.configure(state="disabled")
        elif self.buttons.button_send.cget("state"):
            self.buttons.button_send.configure(state="normal")

        # se não está pausado, avança o subciclo
        if not self.clock.paused:
            self.clock.avanca_subciclo()

        self.root.after(self.clock.intervalo, self.relogio)


process = Processador()
clock = Clock(process)
interface = Interface(clock, process)
