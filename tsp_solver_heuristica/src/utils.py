import platform
from math import sqrt

def os_path_converter(path: str) -> str:
    """
        funcao para converter padrao de diretorios entre linux e windows
    """
    if platform.system().lower() == "linux":
        path = path.replace("\\", "/")
    else:
        path = path.replace("/", "\\")

    return path


def remove_emptys_list_and_casting(list_check: list, cast="") -> list:
    """
        Funcao para remover itens considerados vazios em uma lista: espacos apenas, quebras de linha,
        None, string vazia. Tambem faz troca de tipo de todos os dados.

        cast: FLOAT, INT, STRING

    """
    list_checked = []
    for item in list_check:
        item = item.strip()

        if item is not None and  item != "" and item != "\n":
            if cast == "":
                list_checked.append(item)
            elif cast == "STRING":
                list_checked.append(str(item))
            elif cast == "FLOAT":
                list_checked.append(float(item))
            elif cast == "INT":
                list_checked.append(int(item))

    return list_checked


def strip_list_elements(content_list:list) -> list:
    """
    Funcao para remocao de espacos desnecessarios em elementos do tipo string, dentro de uma lista
    """
    for i in range(len(content_list)):
        if type(content_list[i]) == str:
            content_list[i] = content_list[i].strip()
    return content_list


def node_distance(x1, y1, x2, y2):
    a = (x2 - x1) ** 2
    b = (y2 - y1) ** 2
    return sqrt(a + b)


def edges_size(graph_nodes_size):
    return int((graph_nodes_size * (graph_nodes_size - 1)) / 2)


def gap(fs_better, fs):
    mod = fs - fs_better
    if mod < 0:
        mod *= -1
    return 100 * (mod / fs_better)


def is_digit_positive_negative(string:str):
    if string.isdigit():
        return True
    elif string.startswith("-") and string[1:].isdigit():  # Verifica se é um número negativo
        return True
    else:
        return False


def fix_list_itens(lista: list)-> list | None:
    list_return = []

    if lista is not None:
        for item in lista:
            if item != "" and item != "\n":
                list_return.append(item.strip().rstrip())
        return list_return
    else:
        return None


def number_filter(string: str):
    buffer = ""
    for char in string:
        if char.isdigit():
            buffer += char

    return buffer