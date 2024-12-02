class FirstImprovWithSwap:

    def __init__(self, graph, solution:list, solution_cost, problem_size):
        self.graph = graph
        self.solution = solution
        self.atual_solution_cost = solution_cost
        self.solution_cost = float(solution_cost)
        self.problem_size = int(problem_size)


    def _cost_calculator(self, solution):
        """calculo do custo total percorrendo a rota construída"""

        total_cost = 0.0
        for i in range(len(solution)-1):
            n1, n2 = solution[i], solution[i+1]

            if self.graph[n1][n2] is not None: # parte superior direita
                total_cost += self.graph[n1][n2]
            elif self.graph[n2][n1] is not None: # parte transposta
                total_cost += self.graph[n2][n1]

        n1, n2 = solution[-1], solution[0]
        if self.graph[n1][n2] is not None:
            total_cost += self.graph[n1][n2]
        else:
            total_cost += self.graph[n2][n1]

        return total_cost


    def find_better(self) -> tuple:
        """
        Funcao para aprimorar resultado atual, com busca em vizinhanca gerada por swap. Interromependo a procura ao
        encontrar vizinho melhor que a solucao atual, ou quando nao existe melhor
        :return: tupla com o valor resultado e um booleano que indica se a solucao foi aprimorada ou nao.
        """
        find = False
        new_solution_cost = None

        for i in range(len(self.solution)):
            for j in range(i + 1, len(self.solution)):
                neighborhood = self.solution.copy()
                #__fazendo o swap
                aux = neighborhood[i]
                neighborhood[i] = neighborhood[j]
                neighborhood[j] = aux

                #__percorrendo
                new_solution_cost = self._cost_calculator(neighborhood)

                if new_solution_cost < self.solution_cost:
                    find = True
                    break # Finalizar busca na vizinhanca

            if find:
                break

        #Retronar resultado
        if find:
            return new_solution_cost, find
        else:
            return self.solution_cost, find


    def find_better_expanded(self, max_iterations=1000000):
        iterations = 0
        solution = self.solution.copy()
        solution_cost = self.solution_cost

        while iterations < max_iterations:
            find = False
            for i in range(len(self.solution)):
                for j in range(i + 1, len(self.solution)):
                    neighborhood = solution.copy()
                    #__fazendo o swap
                    aux = neighborhood[i]
                    neighborhood[i] = neighborhood[j]
                    neighborhood[j] = aux

                    #__percorrendo
                    new_solution_cost = self._cost_calculator(neighborhood)

                    if new_solution_cost < solution_cost:
                        find = True
                        solution = neighborhood.copy()
                        solution_cost = new_solution_cost
                        break # Finalizar busca na vizinhanca

                    iterations += 1

                if find:
                    break

            if not find: # n obteve mais vizinhos melhores
                break
        #end while

        if self.solution_cost > solution_cost:
            return solution_cost, True
        else:
            return self.solution_cost, False


if __name__ == '__main__':
    pass


