import json
import time


def producao_a():
    with open("arquivos/producao_a.json", "r") as producao_a_file:
        producao_a_data = json.load(producao_a_file)


def preencher_dados(tipo):
    dados = []
    with open(f"arquivos/producao_{tipo}.json", "r") as producao_file:
        data = json.load(producao_file)

        dados.clear()
        for item in data:
            dados.append(item)

    return dados


def checar_item(id_passed, tipo):
    with open(f"arquivos/producao_{tipo}.json", "r") as estoque_file:
        dados_estoque = json.load(estoque_file)

    if any(item["Id"] == id_passed for item in dados_estoque):
        print('sem alert')
        return 0
    else:
        print('alert?')
        return 1


def pesquisar_dados(input_pesquisa, tipo):
    dados_retornados = []
    with open(f"arquivos/producao_{tipo}.json", "r") as estoque_producao_file:
        data = json.load(estoque_producao_file)

        for item in data:
            if input_pesquisa.upper() in item["Nome"]:
                dados_retornados.append(item)
    return dados_retornados


def retornar_item(id_do_item, tipo):
    with open(f"arquivos/producao_{tipo}.json", "r") as estoque_file:
        data = json.load(estoque_file)

        if id_do_item.isdigit():
            for item in data:
                if item["Id"] == int(id_do_item):
                    return item
            else:
                print("nao é numero")


def change_quant(id_item, quantidade, tipo, user):
    with open(f"arquivos/producao_{tipo}.json", "r") as estoque_file:
        data = json.load(estoque_file)
        if any(item["Id"] == int(id_item) for item in data):
            dicio_editavel = [item for item in data if item["Id"] == int(id_item)]
            item = dicio_editavel[0]
            print(item)
            item["Quantidade"] = int(quantidade)
            print(item["Quantidade"])

            with open(f"arquivos/producao_{tipo}.json", "w") as estoque_write:
                json.dump(data, estoque_write, indent=4)

            with open("arquivos/log.txt", "a") as log_file:
                log_mudanca_cadastro = f"{time.asctime()} - MUDANÇA NO ESTOQUE {tipo} ({quantidade}) - {dicio_editavel} - POR: {user}\n"
                log_file.write(log_mudanca_cadastro)
