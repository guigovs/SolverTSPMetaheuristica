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
        encontrado = True
        novo_custo_solucao = None
        aprimorado = False

        while encontrado:
            encontrado = False
            for i, no in enumerate(self.solucao):  # Usando enumerate para obter índice e elemento
                for j in range(len(self.solucao)):
                    if i == j:
                        continue  # Não é possível inserir na mesma posição

                    vizinho = self.solucao[:i] + self.solucao[i+1:]  # Remove o elemento na posição 'i' (Delete)
                    vizinho = vizinho[:j] + [no] + vizinho[j:]  # Insere o nó na posição 'j' (Insert)

                    # Calcular custo do vizinho
                    novo_custo_solucao = self._calcular_custo(vizinho)

                    if novo_custo_solucao < self.custo_solucao:
                        self.solucao = vizinho
                        self.custo_solucao = novo_custo_solucao
                        encontrado = True
                        aprimorado = True
                        break  # Finalizar busca na vizinhança

                if encontrado:
                    break

        # Retornar resultado
        if aprimorado:
            return novo_custo_solucao, aprimorado
        else:
            return self.custo_solucao, aprimorado
