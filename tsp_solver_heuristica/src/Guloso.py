def guloso(matriz, orig, num_nos):  
    i = 0
    no = [orig]
    custo = 0
    
    while i < num_nos - 1:  # Subtrai 1 para parar antes de visitar o último nó
        for j in range(len(matriz[no[-1]]) - 1):
            # Verifica se o número atual é menor ou igual ao próximo e se já não foi visitado e se o no não é nulo
            if (matriz[no[-1]][j] is not None) and (matriz[j + 1][no[-1]] is not None) and (j not in no) and \
            (matriz[no[-1]][j] <= matriz[no[-1]][j + 1]):
                custo += matriz[no[-1]][j]
                no.append(j)
                break
            elif ( matriz[no[-1]][j + 1] is not None) and (j + 1 not in no):
                custo += matriz[no[-1]][j + 1]
                no.append(j + 1)
                break
            elif (matriz[j][no[-1]] is not None) and (matriz[j + 1][no[-1]] is not None) and (j not in no) and \
                 ( matriz[j][no[-1]] <= matriz[j + 1][no[-1]]):
                custo += matriz[j][no[-1]]
                no.append(j)
                break
            elif (matriz[j + 1][no[-1]] is not None) and (j + 1 not in no):
                custo += matriz[j + 1][no[-1]]
                no.append(j + 1)
                break
        i += 1

    # Volta ao nó inicial para fechar o ciclo do TSP
    if matriz[no[-1]][orig] is not None:
        custo += matriz[no[-1]][orig]
        no.append(orig)
    else:
        custo += matriz[orig][no[-1]]
        no.append(orig)

    print(custo)
    return custo
    