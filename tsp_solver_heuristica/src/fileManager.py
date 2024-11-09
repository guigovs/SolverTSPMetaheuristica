from src.utils import os_path_converter, remove_emptys_list_and_casting, node_distance
import os

class FileManeger:

    def __init__(self):
        self.in_path = ""
        self.out_path = ""
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
        file = os_path_converter(self.in_path + "/" + file_name)

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
        for x in range(len(nodes)):
            for y in range(x, len(nodes)):
                if x == 0: # deve criar as linhas
                    adjacency_matrix.append([])

                if x == y: # ignorar caminho de Si pra si propio
                    adjacency_matrix[y].insert(x, "x")

                else:
                    x1, y1 = nodes[x][1], nodes[x][2]
                    x2, y2 = nodes[y][1], nodes[y][2]
                    distancia = node_distance(x1, y1, x2, y2)
                    adjacency_matrix[y].insert(x, distancia)

        return infos, adjacency_matrix
