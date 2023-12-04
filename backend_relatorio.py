import json


def preencher_relatorio():
    dados_relatorio = []
    with open("arquivos/estoque.json", "r") as estoque_file:
        data = json.load(estoque_file)
        for item in data:
            if item["Quantidade"] < item["QuantidadeMinima"]:
                dados_relatorio.append(item)
            elif item["Quantidade"] <= 1.2 * item["QuantidadeMinima"]:
                dados_relatorio.append(item)
            else:
                pass

    return dados_relatorio
