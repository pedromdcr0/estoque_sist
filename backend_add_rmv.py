import json
import time

id_item = None


def receber_id(id_recebido):
    global id_item
    id_item = int(id_recebido)
    return id_item


def retornar_item(id_do_item):
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)

        if id_do_item.isdigit():
            for item in data:
                if item["Id"] == int(id_do_item):
                    return item
            else:
                print("nao é numero")


def add_rmv(id_addrmv, tipo, quantidade, user):
    global id_item
    if tipo == 1:  # ADD
        with open("arquivos/estoque.json", "r") as estoque_file:
            dados_estoque = json.load(estoque_file)

        if any(item["Id"] == int(id_addrmv) for item in dados_estoque):
            dicio_editavel = [item for item in dados_estoque if item["Id"] == int(id_addrmv)]
            item = dicio_editavel[0]
            valor = item["Quantidade"] + quantidade
            item["Quantidade"] = valor
            print(item["Quantidade"])
            with open("arquivos/estoque.json", "w") as escrever_estoque:
                json.dump(dados_estoque, escrever_estoque, indent=4)
            id_item = None

            with open("arquivos/log.txt", "a") as log_file:
                log_soma_cadastro = (f"{time.asctime()} - SOMADO NO ESTOQUE ({quantidade}) -"
                                     f" {dicio_editavel} - POR: {user}\n")
                log_file.write(log_soma_cadastro)

        else:
            print("naotem")

    elif tipo == 2:  # RMV
        with open("arquivos/estoque.json", "r") as estoque_file:
            dados_estoque = json.load(estoque_file)

        if any(item["Id"] == int(id_addrmv) for item in dados_estoque):
            dicio_editavel = [item for item in dados_estoque if item["Id"] == int(id_addrmv)]
            item = dicio_editavel[0]
            valor = item["Quantidade"] - quantidade
            item["Quantidade"] = valor
            print(item["Quantidade"])
            with open("arquivos/estoque.json", "w") as escrever_estoque:
                json.dump(dados_estoque, escrever_estoque, indent=4)
            id_item = None

            with open("arquivos/log.txt", "a") as log_file:
                log_subtracao_cadastro = f"{time.asctime()} - SUBTRAIDO NO ESTOQUE ({quantidade}) - {dicio_editavel} - POR: {user}\n"
                log_file.write(log_subtracao_cadastro)

        else:
            pass


def checar_item(id_passed):
    with open("arquivos/estoque.json", "r") as estoque_file:
        dados_estoque = json.load(estoque_file)

    if any(item["Id"] == id_passed for item in dados_estoque):
        print('sem alert')
        return 0
    else:
        print('alert?')
        return 1


checar_item(4)
