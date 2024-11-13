# TSP-solver-heuristica

Para executar o código, é necessário passar 5 parâmetros:
Nome do arquivo de entrada.tsp
Nome do arquivo de saída
Melhor solução conhecida
Heurística usada (NN, MST, GUL)
Nó inicial

Na pasta raiz do programa, contém um arquivo “config.txt”, no qual é possível configurar o diretório que contém os documentos de entrada e saída, respectivamente nos campos: INPUT_FILES, OUTPUT_FILES. Caso seja desejado alterar o diretorio, basta modificar o conteúdo de algum dos campos, como por exemplo: (INPUT_FILES:files/input), que faz com que o programa procure os arquivos de entrada dentro da pasta do programa na pasta files/input. 
OBS1: Se a pasta não estiver criada, o programa não irá gerar arquivos de saída. 
OBS2: Caso seja desejado ler/criar os arquivos no diretórios raiz da aplicação, basta omitir as informações dos campos  INPUT_FILES, OUTPUT_FILES.

Por questões de diferentes plataformas executando o mesmo código, foi implementado abertura de arquivos com diretórios completos ou parciais, dependendo de como o interpretador python foi instalado na máquina, opte por um métodos ou outro. Para escolher qual tipo utilizar, basta alterar o conteúdo da flag: COMPLETE_PATH do arquivos “congif.txt”, sentando valor true ou false.

EXEMPLOS DE EXECUÇÃO VÁLIDA:

$ python3 main.py a280.tsp result.txt 2555 NN 1
$ python main.py a280.tsp result.txt 2555 NN 1

obs: Dependendo do sistema operacional, pode ser necessário passar o caminho completo do executável da versão do python instalado em sua máquina.

C:/Users/luize/AppData/Local/Programs/Python/Python312/python.exe c:/Heuristica/TSP-solver-heuristica/tsp_solver_heuristica/main.py a280.tsp result.txt 2555 NN 1
