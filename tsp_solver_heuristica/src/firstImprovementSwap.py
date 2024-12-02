from random import randint

class FirstImprovWithSwap:

    def __init__(self, graph, solution:list, solution_cost, problem_size, neighborhood_size):
        self.graph = graph
        self.solution = solution
        self.atual_solution_cost = solution_cost
        self.solution_cost = float(solution_cost)
        self.problem_size = int(problem_size)
        #self.neighborhood_size = neighborhood_size
        self.neighborhood_size = int(problem_size) # todo reverter dps

    def cost_calculator(self, solution):
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


    def two_different_random_numbers(self):
        position1 = randint(1, self.problem_size)
        # Garantir que as duas posicoes serao diferetes
        while True:
            position2 = randint(1, self.problem_size)
            if position2 != position1:
                break

        return position1, position2


    def find_better(self): # todo implementar time-out dps
        new_solution = self.solution.copy()
        solution_cost = self.solution_cost
        trys = 0

        while True:
            find = False
            for i in range(self.neighborhood_size):
                position1, position2 = self.two_different_random_numbers()
                value1 = new_solution[position1-1]
                value2 = new_solution[position2-1]
                #fazendo o swap
                new_solution[position1-1] = value2
                new_solution[position2-1] = value1
                new_solution_cost = self.cost_calculator(new_solution)

                if new_solution_cost < solution_cost:
                    solution_cost = new_solution_cost
                    find = True
                    break # Finalizar busca na vizinhanca


            if find: # nao encontrou vizinho melhor
                break
            else:
                trys += 1
                if trys == 10000:
                    break

        if find:
            print("eua chei um")

        print(solution_cost, self.solution_cost)