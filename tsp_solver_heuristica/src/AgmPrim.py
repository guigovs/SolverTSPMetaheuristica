def prim(matriz, orig, num_nos) -> float:
    arvore = []
    no_marcados = [orig] #colocar a raiz
    linha = 0
    coluna = 0
    qnt_visitados = 0
    no_escolhido = 0

    while qnt_visitados < num_nos-1:
      menor_no = 9999
      qnt_visitados += 1
      #olhar os nos visitados e pegar o menor custo
      for i in no_marcados:
        for j in range(len(matriz[i])):
          if matriz[i][j] is not None:
            if (matriz[i][j] < menor_no) and not(j in no_marcados):
              menor_no = matriz[i][j]
              linha = i
              coluna = j
              no_escolhido = j

          if matriz[j][i] is not None:
            if (matriz[j][i] < menor_no) and not(j in no_marcados):
              menor_no = matriz[j][i]
              linha = j
              coluna = i
              no_escolhido = j

      no_marcados.append(no_escolhido)
      arvore.append([linha,coluna])

    custo = 0.0
    for i in range(len(no_marcados)-1):
      n1, n2 = no_marcados[i], no_marcados[i+1]

      if matriz[n1][n2] is None:
        custo += matriz[n2][n1]

      elif matriz[n2][n1] is None:
        custo += matriz[n1][n2]

    print(f"Custo total da rota: {custo}")
    return custo
