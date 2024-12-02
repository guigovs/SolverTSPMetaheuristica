def vizinho_mais_proximo(matriz, orig, num_nos) -> (float, list):
    rota = [] #inicializar a rota final
    no_marcados = [orig] #lista de nos que ja foram visitados
    no_atual = orig #definindo o no atual como inicial
    qnt_visitados = 0 #verificar a quantidade de nos visitados

    # enquanto todos os nos nao forem visitados
    while qnt_visitados < num_nos - 1:
        menor_custo = float('inf') #inicializando o menor custo como infinito
        proximo_no = None # proximo no que sera visitado

        # percorre todos os nós para encontrar o nó mais próximo ainda não visitado
        for j in range(num_nos):
            if j == no_atual or j in no_marcados: # o no atual e os ja marcados serao ignorados
                continue

            # custo da matriz de adjacência considerando a parte superior direita
            if no_atual < j and matriz[no_atual][j] is not None:
                # se o nó atual é menor que o nó j, o custo está em matriz[no_atual][j]
                custo = matriz[no_atual][j]
            elif no_atual > j and matriz[j][no_atual] is not None:
                # se o nó atual é maior que o nó j, o custo está em matriz[j][no_atual]
                custo = matriz[j][no_atual]
            else:
                # se nao esta definido o custo, pula para o proximo no
                continue

            if custo < menor_custo: # verificando se o custo encontrado é o menor custo até agora
                menor_custo = custo
                proximo_no = j

        no_marcados.append(proximo_no) #colocando o no encontrado na lista de nos visitados
        rota.append([no_atual, proximo_no]) # atualizando a rota com o no atual e proximo no
        no_atual = proximo_no # atualizando o no atual como o proximo no
        qnt_visitados += 1 

    rota.append([no_atual, orig]) #retorno ao no inicial após o fim

    custo_total = 0.0

    # calculo do custo total percorrendo a rota construída
    for n1, n2 in rota:
        if matriz[n1][n2] is not None: # parte superior direita
            custo_total += matriz[n1][n2]
        elif matriz[n2][n1] is not None: # parte transposta
            custo_total += matriz[n2][n1]

    return custo_total, no_marcados
