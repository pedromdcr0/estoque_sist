import json
import time


def editar(id_passed, novo_nome, nova_quantidade, tipo, user):
    with open("arquivos/estoque.json", "r") as estoque_file:
        dados_estoque = json.load(estoque_file)
        nome = novo_nome

        if any(item["Id"] == int(id_passed) for item in dados_estoque):
            item_editavel = [item for item in dados_estoque if item["Id"] == int(id_passed)]
            item = item_editavel[0]
            item_teste = item_editavel[0]

            if int(tipo) == 1:
                with open("arquivos/estoque.json", "r") as estoque_antigo_file:
                    estoque_antigo_data = json.load(estoque_antigo_file)
                    item_antes = [item for item in estoque_antigo_data if item["Id"] == int(id_passed)]

                item["Nome"] = nome.upper()
                item["QuantidadeMinima"] = int(nova_quantidade)
                with open("arquivos/estoque.json", "w") as novo_estoque_file:
                    json.dump(dados_estoque, novo_estoque_file, indent=4)

                with open("arquivos/log.txt", "a") as log_file:
                    log_edit3_cadastro = (f"{time.asctime()} - EDITADO NO CADASTRO (QUANT E NOME) - "
                                          f"{item_antes} - {item} - "
                                          f"POR: {user}\n")
                    log_file.write(log_edit3_cadastro)

            elif int(tipo) == 2:
                with open("arquivos/estoque.json", "r") as estoque_antigo_file:
                    estoque_antigo_data = json.load(estoque_antigo_file)
                    item_antes = [item for item in estoque_antigo_data if item["Id"] == int(id_passed)]

                item["QuantidadeMinima"] = int(nova_quantidade)
                print(item_teste["Nome"])
                item["Nome"] = item_teste["Nome"]
                with open("arquivos/estoque.json", "w") as novo_estoque_file:
                    json.dump(dados_estoque, novo_estoque_file, indent=4)

                with open("arquivos/log.txt", "a") as log_file:
                    log_edit1_cadastro = (f"{time.asctime()} - EDITADO NO CADASTRO (QUANT) - "
                                          f"{item_antes} - {item} - "
                                          f"POR: {user}\n")
                    log_file.write(log_edit1_cadastro)

            elif int(tipo) == 3:
                with open("arquivos/estoque.json", "r") as estoque_antigo_file:
                    estoque_antigo_data = json.load(estoque_antigo_file)
                    item_antes = [item for item in estoque_antigo_data if item["Id"] == int(id_passed)]

                print("item 3" + item_teste["Nome"])
                item["Nome"] = nome.upper()
                item["QuantidadeMinima"] = item_teste["QuantidadeMinima"]
                with open("arquivos/estoque.json", "w") as novo_estoque_file:
                    json.dump(dados_estoque, novo_estoque_file, indent=4)

                with open("arquivos/log.txt", "a") as log_file:
                    log_edit2_cadastro = (f"{time.asctime()} - EDITADO NO CADASTRO (NOME) - "
                                          f"{item_antes} - {item} - "
                                          f"POR: {user}\n")
                    log_file.write(log_edit2_cadastro)

            elif int(tipo) == 4:
                item["QuantidadeMinima"] = item_teste["QuantidadeMinima"]
                item["Nome"] = item_teste["Nome"]


def checar_item(id_item):
    with open("arquivos/estoque.json", "r") as estoque_file:
        estoque_data = json.load(estoque_file)

        if any(item["Id"] == int(id_item) for item in estoque_data):
            return True
        else:
            return False
