import subprocess

#python3 main.py pr76.tsp destino.dat 108159 GRASP 100-0.5-5

input_files = [
    #("a280.tsp", 2579),
    #("berlin52.tsp", 7542),
    #("ch130.tsp", 6110),
    #("ch150.tsp", 6528),
    #("d198.tsp", 15780),
    #("eil101.tsp", 629),
    #("eil51.tsp", 426),
    #("eil76.tsp", 538),
    #("kroA100.tsp", 21282),
    #("kroB100.tsp", 22141),
    #("kroC100.tsp", 20749),
    #("kroD100.tsp", 21294),
    #("kroE100.tsp", 22068),
    #("lin105.tsp", 14379),
    #("pr76.tsp", 108159),
    #("rat99.tsp", 1211),
    #("rd100.tsp", 7910),
    #("rd400.tsp", 15281),
    #("st70.tsp", 675),
    ("ts225.tsp", 126643),
]

#subprocess.run(["python3", "main.py", "pr76.tsp", "destino.dat", "108159", "GRASP", "100-0.5-5"])

iteracoes = [90]
alfas = [0.25,0.5,0.75]


for item in input_files:
    arquivo, best = item  # Garante que apenas um arquivo seja processado
    output = f"{arquivo[:-4]}_destino.dat"  # Nome do arquivo de saída baseado no nome do input
    print("combinacoes de ", item)
    for iteracao in iteracoes:
        for alfa in alfas:
            exec_list = ["python", "main.py", arquivo, output, str(best), "GRASP", f"{iteracao}-{alfa}-5"]
            print(f"Executando: {exec_list}")
            subprocess.run(exec_list)

print("Processo concluído.")
