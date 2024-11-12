from sys import argv, exit
from src.fileManager import FileManeger
from src.AgmPrim import prim
from src.vizinhoMaisProximo import vizinho_mais_proximo
from src.utils import edges_size, gap
import time


if __name__ == '__main__':

    args = argv[1:]
    if len(args) < 5:
        print("ERRO, Quantidade de parametros insuficientes.")
        exit(1)

    input_file = args[0]
    output_file = args[1]
    known_best_solution = args[2]
    metaheuristic = args[3].upper()
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

    cost = 0
    exec_init = time.time()
    if metaheuristic == "MST":
        cost = prim(adj_matrix, int(initial_node), int(input_infos['dimension']))

    elif metaheuristic == "NN":
        cost = vizinho_mais_proximo(adj_matrix, int(initial_node), int(input_infos['dimension']))

    else:
        print("ERRO! Metaheuristica nao encontrada.")
        exit(1)

    exec_end = time.time()
    exec_time = exec_end - exec_init
    gap_v = gap(fs_better=int(known_best_solution), fs=cost)

    # reduzindo numero flutuante
    cost = f"{cost:.4f}"
    gap_v = f"{gap_v:.4f}"

    #__salvar execucao atual
    file_manager.save_result(
        file_name=output_file,
        input_file=input_file,
        metaheuristics_method=metaheuristic,
        innit_node=initial_node,
        objective=cost,
        runtime=exec_time,
        gap=gap_v,
        nodes=input_infos['dimension'],
        arcs=edges_size(int(input_infos['dimension']))
    )


'''tour = file_manager.read_tour_file("berlin52.opt.tour")
    if tour is None:
        print("ERRO!, nao foi possivel abrir o arquivo ")
    elif tour == -1:
        print("ERRO! inconsistencia no arquivo")
    else:
        print(tour[0]) # informacoes
        print(tour[1]) # caminho'''
