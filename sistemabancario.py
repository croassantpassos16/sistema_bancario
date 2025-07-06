menu = """

Sistema Bancário

Digite a opção desejada para continuar

[s] - Sacar
[d] - Depositar
[e] - Extrato
[q] - Sair

Qual opção você deseja?
"""

mensagem_saida = "\nObrigado por utilizar o sistema bancário!"

NUMERO_DE_SAQUES = 3
SAQUE_MAXIMO = 500
contagem_de_saques = 0
saldo = 0.0
extrato = []

def saque():
    
    global contagem_de_saques, saldo, extrato
    global NUMERO_DE_SAQUES, SAQUE_MAXIMO
    
    print("Saque".center(30, " "))
    
    if contagem_de_saques >= NUMERO_DE_SAQUES:
        print("\nNúmero máximo de saques atingido.")
        return
    
    if saldo <= 0:
        print("\nSaldo insuficiente para realizar o saque.")
        return
        
    while True:
        valor_do_saque = float(input("\nDigite o valor do saque: R$ "))
        
        if valor_do_saque <= 0:
            print("\nValor inválido. O valor do saque deve ser maior que zero.")
            continue
        
        if valor_do_saque > SAQUE_MAXIMO:
            print(f"\nValor inválido. O valor do saque não pode ser maior que R$ {SAQUE_MAXIMO:.2f}.")
            continue
        
        if valor_do_saque > saldo:
            print(f"\nSaldo insuficiente. Seu saldo atual é R$ {saldo:.2f}.")
            continue
        
        break
        
    contagem_de_saques += 1

    saldo -= valor_do_saque
    extrato.append(["Saque", valor_do_saque])
    
    print(f"\nSaque de R$ {valor_do_saque:.2f} realizado com sucesso!")
    print(f"Saldo atual: R$ {saldo:.2f}\n")
    
def deposito():

    global saldo, extrato
    
    print("Depósito".center(30, " "))

    while True:
        
        valor_do_deposito = float(input("\nDigite o valor do depósito: R$"))
        
        if valor_do_deposito <= 0:
            print("\nValor inválido. O valor do depósito deve ser maior que zero.")
            continue
        
        break
    
    saldo += valor_do_deposito
    extrato.append(["Depósito", valor_do_deposito])
    
    print(f"\nDepósito de R$ {valor_do_deposito:.2f} realizado com sucesso!")
    print(f"Saldo atual: R$ {saldo:.2f}\n")
    
def extrato():

    global saldo, extrato
    
    if not extrato:
        print("\nNenhuma transação realizada até o momento.")
        return
    
    print("\nExtrato".center(30, " "))
    print("\nTransações realizadas:\n")
    
    for transacao in extrato:
        tipo, valor = transacao
        print(f"{tipo}: R$ {valor:.2f}")
        
    print(f"\nSaldo atual: R$ {saldo:.2f}\n")
    
    
while True:
    
    opcao = input(menu).strip().lower()
    
    if opcao == 's':
        saque()
        tecla = input("\nPressione Enter para continuar...")
        
    elif opcao == 'd':
        deposito()
        tecla = input("\nPressione Enter para continuar...")
    
    elif opcao == 'e':
        extrato()
        tecla = input("\nPressione Enter para continuar...")
        
    elif opcao == 'q':
        print(mensagem_saida)
        break
    
    else:
        print("\nOpção inválida. Por favor, tente novamente.")

