import json
import time


def cadastro_a(nome, quantidade, quantmin, unidade, user):
    novo_estoque_producao = []
    with open("arquivos/producao_a.json", "a") as cadastro_a_file:
        data_a = json.load(cadastro_a_file)
        if len(data_a) >= 1:
            novo_id = data_a[-1]["Id"] + 1
        elif len(data_a) == 0:
            novo_id = 1

        novo_item = {"Id": novo_id, "Nome": nome.upper(), "Quantidade": int(quantidade),
                     "QuantidadeMinima": int(quantmin), "Unidade": unidade.upper()}

        for item in data_a:
            novo_estoque_producao.append(item)

        with open("arquivos/producao_a.json", "w") as novo_estoque_file:
            novo_estoque_producao.append(novo_item)
            json.dump(novo_estoque_producao, novo_estoque_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_cadastro = f"{time.asctime()} - CADASTRO PRODUÇÃO A - {novo_item} - POR {user}\n"
            log_file.write(log_cadastro)


def cadastro_b(nome, quantidade, quantmin, unidade, user):
    novo_estoque_producao = []
    with open("arquivos/producao_b.json", "a") as cadastro_b_file:
        data_b = json.load(cadastro_b_file)
        if len(data_b) >= 1:
            novo_id = data_b[-1]["Id"] + 1
        elif len(data_b) == 0:
            novo_id = 1

        novo_item = {"Id": novo_id, "Nome": nome.upper(), "Quantidade": int(quantidade),
                     "QuantidadeMinima": int(quantmin), "Unidade": unidade.upper()}

        for item in data_b:
            novo_estoque_producao.append(item)

        with open("arquivos/producao_b.json", "w") as novo_estoque_file:
            novo_estoque_producao.append(novo_item)
            json.dump(novo_estoque_producao, novo_estoque_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_cadastro = f"{time.asctime()} - CADASTRO PRODUÇÃO A - {novo_item} - POR {user}\n"
            log_file.write(log_cadastro)


def cadastro_c(nome, quantidade, quantmin, unidade, user):
    novo_estoque_producao = []
    with open("arquivos/producao_c.json", "a") as cadastro_c_file:
        data_c = json.load(cadastro_c_file)
        if len(data_c) >= 1:
            novo_id = data_c[-1]["Id"] + 1
        elif len(data_c) == 0:
            novo_id = 1

        novo_item = {"Id": novo_id, "Nome": nome.upper(), "Quantidade": int(quantidade),
                     "QuantidadeMinima": int(quantmin), "Unidade": unidade.upper()}

        for item in data_c:
            novo_estoque_producao.append(item)

        with open("arquivos/producao_c.json", "w") as novo_estoque_file:
            novo_estoque_producao.append(novo_item)
            json.dump(novo_estoque_producao, novo_estoque_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_cadastro = f"{time.asctime()} - CADASTRO PRODUÇÃO A - {novo_item} - POR {user}\n"
            log_file.write(log_cadastro)