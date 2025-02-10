class CvrpData:

    def __init__(self):
        self.nome = ""
        self.number_of_trucks = 0
        self.optimal_result = 0.0
        self.dimension = 0
        self.capacity = 0
        self.depot_index = 0
        self.adjacency_matrix = list()
        self.nodes_demand = list()
        self.nodes = list()

    def set_optimal_value(self, number):
        self.optimal_result = float(number)

    def set_number_of_trucks(self, number):
        self.number_of_trucks = int(number)

    def set_dimension(self, number):
        self.dimension = int(number)

    def set_depot(self, index):
        self.depot_index = int(index) - 1 # instancias numeram os nos de 1 a N.

    def set_capacity(self, number):
        self.capacity = int(number)
