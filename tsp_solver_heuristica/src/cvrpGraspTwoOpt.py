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
        # Soma as distâncias entre nós consecutivos da rota
        for i in range(len(rota) - 1):
            n1, n2 = rota[i], rota[i + 1]
            # Considerando a matriz triangular:
            if n1 < n2 and self.grafo[n1][n2] is not None:
                custo += self.grafo[n1][n2]
            elif n1 > n2 and self.grafo[n2][n1] is not None:
                custo += self.grafo[n2][n1]
            else:
                continue  
        return custo

    def _calcular_carga_rota(self, rota):
        carga = 0
        # Soma as demandas dos clientes na rota (desconsidera o depósito)
        for no in rota:
            if no != rota[0]:
                carga += self.demandas[no]
        return carga

    def otimizar(self):
        """
        Aplica melhorias combinando operadores intra-rotas (2-opt) e inter-rotas (realocação).
        Em cada iteração, avalia o melhor movimento global entre:
          - Movimentos 2-opt dentro de cada rota (inversão de subsequência)
          - Movimentos de realocação: retirar um cliente de uma rota e inserí-lo em outra,
            desde que respeite a capacidade e reduza o custo total.
        O loop encerra quando nenhuma melhoria for encontrada.
        """
        iteracao = 0
        while True:
            melhorou = False

            # Busca pelo melhor movimento 2-opt (intra-rota)
            melhor_delta_2opt_global = 0.0
            melhor_movimento_2opt = None  # (índice da rota, nova rota resultante)
            for idx, rota in enumerate(self.rotas):
                custo_atual = self._calcular_custo_rota(rota)
                n = len(rota)
                # Garantindo que a rota possua ao menos dois clientes
                if n < 4:
                    continue
                for i in range(1, n - 2):  # Inicia em 1 para não modificar o depósito inicial
                    for j in range(i + 1, n - 1):  # Termina em n-1 para não modificar o depósito final
                        nova_rota = rota[:i] + rota[i:j+1][::-1] + rota[j+1:]
                        # Checando se a rota é factível
                        if self._calcular_carga_rota(nova_rota) > self.capacidade_veiculo:
                            continue
                        novo_custo = self._calcular_custo_rota(nova_rota)
                        delta = custo_atual - novo_custo  # Se abaixou o custo
                        if delta > melhor_delta_2opt_global:
                            melhor_delta_2opt_global = delta
                            melhor_movimento_2opt = (idx, nova_rota)

            # Busca pelo melhor movimento de realocação (inter-rota)
            melhor_delta_realoc_global = 0.0
            melhor_movimento_realoc = None  #(rota_origem, pos_remocao, rota_destino, pos_insercao, nova_rota_origem, nova_rota_destino)
            for src_idx, rota_src in enumerate(self.rotas):
                # Verifica se há clientes para realocar 
                if len(rota_src) < 3:
                    continue
                custo_src_atual = self._calcular_custo_rota(rota_src)
                for pos in range(1, len(rota_src) - 1):  # Posições dos clientes 
                    candidato = rota_src[pos]
                    demanda_candidato = self.demandas[candidato]
                    nova_rota_src = rota_src[:pos] + rota_src[pos+1:]
                    novo_custo_src = self._calcular_custo_rota(nova_rota_src)
                    delta_src = custo_src_atual - novo_custo_src  # Se houve ganho na rota

                    # Tenta inserir o cliente em outra rota
                    for dst_idx, rota_dst in enumerate(self.rotas):
                        if dst_idx == src_idx:
                            continue
                        # Verifica capacidade na rota destino
                        if self._calcular_carga_rota(rota_dst) + demanda_candidato > self.capacidade_veiculo:
                            continue
                        custo_dst_atual = self._calcular_custo_rota(rota_dst)
                        # Tenta todas as posições possíveis de inserção na rota destino 
                        for ins in range(1, len(rota_dst)):
                            nova_rota_dst = rota_dst[:ins] + [candidato] + rota_dst[ins:]
                            novo_custo_dst = self._calcular_custo_rota(nova_rota_dst)
                            delta_dst = custo_dst_atual - novo_custo_dst  # Se houve ganho na rota destino
                            delta_total = delta_src + delta_dst
                            if delta_total > melhor_delta_realoc_global:
                                melhor_delta_realoc_global = delta_total
                                melhor_movimento_realoc = (src_idx, pos, dst_idx, ins, nova_rota_src, nova_rota_dst)

            # Escolhe e aplica o melhor movimento global 
            if melhor_delta_2opt_global <= 0 and melhor_delta_realoc_global <= 0:
                # Nenhum movimento melhora o custo total
                break

            if melhor_delta_2opt_global >= melhor_delta_realoc_global:
                # Aplica movimento 2-opt
                indice_rota, nova_rota = melhor_movimento_2opt
                custo_antigo = self._calcular_custo_rota(self.rotas[indice_rota])
                custo_novo = self._calcular_custo_rota(nova_rota)
                self.rotas[indice_rota] = nova_rota
                self.custo_total = self.custo_total - custo_antigo + custo_novo
                melhorou = True
            else:
                # Aplica movimento de realocação
                src_idx, pos, dst_idx, ins, nova_rota_src, nova_rota_dst = melhor_movimento_realoc
                custo_src_antigo = self._calcular_custo_rota(self.rotas[src_idx])
                custo_dst_antigo = self._calcular_custo_rota(self.rotas[dst_idx])
                custo_src_novo = self._calcular_custo_rota(nova_rota_src)
                custo_dst_novo = self._calcular_custo_rota(nova_rota_dst)
                self.rotas[src_idx] = nova_rota_src
                self.rotas[dst_idx] = nova_rota_dst
                self.custo_total = (self.custo_total 
                                    - custo_src_antigo - custo_dst_antigo 
                                    + custo_src_novo + custo_dst_novo)
                melhorou = True

            iteracao += 1

        return self.rotas, self.custo_total
