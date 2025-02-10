import subprocess

input_files = [
    ("A-n32-k5.vrp", 784),
    ("A-n33-k5.vrp", 661),
    ("A-n33-k6.vrp", 742),
    ("A-n34-k5.vrp", 778),
    ("A-n36-k5.vrp", 799),
    ("A-n37-k5.vrp", 669),
    ("A-n37-k6.vrp", 949),
    ("A-n38-k5.vrp", 730),
    ("A-n39-k5.vrp", 822),
    ("A-n39-k6.vrp", 831),
    ("A-n44-k6.vrp", 937),
    ("A-n45-k6.vrp", 944),
    ("A-n45-k7.vrp", 1146),
    ("A-n46-k7.vrp", 914),
    ("A-n48-k7.vrp", 1073),
    ("A-n53-k7.vrp", 1010),
    ("A-n54-k7.vrp", 1167),
    ("A-n55-k9.vrp", 1073),
    ("A-n60-k9.vrp", 1354),
    ("A-n61-k9.vrp", 1034),
    ("A-n62-k8.vrp", 1288),
    ("A-n63-k9.vrp", 1616),
    ("A-n63-k10.vrp", 1314),
    ("A-n64-k9.vrp", 1401),
    ("A-n65-k9.vrp", 1174),
    ("A-n69-k9.vrp", 1159),
    ("A-n80-k10.vrp", 1763)
]

grasp = True
alfas = [0.25, 0.5, 0.75]
populacoes = [20, 30, 40]


if grasp:
    iteracoes = [60, 90, 120]
    for item in input_files:
        arquivo, best = item  # Garante que apenas um arquivo seja processado
        output = f"{arquivo[:-4]}_destino.dat"  # Nome do arquivo de saída baseado no nome do input
        print("combinacoes de ", item)
        for iteracao in iteracoes:
            for alfa in alfas:
                exec_list = ["python", "main_cvrp.py", arquivo, output, "GRASP", f"{iteracao}-{alfa}"]
                print(f"Executando: {exec_list}")
                subprocess.run(exec_list)
else:
    iteracoes = [10, 20, 30]
    for item in input_files:
        arquivo, best = item  # Garante que apenas um arquivo seja processado
        output = f"{arquivo[:-4]}_destino.dat"  # Nome do arquivo de saída baseado no nome do input
        print("combinacoes de ", item)
        for iteracao in iteracoes:
            for alfa in alfas:
                for populacao in populacoes:
                    exec_list = ["python", "main_cvrp.py", arquivo, output, "GENETICO", f"{iteracao}-{alfa}-{populacao}"]
                    print(f"Executando: {exec_list}")
                    subprocess.run(exec_list)

print("Processo concluído.")
