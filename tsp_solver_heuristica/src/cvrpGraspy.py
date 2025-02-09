from src.cvrpGraspVizinhoMaisProximo import vizinho_mais_proximo_cvrp
from src.cvrpGraspTwoOpt import TwoOptGraspCVRP

class GRASP_CVRP:
    def __init__(self, cvrp_data, max_iteracoes, alfa):
        self.cvrp_data = cvrp_data            # Dados do problema
        self.max_iteracoes = max_iteracoes    # Número máximo de iterações do GRASP
        self.alfa = alfa                      # Controle da aleatoriedade

    def construir_solucao(self):
        # Usa a função vizinho_mais_proximo_cvrp para construir a solução inicial
        custo, rotas = vizinho_mais_proximo_cvrp(
            cvrp_data=self.cvrp_data,
            alfa=self.alfa
        )
        return custo, rotas  # Retorna o custo e as rotas construídas

    def busca_local(self, rotas, custo_inicial):
        # Usa a classe TwoOptGraspCVRP para aprimorar as rotas
        otimizador = TwoOptGraspCVRP(
            cvrp_data=self.cvrp_data,
            rotas=rotas,
            custo_total=custo_inicial
        )
        return otimizador.otimizar()  # Retorna as rotas otimizadas e o custo total

    def executar(self):
        melhor_solucao_global = None         # Melhor conjunto de rotas encontrado
        melhor_custo_global = float('inf')   # Melhor custo total encontrado

        for i in range(self.max_iteracoes):
            print(f"Iteração {i + 1} de {self.max_iteracoes}")

            # Fase de construção
            custo_inicial, rotas_iniciais = self.construir_solucao()

            # Fase de busca local
            rotas_otimizadas, custo_otimizado = self.busca_local(rotas_iniciais, custo_inicial)

            # Atualiza a melhor solução global
            if custo_otimizado < melhor_custo_global:
                melhor_solucao_global = rotas_otimizadas
                melhor_custo_global = custo_otimizado

        return melhor_solucao_global, melhor_custo_global
