#import matplotlib
#matplotlib.use('TkAgg')  # Ou 'Qt5Agg' dependendo do seu sistema
import matplotlib.pyplot as plt
import networkx as nx

from src.fileManager import FileManeger
from src.cvrpProblemModel import CvrpData


def plot_solution(obj:CvrpData, routes:list):
    graph = nx.Graph()

    # __caso omita o comeco e retorno do caminhao ao destino, adicionar automaticamente
    for route in routes:
        if route[0] != obj.depot_index:
            route.insert(0, obj.depot_index)
        if route[-1] != obj.depot_index:
            route.append(obj.depot_index)


    # __ VERTICES
    positions = dict()
    nodes_color = []
    for i, list_pos in enumerate(obj.nodes):
        if i == obj.depot_index:
            nodes_color.append("blue") # origem
        else:
            nodes_color.append("black") # clientes

        graph.add_node(i)
        positions[i] = (list_pos[1], list_pos[2])


    # __ ARESTAS
    colors_av = ["blue", "red", "green", "orange", "purple", "brown", "gray", "magenta", "cyan", "black", "yellow"]
    colors_ind = 0
    edges_color = dict()
    for route in routes:
        for i in range(len(route)):
            if i < len(route)-1:
                graph.add_edge(route[i], route[i+1])
                edges_color[(route[i], route[i+1])] = colors_av[colors_ind]
        colors_ind += 1
        if colors_ind == len(colors_av):
            colors_ind = 0


    # __ Montar lista de cores das arestas
    edge_color_list = []
    for edge in graph.edges():
        if edge in edges_color.keys():
            edge_color_list.append(edges_color[edge])
        else:
            x,y = edge
            edge_color_list.append(edges_color[(y,x)])


    # __ Exibir eixo x e y no plot
    plt.axhline(y=0, color="gray", linestyle="-", linewidth=1)  # Linha do eixo X
    plt.axvline(x=0, color="gray", linestyle="-", linewidth=1)  # Linha do eixo Y

    # __ Desenhar grafo com a solucao
    nx.draw(graph, positions, with_labels=False, node_color=nodes_color, edge_color=edge_color_list, node_size=10)
    plt.show()


"""
if __name__ == '__main__':
    _routes = [
        [21, 31, 19, 17, 13, 7, 26],
        [12, 1, 16, 30],
        [27, 24],
        [29, 18, 8, 9, 22, 15, 10, 25, 5, 20],
        [14, 28, 11, 4, 23, 3, 2, 6]
    ]

    _file_maneger = FileManeger()
    _obj = _file_maneger.read_cvrp_instance("A-n32-k5.vrp")
    plot_solution(_obj, _routes)
"""
