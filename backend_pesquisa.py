import json


def pesquisa(input_pesquisa):
    dados_retornados = []
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)

        for item in data:
            if input_pesquisa.upper() in item["Nome"]:
                dados_retornados.append(item)
    return dados_retornados


def pesquisa_notas(input_pesquisa):
    dados_retornados = []
    with open("arquivos/notas.json", "r") as notas_file:
        notas_data = json.load(notas_file)

        for nota in notas_data:
            if input_pesquisa.upper() in nota["Fornecedor"]:
                dados_retornados.append(nota)

            elif str(input_pesquisa) in nota["Nota"]:
                dados_retornados.append(nota)

    return dados_retornados

