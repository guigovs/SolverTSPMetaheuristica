class TwoOpt:

    def __init__(self, graph, solution, solution_cost, dimension=None):
        self.graph = graph
        self.solution = solution
        self.solution_cost = solution_cost
        self.dimension = dimension  # Agora você pode usar esse parâmetro dentro da classe

    def _calculate_cost(self, solution):
        """Calcula o custo total da rota fornecida."""
        total_cost = 0.0
        for i in range(len(solution) - 1):
            n1, n2 = solution[i], solution[i + 1]
            cost = self.graph[n1][n2] if self.graph[n1][n2] is not None else self.graph[n2][n1]
            total_cost += cost

        # Adiciona o custo de retorno ao nó inicial
        n1, n2 = solution[-1], solution[0]
        total_cost += self.graph[n1][n2] if self.graph[n1][n2] is not None else self.graph[n2][n1]
        print(f"Custo calculado para a solução {solution}: {total_cost:.4f}")
        return total_cost

    def optimize(self):
        """Executa o 2-Opt com primeiro aprimorante."""
        size = len(self.solution)
        iteration = 0  # Para controle de iteração
        while True:
            improved = False
            iteration += 1

            for i in range(size - 1):
                for j in range(i + 2, size):  # Ignorar vizinhos adjacentes
                    # Gerar uma nova solução aplicando o 2-Opt
                    new_solution = (
                        self.solution[:i + 1] +
                        self.solution[i + 1:j + 1][::-1] +
                        self.solution[j + 1:]
                    )

                    # Calcular o custo da nova solução
                    new_cost = self._calculate_cost(new_solution)

                    if new_cost < self.solution_cost:
                        self.solution = new_solution
                        self.solution_cost = new_cost
                        improved = True
                        break  # Primeiro aprimorante encontrado

                if improved:
                    break

            if not improved:
                break  # Não há mais melhorias possíveis

        return self.solution_cost, self.solution
