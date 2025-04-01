import os
from sys import argv, exit

from src.cvrpProblemModel import CvrpData
from src.fileManager import FileManeger
from src.cvrpProblemModel import CvrpData
from src.utils import string_is_float, gap, edges_size
from src.cvrpGraspy import GRASP_CVRP
from src.algoritmoGenetico import AG
from src.plotCVRP import plot_solution
import time

if __name__ == '__main__':
    metodo = None
    file_name = None
    output_file = None
    max_iteracoes = 0
    alfa = 0.0
    population_size = ""

    #        0       1               2               3               4
    # python.py  nomearquivo, arquvio_saida, metaheuristica, max_interacoes-alfa-geneticopopulacaosize,

    if len(argv) == 5:
        file_name = argv[1]
        output_file = argv[2]
        metodo = argv[3].upper()
        check = argv[4].split("-")

        if not metodo in ["GRASP", "GENETICO"]:
            print("ERRO! Utilize um metodo valido.")
            exit(0)

        if len(check) != 2 and metodo == "GRASP":
            print("ERRO! Formato aceito para grasp deve ser: numeroInteiro-numeroFloat")
            exit(0)
        elif len(check) != 3 and metodo == "GENETICO":
            print("ERRO! Formato aceito para genetico deve ser: numeroInteiro-numeroFloat-numeroInteiro")
            exit(0)

        else:
            if metodo == "GRASP":
                max_iteracoes, alfa = check
            else:
                max_iteracoes, alfa, population_size = check

            if not max_iteracoes.isdigit() or not string_is_float(alfa):
                print("ERRO, as iteracoes devem ser um numero inteiro e o alfa um numero de ponto flutuante.")
                exit(0)

            if metodo == "GENETICO":
                if population_size.isdigit():
                    population_size = int(population_size)
                else:
                    print("ERRO! O numero da populacao deve ser inteiro")
                    exit(0)


            max_iteracoes = int(max_iteracoes)
            alfa = float(alfa)

    elif len(argv) > 4:
        print("ERRO! Quantidade de parâmetros excedente.")
        exit(0)
    else:
        print("ERRO! Quantidade de parâmetros insuficientes.")
        exit(0)


    file_maneger = FileManeger()

    extracted_data = file_maneger.read_cvrp_instance(file_name)
    extracted_data : CvrpData

    melhor_custo = None
    melhor_solucao = None

    if file_name not in os.listdir(file_maneger.in_path):
        print(f"ERRO! Arquivo de entrada: {file_name} nao encontrado.")
        exit(0)

    exec_init = time.time()  # #------------- tempo
    if metodo == "GRASP":
        object_solver = GRASP_CVRP(extracted_data, max_iteracoes, alfa)
        melhor_solucao, melhor_custo = object_solver.executar()
        pass

    elif metodo == "GENETICO":
        object_solver = AG(
            matriz_adjacencia=extracted_data.adjacency_matrix,
            max_iteracoes=max_iteracoes,
            demanda=extracted_data.nodes_demand,
            dimensao=extracted_data.dimension,
            capacidade=extracted_data.capacity,
            mutacao_prob=alfa,
            populacao_size=population_size,
            orig=extracted_data.depot_index,
        )
        melhor_solucao, melhor_custo = object_solver.execucao()

    # _______________________________________ fim Tempo
    exec_end = time.time()
    exec_time = exec_end - exec_init

    if melhor_custo is not None and melhor_solucao is not None:
        print("\n---------------------- RESUMO -------------------------")

        # __validar solucao
        for route in melhor_solucao:
            carga = 0
            for node in route:
                carga += extracted_data.nodes_demand[node]

            if carga > extracted_data.capacity: # solucao invalida
                print("ERRO no solver. Solver gerou solucao inviavel!")
                exit(0)


        print(melhor_custo)
        print(melhor_solucao)

        gap_v = gap(fs_better=extracted_data.optimal_result, fs=melhor_custo)
        gap_v = f"{gap_v:.4f}"

        file_maneger.save_result(
            file_name=output_file,
            input_file=file_name,
            innit_node=argv[4],
            nodes=extracted_data.dimension,
            objective=extracted_data.optimal_result,
            metaheuristics_method=metodo,
            gap=gap_v,
            runtime=exec_time,
            arcs=edges_size(extracted_data.dimension)
        )

        #plot_solution(extracted_data, melhor_solucao)
