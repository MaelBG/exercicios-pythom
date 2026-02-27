def calculadora():
    print("=== Calculadora Simples ===")
    print("Operações disponíveis:")
    print("1 - Soma")
    print("2 - Subtração")
    print("3 - Multiplicação")
    print("4 - Divisão")

    opcao = input("Escolha a operação (1/2/3/4): ")

    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))

    if opcao == "1":
        resultado = num1 + num2
        operacao = "soma"
    elif opcao == "2":
        resultado = num1 - num2
        operacao = "subtração"
    elif opcao == "3":
        resultado = num1 * num2
        operacao = "multiplicação"
    elif opcao == "4":
        if num2 == 0:
            print("Erro: divisão por zero não é permitida!")
            return
        resultado = num1 / num2
        operacao = "divisão"
    else:
        print("Opção inválida!")
        return

    print(f"Resultado da {operacao}: {resultado}")

calculadora()