from src.utils import (os_path_converter, remove_emptys_list_and_casting, node_distance, strip_list_elements,
                       is_digit_positive_negative)
import os

class FileManeger:

    def __init__(self):
        self.in_path = ""
        self.out_path = ""
        self.complete_path = None
        self.read_config_file()

    def read_config_file(self):
        """
            Funcao para obter a configuracao de entrada e saida do programa, para decidir onde os arquivos sao lidos
            e escritos.
        """
        try:
            with open("config.txt", "r") as file:
                file_content = file.readlines()

            for item in file_content:
                if item == "\n":
                    continue

                content = item.split(":")
                if content[1] != "\n" and content[1] != "":
                    if content[0] == "INPUT_FILES":
                        self.in_path = content[1]
                    elif content[0] == "OUTPUT_FILES":
                        self.out_path = content[1]
                    elif content[0] == "COMPLETE_PATH":
                        if content[1].lower().strip() == "true":
                            self.complete_path = True
                        else:
                            self.complete_path = False
        except:
            pass

        self.in_path = self.in_path.strip()
        self.out_path = self.out_path.strip()

        if self.in_path != "":
            self.in_path = os_path_converter(self.in_path)
        if self.out_path != "":
            self.out_path = os_path_converter(self.out_path)


    def read_input_file(self, file_name:str):
        """
        :param file_name: Apenas o nome do arquivo
        :return: tupla: (dicionario com informacoes do arquivo, lista de adjacencia com as distancias calculadas)
        A Lista de adjacencias e preenchida metade dela apenas, devido o grafo ser unidirecional, e a
        diagonal principal com valor X, para ser ignorada, uma vez que nao saimos de um no para ir para ele mesmo.
        """
        if not self.complete_path:
            file = self.in_path + "/" + file_name
        else:
            if self.in_path != "":
                file = f"{os.path.abspath(os.getcwd())}/{self.in_path}/{file_name}"
            else:
                file = f"{os.path.abspath(os.getcwd())}/{file_name}"

        file = os_path_converter(file)

        try:
            with open(file, "r") as file:
                line_content = file.readline().replace("\n", "")
                infos = {}
                moment = "read_info" # variavel de controle de contexto
                nodes = list()
                adjacency_matrix = list()
                ordered = True
                previous_node = None

                while line_content != "":
                    if moment == "read_info":
                        if line_content.strip().upper() == "NODE_COORD_SECTION":
                            moment = "coord"

                        elif line_content.find(":") != -1: # secao de configuracao
                            line_content = line_content.split(":")
                            line_content[0] = line_content[0].strip()
                            line_content[1] = line_content[1].strip()

                            if line_content[0].upper() == "NAME":
                                infos["name"] = line_content[1]
                            if line_content[0].upper() == "COMMENT":
                                infos["comment"] = line_content[1]
                            if line_content[0].upper() == "TYPE":
                                infos["type"] = line_content[1]
                            if line_content[0].upper() == "DIMENSION":
                                infos["dimension"] = line_content[1]
                            if line_content[0].upper() == "EDGE_WEIGHT_TYPE":
                                infos["edge_weitht_type"] = line_content[1]

                    elif moment == "coord":
                        if line_content.strip().upper() == "EOF":
                            pass
                        else:
                            nodes.append(remove_emptys_list_and_casting(line_content.split(" "), "FLOAT"))

                            if previous_node is not None and previous_node + 1 != nodes[-1][0]:
                                ordered = False
                            previous_node = nodes[-1][0]

                    line_content = file.readline().replace("\n", "")
                # Fim leitura do arquivo
        except:
            return None

        if not ordered:  # garantir que a lista de nos obedeca a ordem para facilitar manipulacao
            nodes = sorted(nodes, key=lambda xi: xi[0])

        if len(nodes) != int(infos["dimension"]):  # inconsistencia de informacoes
            return -1

        # x e y sao dois nos conectados sendo cada no uma tupla
        for y in range(len(nodes)):
            for x in range(len(nodes)):
                if y == 0: # deve criar as linhas
                    adjacency_matrix.append([])

                if x == y or x < y: # ignorar caminho de Si pra si propio
                    adjacency_matrix[y].insert(x, None)

                else:
                    x1, y1 = nodes[x][1], nodes[x][2]
                    x2, y2 = nodes[y][1], nodes[y][2]
                    distancia = node_distance(x1, y1, x2, y2)
                    adjacency_matrix[y].insert(x, distancia)

        return infos, adjacency_matrix


    def read_tour_file(self, file_name):
        """
        Funcao para leitura dos arquivos de resposta .tour.
        :return: 1: tupla:(informacoes do documento:dict, resposta:list)
                2: -1 em caso de erros de inconsistencia no arquivo
                3: None caso nao consiga abrir o arquivo
        """
        file_name = self.in_path + "/" + file_name
        file_name = os_path_converter(file_name)
        try:
            tour_file = open(file_name, "r")
        except:
            return None

        moment = "read_info"
        infos = dict()
        solution = list()

        file_content = tour_file.readline()
        while file_content != "":
            file_content = file_content.strip()

            if moment == "read_info" and file_content.find(":") != -1:
                content = strip_list_elements(file_content.split(":"))
                if content[0].upper() == "NAME":
                    infos["name"] = content[1]

                elif content[0].upper() == "TYPE":
                    infos["type"] = content[1]

                elif content[0].upper() == "DIMENSION":
                    infos["dimension"] = content[1]

            elif moment == "read_info" and file_content.upper() == "TOUR_SECTION":
                moment = "problem_solution"

            elif moment == "problem_solution":
                if file_content.upper() != "EOF":
                    if is_digit_positive_negative(file_content):
                        solution.append(float(file_content))
                    else:
                        return -1

            file_content = tour_file.readline()

        tour_file.close()

        if int(infos["dimension"]) != len(solution) - 1: # inconsistencia no arquivo
            return -1

        return infos, solution

    def save_result(self, file_name ,input_file, metaheuristics_method, innit_node, objective, runtime, gap, nodes, arcs):
        if not self.complete_path:
            file = self.out_path + "/" + file_name
        else:
            if self.out_path != "":
                file = f"{os.path.abspath(os.getcwd())}/{self.out_path}/{file_name}"
            else:
                file = f"{os.path.abspath(os.getcwd())}/{file_name}"

        path_result = os_path_converter(file)

        if os.path.exists(path_result):
            file_exists = True
        else:
            file_exists = False

        try:
            result_file = open(path_result, "a+")
        except:
            return None

        if not file_exists:
            result_file.write("INSTANCE\tMETHOD\tPARAM\tOBJECTIVE\tRUNTIME\tGAP\tNODES\tARCS")

        result_file.write(f"\n{input_file}\t{metaheuristics_method}\t{innit_node}"
                          f"\t{objective}\t{runtime}\t{gap}\t{nodes}\t{arcs}")

        result_file.close()
