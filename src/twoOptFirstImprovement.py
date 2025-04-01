class TwoOpt:

    def __init__(self, grafo, solucao, custo_solucao, dimensao=None):
        self.grafo = grafo 
        self.solucao = solucao 
        self.custo_solucao = custo_solucao  
        self.dimensao = dimensao 

    def _calcular_custo(self, solucao):

        custo_total = 0.0

        # itera por cada par consecutivo de nós na rota, exceto o último nó.
        for i in range(len(solucao) - 1):
            n1, n2 = solucao[i], solucao[i + 1]
            # obtém o custo entre os dois nós
            custo = self.grafo[n1][n2] if self.grafo[n1][n2] is not None else self.grafo[n2][n1]
            custo_total += custo

        # custo para retornar ao nó inicial, fechando o ciclo.
        n1, n2 = solucao[-1], solucao[0]
        custo_total += self.grafo[n1][n2] if self.grafo[n1][n2] is not None else self.grafo[n2][n1]
        return custo_total

    def otimizar(self):
        tamanho = len(self.solucao)  # número de nós na solução.
        iteracao = 0  # contador de iterações do algoritmo.
        melhorou_alguma_vez = False  # se houve alguma melhoria.

        while True:
            melhorou = False  # melhorias na iteração atual.
            iteracao += 1 

            # tenta melhorar a solução atual testando todas as trocas possíveis.
            for i in range(tamanho - 1):
                for j in range(i + 2, tamanho):  # ignora nós adjacentes para evitar ciclos triviais.

                    # cria uma nova solução invertendo uma parte da rota.
                    nova_solucao = (
                        self.solucao[:i + 1] +  # primeira parte da rota mantida.
                        self.solucao[i + 1:j + 1][::-1] +  # parte do meio invertida.
                        self.solucao[j + 1:]  # ultima parte da rota mantida.
                    )

                    novo_custo = self._calcular_custo(nova_solucao)

                    if novo_custo < self.custo_solucao:
                        self.solucao = nova_solucao  
                        self.custo_solucao = novo_custo  
                        melhorou = True  # indica que houve melhoria.
                        melhorou_alguma_vez = True  # pelo menos uma melhoria ocorreu.
                        break  # sai do loop interno ao encontrar uma melhoria(first improvement)

                if melhorou:
                    break  # sai do loop externo ao encontrar uma melhoria.

            # se não houver melhorias na iteração atual encerra o loop principal.
            if not melhorou:
                break

        return self.custo_solucao, melhorou_alguma_vez
