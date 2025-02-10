import src.AGvizinhoMaisProximo as vizinhoMaisProximo
import numpy as np
import random

class AG :
    def __init__(self, matriz_adjacencia, dimensao, demanda, mutacao_prob, populacao_size, orig, max_iteracoes, capacidade):
        self.max_iteracoes = max_iteracoes
        self.matriz_adjacencia = matriz_adjacencia
        self.dimensao = dimensao
        self.capacidade = capacidade
        self.mutacao_prob = mutacao_prob
        self.demanda = demanda
        self.orig = orig
        self.populacao_size = populacao_size
        self.populacao = []

    def inicializar_populacao(self) : 
        for _ in range(self.populacao_size):
            self.populacao.append(vizinhoMaisProximo.vizinho_mais_proximo(
                    self.matriz_adjacencia,
                    self.capacidade,
                    self.demanda,
                    self.orig,  # Depósito inicial
                    self.dimensao
                ))
            

    def avaliar(self, solucao):
        custo_total = 0
        for rota in solucao:
            for i in range(len(rota) - 1):
                if self.matriz_adjacencia[rota[i]][rota[i + 1]] is not None:
                    custo_total += self.matriz_adjacencia[rota[i]][rota[i + 1]]
        return custo_total  # Retorna o fitness
    
    def verificar_factibilidade(self, solucao):
        clientes_atendidos = set()

        for rota in solucao:
            demanda_total = 0

            for cliente in rota:
                if cliente != self.orig:  # Ignora o depósito
                    demanda_total += self.demanda[cliente]
                    if cliente in clientes_atendidos:
                        return False  # Cliente visitado mais de uma vez
                    clientes_atendidos.add(cliente)

            if demanda_total > self.capacidade:
                return False  # Capacidade excedida

        # Verifica se todos os clientes foram atendidos
        if len(clientes_atendidos) != self.dimensao - 1:  # Ignora o depósito
            return False

        return True

    #algoritmo da roleta
    def selecao_pais(self, populacao):
        populacao.sort(key=lambda x: self.avaliar(x))
        melhores_pais = []
        for i in range(2):
            melhores_pais.append(populacao[i])
        return melhores_pais
    
    def mutacao(self, solucao):
        if random.random() < self.mutacao_prob:
            # Escolhe duas rotas diferentes
            rota1, rota2 = random.sample(solucao, 2)

            if len(rota1) > 2 and len(rota2) > 2:  # Garante que há clientes para trocar
                # Escolhe um cliente de cada rota
                cliente1 = random.choice(rota1[1:-1])  # Ignora o depósito
                cliente2 = random.choice(rota2[1:-1])  # Ignora o depósito

                # Troca os clientes entre as rotas
                if cliente2 not in rota1: 
                    rota1[rota1.index(cliente1)] = cliente2
                if cliente1 not in rota2:
                    rota2[rota2.index(cliente2)] = cliente1

        return solucao


    def recombinacao(self, pai1, pai2):
        # Seleciona uma rota de cada pai para trocar
        rota_pai1 = random.choice(pai1)
        rota_pai2 = random.choice(pai2)

        # Remove os clientes da rota selecionada do outro pai
        filho1 = [rota for rota in pai1 if rota != rota_pai1]
        filho2 = [rota for rota in pai2 if rota != rota_pai2]

        # Adiciona a rota do outro pai
        filho1.append(rota_pai2)
        filho2.append(rota_pai1)

        # Verifica e corrige clientes repetidos
        filho1 = self.corrigir_clientes_repetidos(filho1)
        filho2 = self.corrigir_clientes_repetidos(filho2)

        return filho1, filho2

    def corrigir_clientes_repetidos(self, solucao):
        clientes_visitados = set()
        novas_rotas = []

        for rota in solucao:
            nova_rota = [self.orig]  # Começa com o depósito
            for cliente in rota[1:-1]:  # Ignora o depósito inicial e final
                if cliente not in clientes_visitados:
                    nova_rota.append(cliente)
                    clientes_visitados.add(cliente)
            nova_rota.append(self.orig)  # Retorna ao depósito
            novas_rotas.append(nova_rota)

        return novas_rotas
    
    def execucao(self):
        melhor_solucao = None
        melhor_fitness = -float('inf')

        self.inicializar_populacao()

        print("População inicial:")
        for i in self.populacao:
            print(i)
            print()

        for _ in range(self.max_iteracoes):
            nova_populacao = []

            # Preserva a melhor solução da geração anterior (elitismo)
            melhor_da_geracao = max(self.populacao, key=self.avaliar)
            nova_populacao.append(melhor_da_geracao)
            # Geração de filhos com crossover
            for i in range((self.populacao_size - 1) // 2):
                pais = self.selecao_pais(self.populacao)

                filho1, filho2 = self.recombinacao(pais[0], pais[1])

                filho1 = self.mutacao(filho1)
                filho2 = self.mutacao(filho2)

                nova_populacao.extend([filho1, filho2])

            self.populacao = nova_populacao
            melhor_local = max(self.populacao, key=self.avaliar)
            fitness_local = self.avaliar(melhor_local)

            if fitness_local > melhor_fitness:
                melhor_solucao = melhor_local[:]
                melhor_fitness = fitness_local

        return melhor_solucao, melhor_fitness