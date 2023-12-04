import json
import time


def adicionar_estoque(nome, quantidade, quantmin, unidade, user):
    novo_estoque = []
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)
        if len(data) >= 1:
            novo_id = data[-1]["Id"] + 1
        elif len(data) == 0:
            novo_id = 1

        novo_item = {"Id": novo_id, "Nome": nome.upper(), "Quantidade": int(quantidade), "QuantidadeMinima": int(quantmin), "Unidade": unidade.upper()}

        for item in data:
            novo_estoque.append(item)

        with open("arquivos/estoque.json", "w") as novo_estoque_file:
            novo_estoque.append(novo_item)
            json.dump(novo_estoque, novo_estoque_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_cadastro = f"{time.asctime()} - CADASTRO - {novo_item} - POR {user}\n"
            log_file.write(log_cadastro)


def cadastrar_nota(nome, fornecedor, nota, data, preco, user):
    novas_notas = []
    with open("arquivos/notas.json", "r") as notas_file:
        nota_data = json.load(notas_file)
        nota_add = {"Item": nome,
                    "Fornecedor": fornecedor.upper(),
                    "Nota": nota,
                    "Data": data,
                    "Preco": float(preco)}

        for item in nota_data:
            novas_notas.append(item)

        with open("arquivos/notas.json", "w") as novas_notas_file:
            novas_notas.append(nota_add)
            json.dump(novas_notas, novas_notas_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_cadastro_nota = f"{time.asctime()} - CADASTRO NOTA - {nota_add} - POR {user}\n"
            log_file.write(log_cadastro_nota)
