import json


def autenticar(username, password):
    with open("arquivos/login.json", "r") as login_file:
        data = json.load(login_file)
        usuario_encontrado = False

        for user in data:
            if user["Username"] == username:
                if user["Password"] == password:
                    if user["Admin"] == 1:
                        usuario_encontrado = True
                        print("admin")
                        return True
                    elif user["Admin"] == 0:
                        usuario_encontrado = True
                        print("nonadmin")
                        return False

        if not usuario_encontrado:
            print("naoencontrado")
            return None


def check_admin(username):
    with open("arquivos/login.json", "r") as login_file:
        data = json.load(login_file)
        for user in data:
            if user["Username"] == username:
                if user["Admin"] == 1:
                    print("user is admin")
                    return True

                elif user["Admin"] == 0:
                    print("user not admin")
                    return False



