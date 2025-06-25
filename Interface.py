# ===================================================== IMPORTS ================================================= #
import tkinter as tk
from tkinter import ttk
from ttkthemes import themed_style as ts
from Assembly import b10_to_b2
from Assembly import gerar_e_compilar


# ===================================================== FUNÇÕES ================================================= #
def edit_row(table, address, value):
    table.item(table.get_children()[address], values=(address, value))


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
    """

    def __init__(self):
        self.inst_index = 0

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
        self.execussao.configure(pady=1)

        self.button_next = tk.Button(self.execussao, text="executar próxima", height=1, command=interface.ex_next)
        self.button_next.pack(fill="x", pady=1, padx=5)

        self.button_rein = tk.Button(self.execussao, text="reiniciar execussão", height=1, command=interface.ex_restart)
        self.button_rein.pack(fill="x", pady=1, padx=5)

        self.button_eall = tk.Button(self.execussao, text="executar tudo", height=1, command=interface.ex_all)
        self.button_eall.pack(fill="x", pady=1, padx=5)

        self.button_paus = tk.Button(self.execussao, text="pausar execussão", height=1, command=interface.ex_pause)
        self.button_paus.pack(fill="x", pady=1, padx=5)

        self.button_inte = tk.Button(self.execussao, text="executar em intervalos", height=1, command=interface.ex_nexts)
        self.button_inte.pack(fill="x", pady=1, padx=5)

        # INSTRUÇÕES ------------------------------------------------------------------------------------------
        self.instrucoes = tk.LabelFrame(self.frame, text="Instruções")
        self.instrucoes.pack(fill="x")
        self.instrucoes.configure(pady=5, padx=5)

        self.instr_table = ttk.Treeview(self.instrucoes, columns=("texto", "instr"), show="", height=3)
        self.instr_table.column("texto", width=140, stretch=tk.NO, anchor="center")
        self.instr_table.column("instr", width=140, stretch=tk.NO, anchor="center")
        self.instr_table.tag_configure(tagname="odd", background="white")
        self.instr_table.tag_configure(tagname="even", background="lightgray")
        self.instr_table.bind("<Button-1>", lambda event: "break")
        self.instr_table.pack()

        self.ciclo_table = ttk.Treeview(self.instrucoes, columns=("texto", "number"), show="", height=2)
        self.ciclo_table.column("texto", width=140, stretch=tk.NO, anchor="center")
        self.ciclo_table.column("number", width=140, stretch=tk.NO, anchor="center")
        self.ciclo_table.tag_configure(tagname="odd", background="white")
        self.ciclo_table.tag_configure(tagname="even", background="lightgray")
        self.ciclo_table.bind("<Button-1>", lambda event: "break")
        self.ciclo_table.pack()

        campos = ["macroinst atual", "ultima microinst", "proxima microinst"]
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
            self.ciclo_table.insert("", index=tk.END, values=(campos[i], ""), tags=temp)

        self.subframe = tk.Frame(self.instrucoes)
        self.subframe.pack()

        self.time_label = tk.Label(self.subframe, font=("Arial", 11), text="Intervalo:")
        self.time_label.grid(row=0, column=0)
        self.time_text = tk.Entry(self.subframe, width=10, font=("Arial", 11))
        self.time_text.grid(row=0, column=1)

        # MEMÓRIA ----------------------------------------------------------------------------------------------
        self.memoria = tk.LabelFrame(self.frame, text="Memória")
        self.memoria.pack(fill="x")
        self.memoria.configure(pady=1)

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
        self.regis_table.heading("address", text="registrador")
        self.regis_table.heading("dado", text="dado")
        self.regis_table.column("address", width=100, stretch=tk.NO, anchor="center")
        self.regis_table.column("dado", width=100, stretch=tk.NO, anchor="center")
        self.regis_table.grid(row=2, column=1)
        self.regis_table.tag_configure(tagname="odd", background="white")
        self.regis_table.tag_configure(tagname="even", background="lightgray")

        self.subframe = tk.Frame(self.frame)
        self.subframe.grid(row=2, column=2)

        self.memor_table = ttk.Treeview(self.subframe, columns=("address", "dado"), show="headings", height=20)
        self.memor_table.heading("address", text="endereço")
        self.memor_table.heading("dado", text="dado")
        self.memor_table.column("address", width=110, stretch=tk.NO, anchor="center")
        self.memor_table.column("dado", width=110, stretch=tk.NO, anchor="center")
        self.memor_table.grid(row=0, column=0)
        self.memor_table.tag_configure(tagname="odd", background="white")
        self.memor_table.tag_configure(tagname="even", background="lightgray")

        self.scroll = ttk.Scrollbar(self.subframe, orient="vertical", command=self.memor_table.yview)
        self.memor_table.configure(yscrollcommand=self.scroll.set)
        self.scroll.grid(row=0, column=1, sticky="ns")

        names = ["ac", "pc", "mpc", "sp", "ir", "mir", "mar", "mbr", "a", "b", "c", "d", "e", "f", "ma1", "me1", "ze"]
        for i in range(len(names)):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            if names[i] == "ma1":
                self.regis_table.insert("", index=tk.END, values=(names[i], b10_to_b2(1, 8)), tags=temp)
            elif names[i] == "me1":
                self.regis_table.insert("", index=tk.END, values=(names[i], b10_to_b2(-1, 8)), tags=temp)
            else:
                self.regis_table.insert("", index=tk.END, values=(names[i], b10_to_b2(0, 8)), tags=temp)

        for i in range(4000):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            self.memor_table.insert("", index=tk.END, values=(i, ""), tags=temp)


# ================================================= MAIN INTERFACE ============================================== #


class Interface:
    """
    As 3 áreas principais da interface estão separadas em classes para facilitar a organização. Dessa forma
    a classe Interface serve apenas para criar e configurar a raíz e para Unir as outras classes.
    """

    def __init__(self):
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

        tk.mainloop()

    def ex_next(self):
        # chamar função de executar próxima instrução
        # fazer controle de fim de código
        pass

    def ex_restart(self):
        """
        O método ex_restart visa recomeçar a execussão do código. Para isso a memória é
        limpa com o método clear_memory() e o código é recarregado na memória com load().
        """
        self.clear_memory()
        self.load(False)

    def ex_all(self):
        # executar auto em intervalo 0
        pass

    def ex_pause(self):
        # pausar autoexecussão
        pass

    def ex_nexts(self):
        # iniciar autoexecussão
        pass

    def compile_and_load(self):
        """
        Esse método chama o método compile(), que se retornat True - significando que a lista de
        macroinstruções não é vazia - chama load()
        """
        if self.compile():
            self.load(True)

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
            self.variables.compiled, self.variables.var_list = gerar_e_compilar(aux_list)
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
        for i in range(len(self.variables.compiled)):
            edit_row(self.regs_and_mem.memor_table, i, self.variables.compiled[i])
        if to_bin:
            aux_str = ""
            for inst in self.variables.compiled:
                aux_str += f"{inst}\n"
            self.code_edit.code_binar.configure(state="normal")
            self.code_edit.code_binar.delete("1.0", "end")
            self.code_edit.code_binar.insert("1.0", aux_str)
            self.code_edit.code_binar.configure(state="disabled")

    def clear_memory(self):
        """
        Limpa a memória percorrendo todos os itens e removendo-os
        """
        self.variables.memor_list = []
        for item in self.regs_and_mem.memor_table.get_children():
            self.regs_and_mem.memor_table.delete(item)
        for i in range(4000):
            temp = "odd"
            if i % 2 == 0:
                temp = "even"
            self.regs_and_mem.memor_table.insert("", index=tk.END, values=(i, ""), tags=temp)

    def clear_code(self):
        """
        Limpa os Widgets de texto da área de código
        """
        self.code_edit.code_input.delete("1.0", "end")
        self.code_edit.code_binar.configure(state="normal")
        self.code_edit.code_binar.delete("1.0", "end")
        self.code_edit.code_binar.configure(state="disabled")


interface = Interface()
