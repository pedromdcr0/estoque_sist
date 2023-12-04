import json
import time


def remover_item(id_item, user):
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)

        dicio_removido = [dicio for dicio in data if dicio["Id"] == id_item]

        novo_estoque = [dicio for dicio in data if dicio["Id"] != id_item]

        for item in novo_estoque:
            if item["Id"] > id_item:
                item["Id"] -= 1

        with open("arquivos/estoque.json", "w") as novo_estoque_file:
            json.dump(novo_estoque, novo_estoque_file, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_rmv_cadastro = (f"{time.asctime()} - REMOVIDO DO CADASTRO - {dicio_removido} - "
                                f"POR: {user}\n")
            log_file.write(log_rmv_cadastro)


def remover_nota(id_nota, user):
    with open("arquivos/notas.json", "r") as notas_file:
        data = json.load(notas_file)

        nota_removida = [nota for nota in data if nota["Nota"] == id_nota]

        novas_notas = [nota for nota in data if nota["Nota"] != id_nota]

        with open("arquivos/notas.json", "w") as novo_estoque_notas:
            json.dump(novas_notas, novo_estoque_notas, indent=4)

        with open("arquivos/log.txt", "a") as log_file:
            log_rmv_nota = f"{time.asctime()} - NOTA REMOVIDA - {nota_removida} - POR: {user}\n"
            log_file.write(log_rmv_nota)


