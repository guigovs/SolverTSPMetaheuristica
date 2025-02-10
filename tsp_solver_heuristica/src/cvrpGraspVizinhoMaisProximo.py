from src.cvrpProblemModel import CvrpData

import random

def vizinho_mais_proximo_cvrp(cvrp_data, alfa):
    num_nos = cvrp_data.dimension               # Número total de nós (incluindo o depósito)
    matriz = cvrp_data.adjacency_matrix         # Matriz de distâncias entre os nós
    demandas = cvrp_data.nodes_demand           # Lista de demandas de cada cliente
    capacidade_veiculo = cvrp_data.capacity     # Capacidade máxima dos veículos
    deposito = cvrp_data.depot_index            # Índice do depósito

    # Lista que irá armazenar as rotas de todos os veículos
    rotas = []

    # Conjunto dos clientes que ainda precisam ser atendidos (exclui o depósito)
    clientes_pendentes = set(range(num_nos))
    clientes_pendentes.remove(deposito)  # Remove o depósito, pois não é um cliente a ser atendido

    # Continua criando rotas enquanto houver clientes pendentes
    while clientes_pendentes:
        # Inicia uma nova rota começando no depósito
        rota_atual = [deposito]
        capacidade_restante = capacidade_veiculo  # Capacidade disponível no veículo atual
        no_atual = deposito  # Começa do depósito

        # Constrói a rota atual adicionando clientes viáveis
        while True:
            candidatos = []

            # Avalia todos os clientes que ainda não foram atendidos
            for cliente in clientes_pendentes:
                demanda_cliente = demandas[cliente]

                # Verifica se o cliente cabe na capacidade restante do veículo
                if demanda_cliente <= capacidade_restante:
                    if no_atual < cliente and matriz[no_atual][cliente] is not None:
                        custo = matriz[no_atual][cliente]
                    elif no_atual > cliente and matriz[cliente][no_atual] is not None:
                        custo = matriz[cliente][no_atual]
                    else:
                        continue
                    # Adiciona o cliente à lista de candidatos junto com o custo
                    candidatos.append((cliente, custo))

            # Se não houver candidatos viáveis, encerra a construção da rota atual
            if not candidatos:
                break

            # Ordena os candidatos pelo menor custo (menor distância)
            candidatos.sort(key=lambda x: x[1])

            # Define o tamanho da RCL com base no alfa
            limite = int(len(candidatos) * alfa)
            limite = max(1, limite)  # Garante que a RCL tenha pelo menos um candidato
            rcl = candidatos[:limite]  # Seleciona os melhores candidatos para a RCL

            # Escolhe aleatoriamente o próximo cliente a partir da RCL
            proximo_no = random.choice(rcl)[0]

            # Atualiza a rota atual com o cliente selecionado
            rota_atual.append(proximo_no)
            # Atualiza a capacidade restante do veículo
            capacidade_restante -= demandas[proximo_no]
            # Remove o cliente da lista de pendentes, pois já foi atendido
            clientes_pendentes.remove(proximo_no)
            # Atualiza o nó atual para continuar a construção da rota
            no_atual = proximo_no

        # Após não ser possível adicionar mais clientes, retorna ao depósito
        rota_atual.append(deposito)
        # Adiciona a rota finalizada à lista de rotas
        rotas.append(rota_atual)

    # Calcula o custo total de todas as rotas construídas
    custo_total = 0.0
    for rota in rotas:
        # Percorre cada par de nós consecutivos na rota
        for i in range(len(rota) - 1):
            n1 = rota[i]
            n2 = rota[i + 1]
            # Obtém o custo entre os nós, considerando a matriz triangular
            if n1 < n2 and matriz[n1][n2] is not None:
                custo_total += matriz[n1][n2]
            elif n1 > n2 and matriz[n2][n1] is not None:
                custo_total += matriz[n2][n1]
            else:
                continue  # Ignora se o custo não está definido

    # Retorna o custo total e as rotas construídas
    return custo_total, rotas
