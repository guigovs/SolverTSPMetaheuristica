from sys import argv, exit
from src.fileManager import FileManeger
from src.AgmPrim import prim
from src.utils import edges_size
import time


if __name__ == '__main__':

    args = argv[1:]
    if len(args) < 5:
        print("ERRO, Quantidade de parametros insuficientes.")
        exit(1)

    input_file = args[0]
    output_file = args[1]
    known_solution = args[2]
    metaheuristic = args[3]
    initial_node = args[4]

    #__ Ler Arquivo de entrada contendo o problema
    file_manager = FileManeger()
    input_data = file_manager.read_input_file(input_file)

    if input_data is None:
        print("ERRO, Arquivo de entrada nao encontrado. Considere checar a configuracao do programa no arquvio"
              "\n config.txt, para verificar qual diretorio 'e usado para procurar arquivos de entrada.")
        exit(1)
    elif input_data == -1:
        print("ERRO! O Arquivo de entrada apresenta inconsistencia.")
        exit(1)

    # __ Preparar para resolver problema
    input_infos, adj_matrix = input_data

    exec_init = time.time()
    list_nodes = prim(adj_matrix, int(initial_node), int(input_infos['dimension']))
    exec_end = time.time()
    exec_time = exec_end - exec_init

    '''tour = file_manager.read_tour_file("berlin52.opt.tour")
    if tour is None:
        print("ERRO!, nao foi possivel abrir o arquivo ")
    elif tour == -1:
        print("ERRO! inconsistencia no arquivo")
    else:
        print(tour[0]) # informacoes
        print(tour[1]) # caminho'''

    #__salvar execucao atual
    file_manager.save_result(
        input_file=input_file,
        metaheuristics_method=metaheuristic,
        innit_node=initial_node,
        objective="", # todo
        runtime=exec_time,
        gap="", #todo
        nodes=input_infos['dimension'],
        arcs=edges_size(int(input_infos['dimension']))
    )
