import tkinter as tk
from tkinter import messagebox

usuarios = []
contas = []
qnt_usuarios = 0

usuario_selecionado = None
conta_selecionada = None

# Funções de negócio
def criar_usuario():
    global qnt_usuarios

    nome = entry_nome.get()
    cpf = entry_cpf.get()
    senha = entry_senha.get()

    if not nome or not cpf or not senha:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    if buscar_usuario_por_cpf(cpf):
        messagebox.showerror("Erro", "CPF já cadastrado.")
        return

    if len(senha) < 6 or not senha.isalnum():
        messagebox.showerror("Erro", "Senha inválida.")
        return

    codigo = f"USR{qnt_usuarios + 1:04d}"
    qnt_usuarios += 1

    usuario = {
        "codigo": codigo,
        "nome": nome,
        "cpf": cpf,
        "senha": senha,
        "contas": []
    }

    usuarios.append(usuario)
    criar_conta(usuario)
    atualizar_usuarios()
    messagebox.showinfo("Sucesso", f"Usuário {nome} criado!")

    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

def criar_conta(usuario):
    numero = f"{len(contas) + 1:04d}"
    conta = {
        "numero": numero,
        "saldo": 0.0,
        "extrato": [],
        "saques_realizados": 0,
        "usuario_codigo": usuario["codigo"]
    }
    contas.append(conta)
    usuario["contas"].append(conta)

def buscar_usuario_por_cpf(cpf):
    return next((u for u in usuarios if u["cpf"] == cpf), None)

def selecionar_usuario():
    global usuario_selecionado
    index = lista_usuarios.curselection()
    if not index:
        messagebox.showwarning("Seleção", "Selecione um usuário.")
        return
    usuario_selecionado = usuarios[index[0]]
    atualizar_contas()

def selecionar_conta():
    global conta_selecionada
    if not usuario_selecionado:
        messagebox.showwarning("Aviso", "Selecione um usuário primeiro.")
        return
    index = lista_contas.curselection()
    if not index:
        messagebox.showwarning("Seleção", "Selecione uma conta.")
        return
    conta_selecionada = usuario_selecionado["contas"][index[0]]
    atualizar_saldo()
    atualizar_extrato()

def atualizar_usuarios():
    lista_usuarios.delete(0, tk.END)
    for u in usuarios:
        lista_usuarios.insert(tk.END, f"{u['nome']} ({u['cpf']})")

def atualizar_contas():
    lista_contas.delete(0, tk.END)
    for c in usuario_selecionado["contas"]:
        lista_contas.insert(tk.END, f"Conta {c['numero']}")

def atualizar_saldo():
    label_saldo.config(text=f"Saldo: R${conta_selecionada['saldo']:.2f}")

def atualizar_extrato():
    extrato_texto.config(state=tk.NORMAL)
    extrato_texto.delete(1.0, tk.END)
    if conta_selecionada["extrato"]:
        for linha in conta_selecionada["extrato"]:
            extrato_texto.insert(tk.END, linha + "\n")
    else:
        extrato_texto.insert(tk.END, "Sem movimentações.")
    extrato_texto.config(state=tk.DISABLED)

def depositar(conta, valor, /):  # positional-only
    if valor <= 0:
        messagebox.showerror("Erro", "Valor inválido.")
        return
    conta["saldo"] += valor
    conta["extrato"].append(f"Depósito: +R${valor:.2f}")
    atualizar_saldo()
    atualizar_extrato()
    messagebox.showinfo("Sucesso", "Depósito realizado.")

def sacar(*, conta, valor):  # keyword-only
    if conta["saques_realizados"] >= 3:
        messagebox.showwarning("Limite", "Limite diário de saques atingido.")
    elif valor > 500:
        messagebox.showwarning("Limite", "Máximo R$500 por saque.")
    elif valor > conta["saldo"]:
        messagebox.showwarning("Erro", "Saldo insuficiente.")
    elif valor <= 0:
        messagebox.showerror("Erro", "Valor inválido.")
    else:
        conta["saldo"] -= valor
        conta["saques_realizados"] += 1
        conta["extrato"].append(f"Saque: -R${valor:.2f}")
        atualizar_saldo()
        atualizar_extrato()
        messagebox.showinfo("Sucesso", "Saque realizado.")

def realizar_deposito():
    if not conta_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma conta.")
        return
    try:
        valor = float(entry_valor.get())
        depositar(conta_selecionada, valor)
        entry_valor.delete(0, tk.END)
    except:
        messagebox.showerror("Erro", "Digite um valor válido.")

def realizar_saque():
    if not conta_selecionada:
        messagebox.showwarning("Aviso", "Selecione uma conta.")
        return
    try:
        valor = float(entry_valor.get())
        sacar(conta=conta_selecionada, valor=valor)
        entry_valor.delete(0, tk.END)
    except:
        messagebox.showerror("Erro", "Digite um valor válido.")

root = tk.Tk()
root.title("Sistema Bancário")
root.resizable(False, False)

frame_esquerdo = tk.Frame(root, padx=10, pady=10)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(frame_esquerdo, text="Criar Usuário", font=("Arial", 12, "bold")).pack(pady=5)

tk.Label(frame_esquerdo, text="Nome:").pack()
entry_nome = tk.Entry(frame_esquerdo, width=30)
entry_nome.pack()

tk.Label(frame_esquerdo, text="CPF:").pack()
entry_cpf = tk.Entry(frame_esquerdo, width=30)
entry_cpf.pack()

tk.Label(frame_esquerdo, text="Senha:").pack()
entry_senha = tk.Entry(frame_esquerdo, show="*", width=30)
entry_senha.pack()

tk.Button(frame_esquerdo, text="Criar Usuário", command=criar_usuario).pack(pady=8)

tk.Label(frame_esquerdo, text="Usuários Cadastrados:").pack(pady=5)
lista_usuarios = tk.Listbox(frame_esquerdo, width=35, height=8)
lista_usuarios.pack()
tk.Button(frame_esquerdo, text="Selecionar Usuário", command=selecionar_usuario).pack(pady=4)

tk.Label(frame_esquerdo, text="Contas do Usuário:").pack(pady=5)
lista_contas = tk.Listbox(frame_esquerdo, width=35, height=6)
lista_contas.pack()
tk.Button(frame_esquerdo, text="Selecionar Conta", command=selecionar_conta).pack(pady=8)



frame_direito = tk.Frame(root, padx=10, pady=10)
frame_direito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

label_saldo = tk.Label(frame_direito, text="Saldo: R$0.00", font=("Arial", 14, "bold"))
label_saldo.pack(pady=5)

frame_valor = tk.Frame(frame_direito)
frame_valor.pack(pady=10)
entry_valor = tk.Entry(frame_valor, width=15)
entry_valor.pack(side=tk.LEFT, padx=5)
tk.Button(frame_valor, text="Depositar", command=realizar_deposito).pack(side=tk.LEFT, padx=5)
tk.Button(frame_valor, text="Sacar", command=realizar_saque).pack(side=tk.LEFT, padx=5)

tk.Label(frame_direito, text="Extrato:").pack(pady=5)
extrato_texto = tk.Text(frame_direito, width=60, height=15, state=tk.DISABLED)
extrato_texto.pack()

root.mainloop()
