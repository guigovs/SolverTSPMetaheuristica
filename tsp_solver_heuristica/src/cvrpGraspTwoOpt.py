from src.cvrpProblemModel import CvrpData

class TwoOptGraspCVRP:

    def __init__(self, cvrp_data, rotas, custo_total):
        self.grafo = cvrp_data.adjacency_matrix          # Matriz de distâncias entre os nós
        self.demandas = cvrp_data.nodes_demand           # Demandas dos clientes
        self.capacidade_veiculo = cvrp_data.capacity     # Capacidade máxima dos veículos
        self.rotas = rotas                               # Lista de rotas (solução inicial)
        self.custo_total = custo_total                   # Custo total das rotas

    def _calcular_custo_rota(self, rota):
        custo = 0.0
        # Percorre a rota somando as distâncias entre os nós
        for i in range(len(rota) - 1):
            n1, n2 = rota[i], rota[i + 1]
            # Acessa a matriz de adjacência considerando que ela pode ser triangular
            if n1 < n2 and self.grafo[n1][n2] is not None:
                custo += self.grafo[n1][n2]
            elif n1 > n2 and self.grafo[n2][n1] is not None:
                custo += self.grafo[n2][n1]
            else:
                continue  # Se o custo não está definido, ignora (ou trate conforme necessário)
        return custo

    def _calcular_carga_rota(self, rota):
        carga = 0
        # Soma as demandas dos clientes na rota (excluindo o depósito)
        for no in rota:
            if no != rota[0]:  # Assume que o depósito está na posição 0
                carga += self.demandas[no]
        return carga

    def otimizar(self):
        iteracao = 0  
        melhorou_alguma_vez = False  # Indica se houve alguma melhoria

        # Tenta melhorar as rotas até não haver mais melhorias
        while True:
            melhorou = False  # Indica melhorias na iteração atual
            iteracao += 1

            # Percorre todas as rotas
            for idx_rota, rota in enumerate(self.rotas):
                tamanho_rota = len(rota)
                custo_rota_atual = self._calcular_custo_rota(rota)  # Calcula o custo da rota atual uma vez
                # Tenta melhorar a rota atual 
                for i in range(1, tamanho_rota - 2):  # Começa em 1 para não remover o depósito inicial
                    for j in range(i + 1, tamanho_rota - 1):  # Termina em tamanho_rota - 1 para não remover o depósito final

                        # Cria uma nova rota invertendo uma subseção
                        nova_rota = rota[:i] + rota[i:j+1][::-1] + rota[j+1:]

                        # Verifica se a nova rota atende às restrições de capacidade
                        carga_nova_rota = self._calcular_carga_rota(nova_rota)
                        if carga_nova_rota > self.capacidade_veiculo:
                            continue  # Não aceita a nova rota se exceder a capacidade

                        # Calcula o novo custo da rota
                        novo_custo_rota = self._calcular_custo_rota(nova_rota)
                        # Calcula o novo custo total ajustado
                        novo_custo_total = self.custo_total - custo_rota_atual + novo_custo_rota

                        if novo_custo_total < self.custo_total:
                            # Atualiza a rota na solução
                            self.rotas[idx_rota] = nova_rota
                            # Atualiza o custo total
                            self.custo_total = novo_custo_total
                            melhorou = True
                            melhorou_alguma_vez = True
                            break  # Sai do loop interno (first improvement)

                    if melhorou:
                        break  # Se encontrou melhoria, sai do loop de 'i'

                if melhorou:
                    break  # Se encontrou melhoria, sai para a próxima iteração global

            # Se não houve melhorias na iteração atual, encerra o loop principal
            if not melhorou:
                break

        return self.rotas, self.custo_total
