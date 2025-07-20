from abc import ABC, abstractmethod
from datetime import datetime

# Interface de transações
class Transacao(ABC):
    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def depositar(self, valor):
        pass

# Histórico de transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar(self, tipo, valor):
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transacoes.append(f"{data} - {tipo}: R${valor:.2f}")

    def listar(self):
        return self.transacoes

# Conta base
class Conta(Transacao):
    def __init__(self, numero, agencia, cliente):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self._saldo = 0
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de depósito deve ser positivo.")
        self._saldo += valor
        self.historico.adicionar("Depósito", valor)

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de saque deve ser positivo.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente.")
        self._saldo -= valor
        self.historico.adicionar("Saque", valor)

# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=1000, limite_saque=500):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

# Cliente base
class Cliente:
    def __init__(self, nome, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def __str__(self):
        return f"{self.nome} - CPF: {self.cpf} - Endereço: {self.endereco}"

    def atualizar_endereco(self, novo_endereco):
        self.endereco = novo_endereco

    def adicionar_conta(self, conta):
        if isinstance(conta, Conta):
            self.contas.append(conta)
        else:
            raise TypeError("A conta precisa ser uma instância da classe Conta.")

# Cliente PF
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, endereco, data_nascimento):
        super().__init__(nome, cpf, endereco)
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"{super().__str__()} - Nascimento: {self.data_nascimento}"

clientes = []
contas = []
cliente_logado = None

while True:
    print("\n📋 MENU DO SISTEMA BANCÁRIO")
    print("[1] Criar cliente")
    print("[2] Selecionar cliente")
    print("[3] Criar conta para cliente selecionado")
    print("[4] Depositar")
    print("[5] Sacar")
    print("[6] Ver extrato")
    print("[7] Trocar cliente")
    print("[0] Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")
        nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        novo_cliente = PessoaFisica(nome, cpf, endereco, nascimento)
        clientes.append(novo_cliente)
        print("✅ Cliente criado com sucesso!")

    elif opcao == "2":
        if not clientes:
            print("⚠️ Nenhum cliente cadastrado.")
            continue
        print("\nClientes disponíveis:")
        for i, c in enumerate(clientes):
            print(f"[{i}] {c}")
        idx = int(input("Escolha o número do cliente: "))
        cliente_logado = clientes[idx]
        print(f"✅ Cliente {cliente_logado.nome} selecionado.")

    elif opcao == "3":
        if not cliente_logado:
            print("⚠️ Selecione um cliente primeiro!")
            continue
        numero = len(contas) + 1
        agencia = "0001"
        nova_conta = ContaCorrente(numero, agencia, cliente_logado)
        cliente_logado.adicionar_conta(nova_conta)
        contas.append(nova_conta)
        print(f"✅ Conta criada com número {numero}.")

    elif opcao == "4":
        if not cliente_logado or not cliente_logado.contas:
            print("⚠️ Cliente sem conta.")
            continue
        for i, conta in enumerate(cliente_logado.contas):
            print(f"[{i}] Conta {conta.numero} - Saldo: R${conta.saldo:.2f}")
        idx = int(input("Escolha a conta: "))
        valor = float(input("Valor para depositar: "))
        cliente_logado.contas[idx].depositar(valor)
        print("✅ Depósito realizado.")

    elif opcao == "5":
        if not cliente_logado or not cliente_logado.contas:
            print("⚠️ Cliente sem conta.")
            continue
        for i, conta in enumerate(cliente_logado.contas):
            print(f"[{i}] Conta {conta.numero} - Saldo: R${conta.saldo:.2f}")
        idx = int(input("Escolha a conta: "))
        valor = float(input("Valor para sacar: "))
        try:
            cliente_logado.contas[idx].sacar(valor)
            print("✅ Saque realizado.")
        except ValueError as e:
            print(f"❌ {e}")

    elif opcao == "6":
        if not cliente_logado or not cliente_logado.contas:
            print("⚠️ Cliente sem conta.")
            continue
        for i, conta in enumerate(cliente_logado.contas):
            print(f"\n📄 Extrato da Conta {conta.numero}:")
            transacoes = conta.historico.listar()
            if not transacoes:
                print("Sem transações.")
            else:
                for t in transacoes:
                    print(t)
            print(f"Saldo atual: R${conta.saldo:.2f}")

    elif opcao == "7":
        cliente_logado = None
        print("🔁 Cliente deslogado.")

    elif opcao == "0":
        print("👋 Obrigado por usar o sistema!")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")
