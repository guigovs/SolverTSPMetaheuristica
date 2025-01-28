from sys import argv, exit
from src.fileManager import FileManeger
from src.AgmPrim import prim
from src.vizinhoMaisProximo import vizinho_mais_proximo
from src.Guloso import guloso
from src.utils import edges_size, gap
from src.firstImprovementSwap import FirstImprovWithSwap
from src.twoOptFirstImprovement import TwoOpt
from src.firstImprovementDnI import DeleteAndInsert
from src.grasp import GRASP
import time


if __name__ == '__main__':
    args = argv[1:]
    test_exec = False

    if args[-1] == "test":
        test_exec = True

    if len(args) < 5 or (len(args) == 5 and test_exec):
        print("ERRO, Quantidade de parametros insuficientes.")
        exit(1)

    input_file = args[0]
    output_file = args[1]
    known_best_solution = args[2]
    metaheuristic = args[3].upper()
    initial_node = args[4]


    #__Ler Arquivo de entrada contendo o problema
    file_manager = FileManeger()
    input_data = file_manager.read_input_file(input_file)

    if input_data is None:
        print("ERRO, Arquivo de entrada nao encontrado. Considere checar a configuracao do programa no arquivo"
              "\n config.txt, para verificar qual diretorio 'e usado para procurar arquivos de entrada.")
        exit(1)
    elif input_data == -1:
        print("ERRO! O Arquivo de entrada apresenta inconsistencia.")
        exit(1)

    #__Preparar para resolver problema
    input_infos, adj_matrix = input_data

    if metaheuristic != 'GRASP' and int(initial_node) > int(input_infos["dimension"])-1:
        print("ERRO! No inicial invalido, pois estrapola a quantidade de nos do grafo.")
        exit(1)

    cost = 0
    exec_init = time.time() # #------------- tempo ---------------------------------------------------------------------
    if metaheuristic == "MST":
        cost = prim(adj_matrix, int(initial_node), int(input_infos['dimension']))

    elif metaheuristic in ["NN", "FS-NN-SWAP", "FS-NN-2OPT", "FS-NN-DNI"]:
        cost, solution = vizinho_mais_proximo(adj_matrix, int(initial_node), int(input_infos['dimension']))
    
    elif metaheuristic == "GUL":
        cost = guloso(adj_matrix, int(initial_node), int(input_infos['dimension']))

        #__Uso da metaheurístca
    elif metaheuristic == "GRASP":
        list_params = initial_node.split('-')

        grasp = GRASP(
            matriz_adjacencia=adj_matrix,
            dimensao=int(input_infos['dimension']),
            max_iteracoes=int(list_params[0]),
            alfa=float(list_params[1])  # Controle da aleatoriedade (entre 0 e 1)
        )
        cost, solution = grasp.executar(no_inicial=int(list_params[2]))

    else:
        print("ERRO! Metaheuristica nao encontrada.")
        exit(1)

    #__Aprimorar resultado com busca local
    if metaheuristic == "FS-NN-SWAP":
        fsswap = FirstImprovWithSwap(adj_matrix, solution, cost, input_infos['dimension'])
        cost, find = fsswap.find_better()
        
    elif metaheuristic == "FS-NN-2OPT":
        two_opt = TwoOpt(adj_matrix, solution, cost, input_infos['dimension'])
        cost, find = two_opt.otimizar()
        print('-----------------------------------------', find)

    elif metaheuristic == "FS-NN-DNI":
        del_insert = DeleteAndInsert(adj_matrix, solution, cost, input_infos['dimension'])
        cost, find = del_insert.encontrar_otimizado()
        


    exec_end = time.time()
    exec_time = exec_end - exec_init
    #_______________________________________ fim Tempo ________________________________________________________________

    # informar se caso tenha solicitado aprimoramento, se o valor foi aprimorado
    # if find is not None and find:
    #     print("A solucao inicial foi aprimorada")
    # if find is not None and not find:
    #     print("A solucao inicial nao foi aprimorada")

    gap_v = gap(fs_better=int(known_best_solution), fs=cost)

    # reduzindo numero flutuante
    cost = f"{cost:.4f}"
    gap_v = f"{gap_v:.4f}"

    if not test_exec:
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
