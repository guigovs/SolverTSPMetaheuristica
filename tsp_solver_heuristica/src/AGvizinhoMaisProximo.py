import random

def vizinho_mais_proximo(matriz, capacidade, demandas, orig, num_nos, k=3):
    rota_final = []
    clientes_restantes = set(range(1, num_nos))  # Ignora o depósito
    capacidade_atual = 0
    no_atual = orig  # Começa pelo depósito
    rota_atual = [orig]

    while clientes_restantes:
        # Encontra os k vizinhos mais próximos que cabem na capacidade
        vizinhos_candidatos = []
        for cliente in clientes_restantes:
            if matriz[no_atual][cliente] is not None:
                custo = matriz[no_atual][cliente]
                if capacidade_atual + demandas[cliente] <= capacidade:
                    vizinhos_candidatos.append((custo, cliente))

        # Ordena os candidatos pelo custo (menor custo primeiro)
        vizinhos_candidatos.sort(key=lambda x: x[0])

        # Seleciona aleatoriamente entre os k mais próximos
        if vizinhos_candidatos:
            k_vizinhos = vizinhos_candidatos[:k]
            custo, proximo_no = random.choice(k_vizinhos)
        else:
            proximo_no = None

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