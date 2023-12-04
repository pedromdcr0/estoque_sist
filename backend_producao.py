import json
import time


def producao_a():
    with open("arquivos/producao_a.json", "r") as producao_a_file:
        producao_a_data = json.load(producao_a_file)


def preencher_dados():
    dados = []
    with open("arquivos/producao_a.json", "r") as producao_a_file:
        data = json.load(producao_a_file)

        dados.clear()
        for item in data:
            dados.append(item)

    return dados


def pesquisar_dados(input_pesquisa, tipo):
    dados_retornados = []
    with open(f"arquivos/producao_{tipo}.json", "r") as estoque_producao_file:
        data = json.load(estoque_producao_file)

        for item in data:
            if input_pesquisa.upper() in item["Nome"]:
                dados_retornados.append(item)
    return dados_retornados
