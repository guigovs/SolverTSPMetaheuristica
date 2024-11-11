def prim(matriz, orig, num_nos):
  arvore = []
  no_marcados = [orig] #colocar a raiz
  linha = 0
  coluna = 0
  qnt_visitados = 0
  no_escolhido = 0
  menor_no = 9999

  while(qnt_visitados < num_nos-1):
    menor_no = 9999
    qnt_visitados += 1
    #olhar os nos visitados e pegar o menor custo
    for i in no_marcados:
      for j in range(len(matriz[i])):
        if(matriz[i][j] != None):
          if ((matriz[i][j] < menor_no)) and not(j in no_marcados):
            menor_no = matriz[i][j]
            linha = i
            coluna = j
            no_escolhido = j
          else:
            pass
        if (matriz[j][i] != None):
          if ((matriz[j][i] < menor_no)) and not(j in no_marcados):
            menor_no = matriz[j][i]
            linha = j
            coluna = i
            no_escolhido = j
          else:
            pass
    no_marcados.append(no_escolhido)
    arvore.append([linha,coluna])

    return arvore

