import AGvizinhoMaisProximo as vizinhoMaisProximo 
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
            self.populacao.append(vizinhoMaisProximo(
                    self.matriz_adjacencia,
                    self.capacidade,
                    self.demanda,
                    self.orig,  # Depósito inicial
                    self.dimensao
                ))
            

    def avaliar(self, solucao):
        for i in range(len(solucao) - 1):
            custo = sum(self.matriz_adjacencia[solucao[i]][solucao[i + 1]] )
        return 1 / custo if custo > 0 else 1e-6  # Retorna o fitness
    
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
    def selecao_pais(self):
        fitness = []
        probabilidades = []
        for sol in self.populacao:
            fitness.append(self.avaliar(sol))
        soma_fitness = sum(fitness)
        for f in fitness:
            probabilidades.append(f/soma_fitness)

        return self.populacao[np.random.choice(len(self.populacao), p=probabilidades)]
    
    def mutacao(self, solucao):
        while True:
            solucao_mutada = solucao[:]

            # Seleciona duas rotas aleatórias
            rota1_idx, rota2_idx = random.sample(range(len(solucao_mutada)), 2)
            rota1 = solucao_mutada[rota1_idx]
            rota2 = solucao_mutada[rota2_idx]

            # Seleciona um cliente de cada rota (ignorando o depósito)
            cliente1 = random.choice([cliente for cliente in rota1 if cliente != self.orig])
            cliente2 = random.choice([cliente for cliente in rota2 if cliente != self.orig])

            # Troca os clientes entre as rotas
            idx1 = rota1.index(cliente1)
            idx2 = rota2.index(cliente2)
            rota1[idx1], rota2[idx2] = rota2[idx2], rota1[idx1]

            # Verifica se a solução mutada é factível
            if self.verificar_factibilidade(solucao_mutada):
                return solucao_mutada

    def recombinacao(self, pai1, pai2):
        #crossover de ordem (OX) entre dois pais
        tamanho = len(pai1)
        filho = [None] * tamanho

        # Sorteia dois pontos de corte
        ponto1, ponto2 = sorted(random.sample(range(1, tamanho - 1), 2))

        # Copia segmento do pai1 para o filho
        filho[ponto1:ponto2] = pai1[ponto1:ponto2]

        # Preenche o restante com elementos do pai2 na ordem em que aparecem
        pos_filho = ponto2
        for gene in pai2:
            if gene not in filho:
                if pos_filho >= tamanho:
                    pos_filho = 0
                filho[pos_filho] = gene
                pos_filho += 1

        if self.verificar_factibilidade([filho]):
            return filho
    
def execucao(self):
    melhor_solucao = None
    melhor_fitness = -float('inf')

    self.inicializar_populacao()

    for _ in range(self.max_iteracoes):
        nova_populacao = []

        # Preserva a melhor solução da geração anterior (elitismo)
        melhor_da_geracao = max(self.populacao, key=self.avaliar)
        nova_populacao.append(melhor_da_geracao)

        # Geração de filhos com crossover
        for _ in range((self.populacao_size - 1) // 2):
            pai1 = self.selecao_pais()
            pai2 = self.selecao_pais()

            filho1 = self.recombinacao(pai1, pai2)
            filho2 = self.recombinacao(pai2, pai1)

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
