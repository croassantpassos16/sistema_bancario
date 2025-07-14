# Sistema Bancário - Estrutura Organizada com Regras de Parâmetros

usuarios = []
contas = []
qnt_usuarios = 0


def criar_usuario():
    global qnt_usuarios

    print("Criação de Usuário".center(50, "-"))
    nome = input("Nome completo: ")
    cpf = input("CPF: ")

    if buscar_usuario_por_cpf(cpf):
        print("CPF já cadastrado.")
        return

    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    senha = input("Crie uma senha (mín. 6 caracteres, letras e números): ")

    while len(senha) < 6 or not senha.isalnum():
        print("Senha inválida.")
        senha = input("Digite novamente a senha: ")

    codigo = f"USR{qnt_usuarios + 1:04d}"
    qnt_usuarios += 1

    usuario = {
        "codigo": codigo,
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "telefone": telefone,
        "senha": senha,
        "contas": []
    }

    usuarios.append(usuario)
    print(f"Usuário {nome} criado com sucesso!")
    criar_conta(usuario)


def criar_conta(usuario):
    numero = f"{len(contas) + 1:04d}"
    agencia = "0001"
    conta = {
        "numero": numero,
        "agencia": agencia,
        "saldo": 0.0,
        "limite": 1000.0,
        "usuario_codigo": usuario["codigo"],
        "titular": usuario["nome"],
        "extrato": [],
        "saques_realizados": 0
    }

    contas.append(conta)
    usuario["contas"].append(conta)
    print(f"Conta {numero} criada para {usuario['nome']} na agência {agencia}.")


def buscar_usuario_por_cpf(cpf):
    return next((u for u in usuarios if u["cpf"] == cpf), None)


def buscar_conta(numero):
    return next((c for c in contas if c["numero"] == numero), None)


def entrar_na_conta():
    print("Entrar na Conta".center(50, "-"))
    numero = input("Número da conta: ")
    cpf = input("CPF do titular: ")
    senha = input("Senha: ")

    conta = buscar_conta(numero)
    usuario = buscar_usuario_por_cpf(cpf)

    if not conta or not usuario:
        print("Dados incorretos.")
        return

    if usuario["senha"] != senha or conta["usuario_codigo"] != usuario["codigo"]:
        print("Credenciais inválidas.")
        return

    menu_conta(conta, usuario)


def menu_conta(conta, usuario):
    while True:
        print("\n" + "-" * 50)
        print(f"Olá, {usuario['nome']} | Conta: {conta['numero']}")
        print("[1] Ver Extrato")
        print("[2] Depositar")
        print("[3] Sacar")
        print("[4] Sair")
        opcao = input("Escolha a opção: ")

        if opcao == "1":
            ver_extrato(conta)
        elif opcao == "2":
            valor = float(input("Valor do depósito: R$"))
            depositar(conta, valor)
        elif opcao == "3":
            valor = float(input("Valor do saque: R$"))
            sacar(conta=conta, valor=valor)  
        elif opcao == "4":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida.")


def ver_extrato(conta):
    print("\n" + "=" * 50)
    print("EXTRATO".center(50))
    if conta["extrato"]:
        for item in conta["extrato"]:
            print(item)
    else:
        print("Nenhuma movimentação.")
    print(f"Saldo atual: R${conta['saldo']:.2f}")
    print("=" * 50)


def depositar(conta, valor, /):
    if valor <= 0:
        print("Valor inválido.")
    else:
        conta["saldo"] += valor
        conta["extrato"].append(f"Depósito: +R${valor:.2f}")
        print("Depósito realizado com sucesso.")


def sacar(*, conta, valor):
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500.0

    if conta["saques_realizados"] >= LIMITE_SAQUES:
        print("Limite diário de saques atingido.")
    elif valor > LIMITE_VALOR:
        print("Limite de saque excedido (máx. R$500 por operação).")
    elif valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor <= 0:
        print("Valor inválido.")
    else:
        conta["saldo"] -= valor
        conta["saques_realizados"] += 1
        conta["extrato"].append(f"Saque: -R${valor:.2f}")
        print(f"Saque de R${valor:.2f} realizado com sucesso.")

while True:
    print("\n" + "=" * 50)
    opcao = input("""SISTEMA BANCÁRIO:
[1] Criar Usuário
[2] Criar Conta (CPF já cadastrado)
[3] Entrar na Conta
[4] Sair
Escolha: """)

    if opcao == "1":
        criar_usuario()
    elif opcao == "2":
        cpf = input("Digite o CPF do usuário: ")
        usuario = buscar_usuario_por_cpf(cpf)
        if usuario:
            criar_conta(usuario)
        else:
            print("Usuário não encontrado.")
    elif opcao == "3":
        entrar_na_conta()
    elif opcao == "4":
        print("Sistema encerrado.")
        break
    else:
        print("Opção inválida.")
