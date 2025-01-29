from src.graspVizinhoMaisProximo import vizinho_mais_proximo
from src.graspTwoOpt import TwoOptGrasp

class GRASP:
    def __init__(self, matriz_adjacencia, dimensao, max_iteracoes, alfa):
        self.matriz_adjacencia = matriz_adjacencia
        self.dimensao = dimensao
        self.max_iteracoes = max_iteracoes
        self.alfa = alfa  # Controle da aleatoriedade (valores entre 0 e 1)

    def construir_solucao(self, no_inicial):
        # Usa a função vizinho_mais_proximo com o controle de aleatoriedade para construir a solução inicial
        custo, solucao = vizinho_mais_proximo(
            matriz=self.matriz_adjacencia,
            orig=no_inicial,
            num_nos=self.dimensao,
            alfa=self.alfa
        )
        return custo, solucao  # Retorna o custo e a solução construída

    def busca_local(self, solucao, custo_inicial):
        # Usa a classe TwoOpt para aprimorar a solução
        otimizador = TwoOptGrasp(
            grafo=self.matriz_adjacencia,
            solucao=solucao,
            custo_solucao=custo_inicial,
            dimensao=self.dimensao
        )
        return otimizador.otimizar()

    def executar(self, no_inicial):
        melhor_solucao_global = None
        melhor_custo_global = float('inf')

        for _ in range(self.max_iteracoes):
            # Fase de construção
            custo_inicial, solucao_inicial = self.construir_solucao(no_inicial)

            # Fase de busca local
            solucao_final, custo_final = self.busca_local(solucao_inicial, custo_inicial)
            # Atualiza a melhor solução global
            if custo_final < melhor_custo_global:
                melhor_solucao_global = solucao_final
                melhor_custo_global = custo_final

        return melhor_solucao_global, melhor_custo_global