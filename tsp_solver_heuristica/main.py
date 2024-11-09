from sys import argv, exit
from src.fileManager import FileManeger


if __name__ == '__main__':

    args = argv[1:]
    if len(args) < 3:
        print("ERRO, Quantidade de parametros insuficientes.")
        exit(1)

    input_file = args[0]
    output_file = args[1]
    nome_heuristica = args[2]
    rest_params = args[3:]

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
    infos, adj_matrix = input_data
    print(infos)

    for i in adj_matrix:
        print(i)

