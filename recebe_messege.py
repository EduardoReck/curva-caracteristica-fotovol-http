from checagem import check
def receive_message(result):
    """
    Processa os dados recuperados do dispositivo e atualiza as variáveis globais.

    Args:
        result (list): Lista de dados recuperados do dispositivo.
    Returns:
        tuple: Valores atualizados das variáveis de entrada.
    """
    # Inicializando as variáveis com valores padrão
    
    entrada1, entrada2, entrada3, entrada4 = -99, -99, -99, -99

    if result and isinstance(result, list):  # Verifica se result é uma lista não vazia
        print(f"\n=== Dados Recuperados ===")
        for data in result:
            if isinstance(data, dict) and 'variable' in data and 'value' in data:
                variable = data['variable']
                value = data['value']

                # Atualizando as variáveis de entrada com os valores recuperados
                if variable == 'icc':
                    entrada1 = value
                elif variable == 'vmp':
                    entrada2 = value
                elif variable == 'vca':
                    entrada3 = value
                elif variable == 'temperature':
                    entrada4 = value
                
                # Exibindo a variável recuperada
                print(f"Variavel: {variable}, Valor: {value}")
            else:
                print(f"Dado inválido encontrado: {data}")
        print("==========================\n")
    else:
        print("\nNenhum dado encontrado ou formato inválido.\n")
    check(entrada1,entrada2,entrada3,entrada4)
    return entrada1, entrada2, entrada3, entrada4
    