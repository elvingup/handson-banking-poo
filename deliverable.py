from abc import ABC, abstractclassmethod, abstractproperty
from datetime import date


class Historico:
    def __init__(self):
        self._historico = []

    def adicionar_transacao(self, transacao):
        self._historico.append(transacao)

    @property
    def historico(self):
        return self._historico


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.sacar(self.valor)
        conta.historico.adicionar_transacao(self)


class Conta:
    def __init__(self, numero, agencia, cliente, saldo=0):
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._saldo = saldo
        self._historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self._saldo
        excedeu_limite = valor > self._cliente.limite
        excedeu_saques = self._cliente.numero_saques >= self._cliente.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def saldo(self):
        return self._saldo

    @property
    def historico(self):
        return self._historico


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, saldo=0, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente, saldo)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    @property
    def numero_saques(self):
        return self._numero_saques


class PessoaFisica:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._endereco = endereco
        self._contas = []
        self.limite = 500
        self.limite_saques = 3
        self.numero_saques = 0

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas


class Banco:
    def __init__(self):
        self._usuarios = []
        self._contas = []
        self._agencia = "0001"

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = PessoaFisica(nome, cpf, date.fromisoformat(data_nascimento), endereco)
        self._usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            numero_conta = len(self._contas) + 1
            conta = ContaCorrente(numero_conta, self._agencia, usuario)
            usuario.adicionar_conta(conta)
            self._contas.append(conta)
            print("\n=== Conta criada com sucesso! ===")
            return

        print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

    def listar_contas(self):
        for conta in self._contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero}
                Titular:\t{conta.cliente.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self._usuarios if usuario.cpf == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def menu(self):
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == "d":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = self.filtrar_usuario(cpf)

                if usuario:
                    numero_conta = int(input("Informe o número da conta: "))
                    conta = next(
                        (conta for conta in usuario.contas if conta.numero == numero_conta),
                        None,
                    )

                    if conta:
                        valor = float(input("Informe o valor do depósito: "))
                        Deposito(valor).registrar(conta)
                    else:
                        print("\n@@@ Conta não encontrada! @@@")
                else:
                    print("\n@@@ Usuário não encontrado! @@@")

            elif opcao == "s":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = self.filtrar_usuario(cpf)

                if usuario:
                    numero_conta = int(input("Informe o número da conta: "))
                    conta = next(
                        (conta for conta in usuario.contas if conta.numero == numero_conta),
                        None,
                    )

                    if conta:
                        valor = float(input("Informe o valor do saque: "))
                        Saque(valor).registrar(conta)
                    else:
                        print("\n@@@ Conta não encontrada! @@@")
                else:
                    print("\n@@@ Usuário não encontrado! @@@")

            elif opcao == "e":
                cpf = input("Informe o CPF do titular da conta: ")
                usuario = self.filtrar_usuario(cpf)

                if usuario:
                    numero_conta = int(input("Informe o número da conta: "))
                    conta = next(
                        (conta for conta in usuario.contas if conta.numero == numero_conta),
                        None,
                    )

                    if conta:
                        print("\n================ EXTRATO ================")
                        print(
                            "Não foram realizadas movimentações."
                            if not conta.historico.historico
                            else "\n".join(
                                f"{t.data} - {t.tipo}: R$ {t.valor:.2f}"
                                for t in conta.historico.historico
                            )
                        )
                        print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
                        print("==========================================")
                    else:
                        print("\n@@@ Conta não encontrada! @@@")
                else:
                    print("\n@@@ Usuário não encontrado! @@@")

            elif opcao == "nu":
                self.criar_usuario()

            elif opcao == "nc":
                self.criar_conta()

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "q":
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    banco = Banco()
    banco.executar()