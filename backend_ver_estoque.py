import json


def preencher_dados():
    dados = []
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)

        dados.clear()
        for item in data:
            dados.append(item)

    return dados


def preencher_notas(id_item):
    dados_notas = []
    print(id_item)
    nome = None
    with open('arquivos/estoque.json', "r") as estoque_file:
        estoque_data = json.load(estoque_file)
        if any(item["Id"] == int(id_item) for item in estoque_data):
            item_list = [item for item in estoque_data if item["Id"] == int(id_item)]
            item = item_list[0]
            nome = item['Nome']

    with open("arquivos/notas.json", "r") as notas_file:
        notas_data = json.load(notas_file)
        dados_notas.clear()
        item_list = [notas for notas in notas_data if notas["Item"] == nome]
        for item in item_list:
            dados_notas.append(item)

    print(dados_notas)

    return dados_notas
