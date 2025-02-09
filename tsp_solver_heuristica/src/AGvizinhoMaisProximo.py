def vizinho_mais_proximo(matriz, capacidade, demandas, orig, num_nos):
    """ Gera uma solução inicial respeitando a capacidade dos veículos """
    rota_final = []
    clientes_restantes = set(range(1, num_nos))  # Ignora o depósito
    capacidade_atual = 0
    no_atual = orig  # Começa pelo depósito
    rota_atual = [orig]

    while clientes_restantes:
        menor_custo = float('inf')
        proximo_no = None

        for cliente in clientes_restantes:
            custo = matriz[no_atual][cliente]
            if custo < menor_custo and (capacidade_atual + demandas[cliente] <= capacidade):
                menor_custo = custo
                proximo_no = cliente

        if proximo_no is None:
            # Se não puder adicionar mais clientes, retorna ao depósito e inicia nova rota
            rota_atual.append(orig)
            rota_final.append(rota_atual)
            capacidade_atual = 0
            no_atual = orig
            rota_atual = [orig]
        else:
            # Adiciona o cliente à rota
            rota_atual.append(proximo_no)
            capacidade_atual += demandas[proximo_no]
            clientes_restantes.remove(proximo_no)
            no_atual = proximo_no

    rota_atual.append(orig)  # Retorna ao depósito ao final
    rota_final.append(rota_atual)
    return rota_final