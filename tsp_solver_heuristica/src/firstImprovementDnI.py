class DeleteAndInsert:

    def __init__(self, grafo, solucao: list, custo_solucao, tamanho_problema):
        self.grafo = grafo
        self.solucao = solucao
        self.custo_solucao_atual = custo_solucao
        self.custo_solucao = float(custo_solucao)
        self.tamanho_problema = int(tamanho_problema)

    def _calcular_custo(self, solucao):
        # Cálculo do custo total percorrendo a rota construída

        custo_total = 0.0
        for i in range(len(solucao) - 1):
            no1, no2 = solucao[i], solucao[i + 1]

            if self.grafo[no1][no2] is not None:
                custo_total += self.grafo[no1][no2]
            elif self.grafo[no2][no1] is not None:
                custo_total += self.grafo[no2][no1]

        no1, no2 = solucao[-1], solucao[0]
        if self.grafo[no1][no2] is not None:
            custo_total += self.grafo[no1][no2]
        else:
            custo_total += self.grafo[no2][no1]

        return custo_total

    def encontrar_otimizado(self) -> tuple:
        """
        Função para aprimorar resultado atual, com busca em vizinhança gerada por Delete-and-Insert.
        Interrompe a procura ao encontrar vizinho melhor que a solução atual, ou quando não existe melhor.
        :return: tupla com o valor resultado e um booleano que indica se a solução foi aprimorada ou não.
        """
        encontrado = False
        novo_custo_solucao = None

        for i in range(len(self.solucao)):
            for j in range(len(self.solucao)):
                if i == j:
                    continue  # Não é possível inserir na mesma posição

                vizinho = self.solucao.copy()
                no = vizinho.pop(i) # Realizando o Delete
                vizinho.insert(j, no) # Realizando o Insert

                novo_custo_solucao = self._calcular_custo(vizinho)

                if novo_custo_solucao < self.custo_solucao:
                    encontrado = True
                    break  # Finalizar busca na vizinhança

            if encontrado:
                break

        # Retornar resultado
        if encontrado:
            return novo_custo_solucao, encontrado
        else:
            return self.custo_solucao, encontrado
