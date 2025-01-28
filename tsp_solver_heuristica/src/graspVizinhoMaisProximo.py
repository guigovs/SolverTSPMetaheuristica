import random

def vizinho_mais_proximo(matriz, orig, num_nos, alfa) -> (float, list):
    rota = []  # Inicializa a rota final
    no_marcados = [orig]  # Lista de nós que já foram visitados
    no_atual = orig  # Define o nó atual como inicial
    qnt_visitados = 0  # Quantidade de nós visitados

    # Enquanto todos os nós não forem visitados
    while qnt_visitados < num_nos - 1:
        candidatos = []  # Lista de candidatos com custos
        for j in range(num_nos):
            if j == no_atual or j in no_marcados:  # Ignora o nó atual e os já visitados
                continue

            # Obtém o custo da matriz de adjacência
            if no_atual < j and matriz[no_atual][j] is not None:
                custo = matriz[no_atual][j]
            elif no_atual > j and matriz[j][no_atual] is not None:
                custo = matriz[j][no_atual]
            else:
                continue  # Ignora casos onde o custo não está definido

            # Adiciona o candidato à lista com seu custo
            candidatos.append((j, custo))

        # Ordena os candidatos por custo (crescente)
        candidatos.sort(key=lambda x: x[1])

        # Define a RCL com base no alfa
        limite = int(len(candidatos) * alfa)
        limite = max(1, limite)  # Garante pelo menos 1 candidato na RCL
        rcl = candidatos[:limite]

        # Escolhe um próximo nó aleatório da RCL
        proximo_no = random.choice(rcl)[0]

        no_marcados.append(proximo_no)  # Adiciona o nó encontrado aos visitados
        rota.append([no_atual, proximo_no])  # Atualiza a rota com o nó atual e próximo nó
        no_atual = proximo_no  # Atualiza o nó atual como o próximo nó
        qnt_visitados += 1

    # Retorno ao nó inicial após o fim
    rota.append([no_atual, orig])

    custo_total = 0.0
    # Calcula o custo total percorrendo a rota construída
    for n1, n2 in rota:
        if matriz[n1][n2] is not None:  # Parte superior direita
            custo_total += matriz[n1][n2]
        elif matriz[n2][n1] is not None:  # Parte transposta
            custo_total += matriz[n2][n1]

    return custo_total, no_marcados
