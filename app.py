from flask import Flask, render_template, request, flash, redirect, session, url_for
import backend_relatorio as br
import backend_ver_estoque as bve
import backend_adicionar_item as bai
import backend_pesquisa as bp
import backend_remover_item as bri
import backend_add_rmv as bar
import backend_edit as bed
import backend_autenticar_login as bal
import backend_cadastro_login as bcl
import backend_cadastro_producao as bcp
import backend_producao as bpd
from datetime import datetime, timezone
from functools import wraps

app = Flask(__name__)

app.secret_key = "pão_com_ovo"
user = None


# def verificar_inatividade():
#     if 'ultima_interacao' in session:
#         ultima_interacao = session['ultima_interacao']
#         tempo_decorrido = datetime.datetime.now() - ultima_interacao
#         print(tempo_decorrido)
#         print(ultima_interacao)
#         if tempo_decorrido.total_seconds() > 10:  # 10 minutos de inatividade
#             session.clear()


@app.before_request
def atualizar_ultima_interacao():
    if 'user' in session:
        tempo_atual = datetime.now(timezone.utc)  # Utilize timezone.utc para obter um datetime com fuso horário
        if 'ultima_interacao' not in session or (tempo_atual - session.get('ultima_interacao', tempo_atual)).total_seconds() > 600:
            print(tempo_atual)
            session['ultima_interacao'] = tempo_atual
            return redirect('/')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/select_type')
def select_type():
    return render_template('select.html')


# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/relatorio')
@login_required
def relatorio():
    dados_relatorio = br.preencher_relatorio()

    return render_template('relatorio.html', dados=dados_relatorio)


@app.route('/a_relatorio')
@login_required
def a_relatorio():
    dados_relatorio = br.preencher_relatorio()

    return render_template('a_relatorio.html', dados=dados_relatorio)


@app.route('/ver_estoque')
@login_required
def ver_estoque():
    dados = bve.preencher_dados()

    return render_template('ver_estoque.html', dados=dados)


@app.route('/ver_estoque_notas', methods=["POST"])
@login_required
def ver_estoque_notas():
    id_item = request.form.get('input_info')
    notas = bve.preencher_notas(id_item)

    return render_template('ver_estoque_notas.html', notas=notas, id_item=id_item)


@app.route('/ver_estoque_notas_pesquisa', methods=["POST"])
@login_required
def ver_estoque_notas_pesquisa():
    input_pesquisado = request.form.get('input_pesquisa')
    dados_pesquisa = bp.pesquisa_notas(input_pesquisado)

    return render_template('ver_estoque_notas.html', notas=dados_pesquisa)


@app.route('/cadastrar_nota/<id_item>', methods=["POST"])
@login_required
def cadastrar_nota(id_item):
    item = bar.retornar_item(id_item)
    return render_template('/cadastrar_nota.html', item=item)


@app.route("/processar_cadastro/<nome>", methods=["POST"])
@login_required
def processar_cadastro(nome):
    fornecedor = request.form["fornecedor"]
    nota = request.form['nota']
    data = request.form['data']
    preco = request.form['preco']
    bai.cadastrar_nota(nome, fornecedor, nota, data, preco, user)
    return redirect('/ver_estoque')


@app.route("/excluir_nota", methods=["POST"])
@login_required
def excluir_nota():
    global user
    input_nota = request.form['input_nota']
    bri.remover_nota(str(input_nota), user)
    return redirect('/ver_estoque')


@app.route('/ver_estoque_pesquisa', methods=['POST'])
@login_required
def ver_estoque_pesquisa():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('ver_estoque.html', dados=dados_pesquisa)


@app.route('/a_ver_estoque_pesquisa', methods=['POST'])
@login_required
def a_ver_estoque_pesquisa():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('a_ver_estoque.html', dados=dados_pesquisa)


@app.route('/a_ver_estoque')
@login_required
def a_ver_estoque():
    dados = bve.preencher_dados()

    return render_template('a_ver_estoque.html', dados=dados)


@app.route('/ver_estoque_pesquisa', methods=['POST'])
@login_required
def a_pesquisa():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('a_ver_estoque.html', dados=dados_pesquisa)


@app.route('/add_item')
@login_required
def add_item():
    return render_template('add_item.html')


@app.route('/processar', methods=['POST'])
@login_required
def adicionar_item():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    quant_min = request.form['quantmin']
    unidade = request.form['unidade']

    if bai.adicionar_estoque(nome, quantidade, quant_min, unidade, user):
        flash('Item adicionado com sucesso', 'success')
    else:
        flash('Falha ao adicionar o item', 'error')

    return redirect('/add_item')


@app.route('/rmv_item')
@login_required
def rmv_item():
    dados = bve.preencher_dados()

    return render_template('rmv_item.html', dados=dados)


@app.route('/rmv_item_pesquisa', methods=['POST'])
@login_required
def pesquisa_rmv():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('rmv_item.html', dados=dados_pesquisa)


@app.route('/processoremoveritem', methods=['POST'])
@login_required
def remover_item():
    global user
    id_para_remover = request.form['id_input']
    if id_para_remover.isnumeric():
        bri.remover_item(int(id_para_remover), user)
    else:
        print("não é numero")

    return redirect('/rmv_item')


@app.route('/add_rmv', methods=['GET', 'POST'])
@login_required
def add_rmv():
    dados = bve.preencher_dados()
    item = request.form.get('id_input')

    return render_template('/add_rmv.html', dados=dados, item=item)


@app.route('/add_rmv_pesquisa', methods=['POST'])
@login_required
def pesquisa_add_rmv():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('add_rmv.html', dados=dados_pesquisa)


@app.route('/processoaddrmv', methods=['GET', 'POST'])
@login_required
def processo_add_rmv():
    if bar.checar_item(int(request.form.get('id_input'))) == 0:
        if request.form['action'] == 'add':
            tipo_proximo = 1
            item = request.form.get('id_input')
            return redirect(f'/processoadd/{item}/{tipo_proximo}')

        elif request.form['action'] == 'rmv':
            tipo_proximo = 2
            item = request.form.get('id_input')
            return redirect(f'/processormv/{item}/{tipo_proximo}')

    else:
        dados = bve.preencher_dados()
        mensagem = "alert('Este item não existe no estoque, verifique o id.')"
        return render_template("/add_rmv.html", dados=dados, mensagem=mensagem)


@app.route('/processoadd/<id_item>/<tipo>')
@login_required
def processo_add(id_item, tipo):
    print(id_item)
    id_do_item = bar.receber_id(id_item)

    print(id_do_item)
    item = bar.retornar_item(id_item)
    tipo_passado = tipo

    return render_template('add_rmv1.html', item=item, id_do_item=id_do_item, tipo_passado=tipo_passado)


@app.route('/processormv/<id_item>/<tipo>')
@login_required
def processo_rmv(id_item, tipo):
    print(id_item)
    id_do_item = bar.receber_id(id_item)

    print(id_do_item)
    item = bar.retornar_item(id_item)
    tipo_passado = tipo

    return render_template('add_rmv2.html', item=item, id_do_item=id_do_item, tipo_passado=tipo_passado)


@app.route('/processoadicionaitem/<id_item>/<tipo>', methods=['POST'])
@login_required
def adiciona_item(id_item, tipo):
    global user
    quantidade_para_adicionar = request.form.get('quant_input')
    bar.add_rmv(int(id_item), int(tipo), int(quantidade_para_adicionar), user)

    return redirect('/add_rmv')


@app.route('/a_add_rmv', methods=['GET', 'POST'])
@login_required
def a_add_rmv():
    dados = bve.preencher_dados()
    item = request.form.get('id_input')

    return render_template('/a_add_rmv.html', dados=dados, item=item)


@app.route('/a_add_rmv_pesquisa', methods=['POST'])
@login_required
def a_pesquisa_add_rmv():
    input_pesquisado = request.form['input_pesquisa']
    dados_pesquisa = bp.pesquisa(input_pesquisado)

    return render_template('a_add_rmv.html', dados=dados_pesquisa)


@app.route('/a_processoaddrmv', methods=['GET', 'POST'])
@login_required
def a_processo_add_rmv():
    if bar.checar_item(int(request.form.get('id_input'))) == 0:
        if request.form['action'] == 'add':
            tipo_proximo = 1
            item = request.form.get('id_input')
            return redirect(f'/a_processoadd/{item}/{tipo_proximo}')

        elif request.form['action'] == 'rmv':
            tipo_proximo = 2
            item = request.form.get('id_input')
            return redirect(f'/a_processormv/{item}/{tipo_proximo}')

    else:
        condicao = 1
        dados = bve.preencher_dados()
        mensagem = "alert('Este item não existe no estoque, verifique o id.')"
        return render_template("/a_add_rmv.html", dados=dados, mensagem=mensagem, condicao=condicao)


@app.route('/a_processoadd/<id_item>/<tipo>')
@login_required
def a_processo_add(id_item, tipo):
    print(id_item)
    id_do_item = bar.receber_id(id_item)

    print(id_do_item)
    item = bar.retornar_item(id_item)
    tipo_passado = tipo

    return render_template('a_add_rmv1.html', item=item, id_do_item=id_do_item, tipo_passado=tipo_passado)


@app.route('/a_processormv/<id_item>/<tipo>')
@login_required
def a_processo_rmv(id_item, tipo):
    print(id_item)
    id_do_item = bar.receber_id(id_item)

    print(id_do_item)
    item = bar.retornar_item(id_item)
    tipo_passado = tipo

    return render_template('a_add_rmv2.html', item=item, id_do_item=id_do_item, tipo_passado=tipo_passado)


@app.route('/a_processoadicionaitem/<id_item>/<tipo>', methods=['POST'])
@login_required
def a_adiciona_item(id_item, tipo):
    global user
    quantidade_para_adicionar = request.form.get('quant_input')
    bar.add_rmv(int(id_item), int(tipo), int(quantidade_para_adicionar), user)

    return redirect('/a_add_rmv')


@app.route('/editar_item', methods=["GET", "POST"])
@login_required
def editar_item():
    dados = bve.preencher_dados()
    return render_template('edit_item.html', dados=dados)


@app.route('/processoeditar', methods=["POST"])
@login_required
def processo_editar():
    id_item = request.form.get('id_input')

    if bed.checar_item(id_item):
        return redirect(f'/processoeditar2/{id_item}')
    else:
        return redirect('/editar_item')


@app.route('/processoeditar2/<id_item>', methods=["GET", "POST"])
@login_required
def processo_definitivo_editar(id_item):
    item = bar.retornar_item(id_item)

    return render_template('/edit_item_2.html', item=item, id_item=id_item)


@app.route('/editar/<id_item>', methods=["POST"])
@login_required
def editar(id_item):
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    print(nome, quantidade)
    tipo = None

    if quantidade.isdigit() or quantidade == "":
        if nome != "" and quantidade != "":
            tipo = 1
        elif nome == "" and quantidade != "":
            tipo = 2
        elif nome != "" and quantidade == "":
            tipo = 3
        elif nome == "" and quantidade == "":
            return redirect('/editar_item')
    else:
        return redirect('/editar_item')
    print(tipo)
    if id_item.isdigit():
        bed.editar(int(id_item), nome, quantidade, tipo, user)
    return redirect('/editar_item')


@app.route('/')
def login():
    global user
    user = None
    session.clear()
    return render_template('login.html')


@app.route('/autenticar', methods=["POST"])
def autenticar_login():
    global user
    username = request.form.get('username')
    password = request.form.get('password')
    session.clear()

    if bal.autenticar(username, password) is None:
        return redirect('/')
    elif not bal.autenticar(username, password):
        user = username
        session['user'] = username
        session["ultima_interacao"] = datetime.now(timezone.utc)
        return redirect('/select_type')
    elif bal.autenticar(username, password):
        user = username
        session['user'] = username
        session["ultima_interacao"] = datetime.now(timezone.utc)
        return redirect('/select_type')


@app.route("/autenticar_estoque")
def autenticar_estoque():
    if bal.check_admin(session["user"]):
        return redirect("/relatorio")

    elif not bal.check_admin(session["user"]):
        return redirect("/a_relatorio")


@app.route("/autenticar_producao")
def autenticar_producao():
    if bal.check_admin(session["user"]):
        return redirect("/producao")
    elif not bal.check_admin(session["user"]):
        return redirect("/b_producao")


@app.route('/cadastrar_login')
def cadastrar_login():
    return render_template('cadastrar_login.html')


@app.route("/processar_cadastro_login", methods=["POST"])
def processo_cadastro_login():
    username = request.form.get('usuario')
    senha = request.form.get('senha')
    conf_senha = request.form.get('conf_senha')
    admin = request.form.get('check')
    administrator = 0
    if admin is None:
        pass
    elif admin == 'on':
        administrator = 1
    print(administrator)

    if bcl.cadastro(username, senha, conf_senha, administrator):
        return redirect('/relatorio')
    else:
        return redirect('/cadastrar_login')


@app.route("/signup")
def signup():
    popup = False
    return render_template("signup.html", popup=popup)


@app.route("/signed_up", methods=["GET", "POST"])
def signingup():
    username = request.form.get('username')
    password = request.form.get('password')
    c_password = request.form.get('c_password')
    admin = request.form.get('check')
    administrator = 0
    if admin is None:
        pass
    elif admin == 'on':
        administrator = 1
    print(administrator)

    if bcl.cadastro(username, password, c_password, administrator):
        popup = 0
    else:
        popup = 1
    print(popup)

    return redirect(url_for('login', popup=popup))


@app.route("/producao")
@login_required
def producao():
    return render_template("producao.html")


@app.route("/cadastro_a")
@login_required
def cadastro_a():
    return render_template("cadastro_a.html")


@app.route("/cadastro_b")
@login_required
def cadastro_b():
    return render_template("cadastro_b.html")


@app.route("/cadastro_c")
@login_required
def cadastro_c():
    return render_template("cadastro_c.html")


@app.route("/processar_cadastro_a", methods=["POST"])
@login_required
def processar_cadastro_a():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    quant_min = request.form['quantmin']
    unidade = request.form['unidade']

    bcp.cadastro_a(nome, quantidade, quant_min, unidade, user)

    return redirect("/cadastro_a")


@app.route("/processar_cadastro_b", methods=["POST"])
@login_required
def processar_cadastro_b():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    quant_min = request.form['quantmin']
    unidade = request.form['unidade']

    bcp.cadastro_b(nome, quantidade, quant_min, unidade, user)

    return redirect("/cadastro_b")


@app.route("/processar_cadastro_c", methods=["POST"])
@login_required
def processar_cadastro_c():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    quant_min = request.form['quantmin']
    unidade = request.form['unidade']

    bcp.cadastro_c(nome, quantidade, quant_min, unidade, user)

    return redirect("/cadastro_c")


@app.route("/producao_a")
@login_required
def producao_a():
    dados = bpd.preencher_dados("a")
    return render_template("producao_a.html", dados=dados)


@app.route("/producao_a_pesquisa", methods=["POST"])
@login_required
def producao_a_pesquisa():
    input_pesquisa = request.form["input_pesquisa"]
    dados_pesquisa = bpd.pesquisar_dados(input_pesquisa, "a")
    return render_template("producao_a.html", dados=dados_pesquisa)


@app.route("/processo_producao_a", methods=["POST"])
@login_required
def processo_producao_a():
    id_input = request.form["id_input"]

    return redirect(f"/producao_a_1/{id_input}")


@app.route("/producao_a_1/<id_input>", methods=["GET", "POST"])
@login_required
def producao_a_1(id_input):
    item = bpd.retornar_item(id_input, "a")
    print(id_input)
    return render_template("producao_a_1.html", item=item, id_item=id_input)


@app.route("/producao_atual_a/<id_item>", methods=["GET", "POST"])
@login_required
def producao_atual(id_item):
    quantidade = request.form.get("quant_input")
    print(quantidade)
    bpd.change_quant(id_item, quantidade, "a", user)
    return redirect("/producao_a")


@app.route("/producao_b")
@login_required
def producao_b():
    dados = bpd.preencher_dados("b")
    return render_template("producao_b.html", dados=dados)


@app.route("/producao_b_pesquisa", methods=["POST"])
@login_required
def producao_b_pesquisa():
    input_pesquisa = request.form["input_pesquisa"]
    dados_pesquisa = bpd.pesquisar_dados(input_pesquisa, "b")
    return render_template("producao_b.html", dados=dados_pesquisa)


@app.route("/processo_producao_b", methods=["POST"])
@login_required
def processo_producao_b():
    id_input = request.form["id_input"]

    return redirect(f"/producao_b_1/{id_input}")


@app.route("/producao_b_1/<id_input>", methods=["GET", "POST"])
@login_required
def producao_b_1(id_input):
    item = bpd.retornar_item(id_input, "a")
    print(id_input)
    return render_template("producao_b_1.html", item=item, id_item=id_input)


@app.route("/producao_atual_b/<id_item>", methods=["GET", "POST"])
@login_required
def producao_atual_b(id_item):
    quantidade = request.form.get("quant_input")
    print(quantidade)
    bpd.change_quant(id_item, quantidade, "b", user)
    return redirect("/producao_b")


@app.route("/producao_c")
@login_required
def producao_c():
    dados = bpd.preencher_dados("c")
    return render_template("producao_c.html", dados=dados)


@app.route("/producao_c_pesquisa", methods=["POST"])
@login_required
def producao_c_pesquisa():
    input_pesquisa = request.form["input_pesquisa"]
    dados_pesquisa = bpd.pesquisar_dados(input_pesquisa, "c")
    return render_template("producao_c.html", dados=dados_pesquisa)


@app.route("/processo_producao_c", methods=["POST"])
@login_required
def processo_producao_c():
    id_input = request.form["id_input"]

    return redirect(f"/producao_c_1/{id_input}")


@app.route("/producao_c_1/<id_input>", methods=["GET", "POST"])
@login_required
def producao_c_1(id_input):
    item = bpd.retornar_item(id_input, "c")
    print(id_input)
    return render_template("producao_c_1.html", item=item, id_item=id_input)


@app.route("/producao_atual_c/<id_item>", methods=["GET", "POST"])
@login_required
def producao_atual_c(id_item):
    quantidade = request.form.get("quant_input")
    print(quantidade)
    bpd.change_quant(id_item, quantidade, "c", user)
    return redirect("/producao_c")


@app.route("/relatorio_prod_a")
@login_required
def relatorio_a():
    dados = bpd.preencher_dados("a")
    return render_template("relatorio_a.html", dados=dados)


@app.route("/relatorio_prod_b")
@login_required
def relatorio_b():
    dados = bpd.preencher_dados("b")
    return render_template("relatorio_b.html", dados=dados)


@app.route("/relatorio_prod_c")
@login_required
def relatorio_c():
    dados = bpd.preencher_dados("c")
    return render_template("relatorio_c.html", dados=dados)


if __name__ == '__main__':
    app.run(debug=True)
