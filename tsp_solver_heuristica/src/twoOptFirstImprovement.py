class TwoOpt:

    def __init__(self, grafo, solucao, custo_solucao, dimensao=None):

        self.grafo = grafo  
        self.solucao = solucao  
        self.custo_solucao = custo_solucao  
        self.dimensao = dimensao 

    def _calcular_custo(self, solucao):
        """Calcula o custo total da rota fornecida."""
        custo_total = 0.0
        # itera sobre todos os nós da solução, exceto o último
        for i in range(len(solucao) - 1):
            n1, n2 = solucao[i], solucao[i + 1]
            # obtem o custo entre dois nós se existir
            custo = self.grafo[n1][n2] if self.grafo[n1][n2] is not None else self.grafo[n2][n1]
            custo_total += custo

        # Adiciona o custo de retorno ao nó inicial fechando um ciclo
        n1, n2 = solucao[-1], solucao[0]
        custo_total += self.grafo[n1][n2] if self.grafo[n1][n2] is not None else self.grafo[n2][n1]
        return custo_total

    def otimizar(self):
        #executando o 2-opt
        tamanho = len(self.solucao)  
        iteracao = 0  
        while True:
            melhorou = False  # verificar se a solucao foi otimizada
            iteracao += 1

            # tentando melhorar a solucao com 2-Opt
            for i in range(tamanho - 1):
                for j in range(i + 2, tamanho):  # ignorando os vizinhos adjascentes
                    # nova solucao com a troca
                    nova_solucao = (
                        self.solucao[:i + 1] +  # primeira parte inalterada
                        self.solucao[i + 1:j + 1][::-1] +  # invertendo parte da solucao
                        self.solucao[j + 1:]  # ultima parte tambem inalterada
                    )

                    # custo da nova solucao
                    novo_custo = self._calcular_custo(nova_solucao)

                    if novo_custo < self.custo_solucao:
                        self.solucao = nova_solucao 
                        self.custo_solucao = novo_custo  
                        melhorou = True  
                        break  # encerrando ao encontrar a primeira melhoria

                if melhorou:
                    break  

            # se não houver mais melhorias termina a busca
            if not melhorou:
                break

        return self.custo_solucao, self.solucao
