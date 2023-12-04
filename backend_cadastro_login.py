import json


def cadastro(usuario, senha, conf_senha, admin):
    with open("arquivos/login.json", "r") as login_file:
        login_data = json.load(login_file)
        lista_login = []
        login_passa = 1

        for login in login_data:
            lista_login.append(login)
            if usuario == login['Username']:
                print(usuario)
                print(login["Username"])
                login_passa = 0

        if login_passa == 1:
            if senha == conf_senha:
                novo_login = {"Username": usuario, "Password": senha, "Admin": admin}
                lista_login.append(novo_login)

                with open("arquivos/login.json", "w") as login_file_w:
                    json.dump(lista_login, login_file_w, indent=4)
                return True

            else:
                return False
