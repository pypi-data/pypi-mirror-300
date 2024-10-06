from classes import Cliente, PessoaFisica, Conta, ContaCorrente, Transacao, Deposito, Saque, Historico


# Menu de opções do usuário
def menu():
    menu = """\n
======= Bem-Vindo ao nosso Sistema Bancário =======

* Informe o tipo de operação que deseja realizar *
[1] - Depósito
[2] - Saque
[3] - Extrato
[4] - Novo Cliente
[5] - Nova Conta
[6] - Listar Clientes
[7] - Listar Contas
[0] - Sair
===================================================
=> """

    return input(menu)

# Função: encontra um cliente apartir do CPF
def encontrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função: encontra a primeira conta de um cliente
def encontrar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n ** O cliente não possui conta! **")
        return
    
    # FIXME: não permite o cliente escolher a conta 
    return cliente.contas[0]

# Função: realiza um depósito
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função: realiza um saque
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função: exibe o extrato de uma conta, apartir do CPF do cliente
def exibe_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return
    
    conta = encontrar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============= EXTRATO =============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\nNão houve movimentações na conta."

    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("====================================")

# Função: cria um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente:
        print("\n ** Já existe um cliente com esse CPF! **")
        return
    
    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(endereco=endereco, cpf=cpf, nome=nome, data_nasc=data_nasc)

    clientes.append(cliente)

    print("\n == Cliente criado com sucesso! ==")

# Função: cria uma nova conta para um cliente específico, apartir do CPF
def criar_conta(nro_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if not cliente:
        print("\n ** Cliente não encontrado! **")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=nro_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n == Conta criada com sucesso! ==")

# Função: lista todos os clientes
def listar_clientes(clientes): 
    for cliente in clientes:
        print("=" * 40)
        print(str(cliente))

# Função: lista todas as contas 
def listar_contas(contas): 
    for conta in contas:
        print("=" * 40)
        print(str(conta))

# Inicia o sistema bancário
def main():
    clientes = []
    contas = []

    while True:

        option = menu()

        if option == '1':
            depositar(clientes)

        elif option == '2':
            sacar(clientes)

        elif option == '3':
            exibe_extrato(clientes)

        elif option == '4':
            criar_cliente(clientes)

        elif option == '5':
            nro_conta = len(contas) + 1
            criar_conta(nro_conta, clientes, contas)

        elif option == '6':
            listar_clientes(clientes)
        
        elif option == '7':
            listar_contas(contas)
           
        elif option == '0':
            break

        else:
            print('Operação falhou! Selecione uma opção válida.')


main()