from flask import Flask, render_template, request, redirect, session, url_for
import json, os

# ------------------------------------------------------------
# ⚙️ CONFIGURAÇÃO DO FLASK
# ------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "unip123"
app.config["SESSION_PERMANENT"] = False

# Caminhos dos arquivos
ARQ_ALUNOS = "dados/alunos.json"
ARQ_TURMAS = "dados/turmas.json"
ARQ_USUARIOS = "dados/usuarios.json"

# ------------------------------------------------------------
# 🔧 FUNÇÕES AUXILIARES
# ------------------------------------------------------------
def carregar_json(caminho):
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def salvar_json(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def garantir_arquivos():
    """Garante que os arquivos principais existam"""
    if not os.path.exists(ARQ_USUARIOS):
        salvar_json(ARQ_USUARIOS, [{"usuario": "admin", "senha": "1234", "tipo": "admin"}])
    if not os.path.exists(ARQ_ALUNOS):
        salvar_json(ARQ_ALUNOS, [])
    if not os.path.exists(ARQ_TURMAS):
        salvar_json(ARQ_TURMAS, [])

# ------------------------------------------------------------
# 🔐 LOGIN / LOGOUT
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    usuarios = carregar_json(ARQ_USUARIOS)

    if request.method == "POST":
        usuario = request.form["usuario"].strip().lower()
        senha = request.form["senha"].strip()

        user = next((u for u in usuarios if u["usuario"] == usuario and u["senha"] == senha), None)
        if user:
            session["usuario"] = usuario
            session["tipo"] = user["tipo"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", erro="Usuário ou senha inválidos!")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ------------------------------------------------------------
# 🚨 Protege páginas com login obrigatório
# ------------------------------------------------------------
@app.before_request
def verificar_login():
    rotas_livres = ["login", "static"]
    endpoint = request.endpoint or ""
    if not session.get("usuario") and endpoint.split(".")[-1] not in rotas_livres:
        return redirect(url_for("login"))

# ------------------------------------------------------------
# 🏠 PÁGINA INICIAL
# ------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", usuario=session.get("usuario"), tipo=session.get("tipo"))

# ------------------------------------------------------------
# 👨‍🏫 ADMIN — GERENCIAR ALUNOS
# ------------------------------------------------------------
@app.route("/alunos", methods=["GET", "POST"])
def pagina_alunos():
    if session.get("tipo") != "admin":
        return redirect(url_for("index"))

    alunos = carregar_json(ARQ_ALUNOS)
    usuarios = carregar_json(ARQ_USUARIOS)

    if request.method == "POST":
        acao = request.form.get("acao")

        # ➕ Cadastrar novo aluno
        if acao == "adicionar":
            nome = request.form.get("nome").strip()
            matricula = request.form.get("matricula").strip()

            if not nome or not matricula:
                return render_template("alunos.html", alunos=alunos, erro="Preencha todos os campos.")

            if any(a["matricula"] == matricula for a in alunos):
                return render_template("alunos.html", alunos=alunos, erro="Matrícula já existente.")

            alunos.append({"nome": nome, "matricula": matricula})

            usuario_novo = nome.lower().replace(" ", "")
            if not any(u["usuario"] == usuario_novo for u in usuarios):
                usuarios.append({
                    "usuario": usuario_novo,
                    "senha": matricula,
                    "tipo": "aluno"
                })

            salvar_json(ARQ_ALUNOS, alunos)
            salvar_json(ARQ_USUARIOS, usuarios)
            return redirect(url_for("pagina_alunos"))

        # ❌ Excluir aluno
        elif acao == "excluir":
            matricula = request.form["matricula"]
            alunos = [a for a in alunos if a["matricula"] != matricula]
            usuarios = [u for u in usuarios if not (u["senha"] == matricula and u["tipo"] == "aluno")]

            salvar_json(ARQ_ALUNOS, alunos)
            salvar_json(ARQ_USUARIOS, usuarios)
            return redirect(url_for("pagina_alunos"))

    return render_template("alunos.html", alunos=alunos, usuario=session["usuario"], tipo=session["tipo"])

# ------------------------------------------------------------
# 🏫 TURMAS
# ------------------------------------------------------------
@app.route("/turmas", methods=["GET", "POST"])
def pagina_turmas():
    turmas = carregar_json(ARQ_TURMAS)
    alunos = carregar_json(ARQ_ALUNOS)

    # 👩‍🎓 Aluno
    if session.get("tipo") == "aluno":
        usuario = session["usuario"].lower()
        turmas_aluno = []

        for turma in turmas:
            for a in turma.get("alunos", []):
                if a["nome"].lower().replace(" ", "") == usuario:
                    turmas_aluno.append(a | {"turma": turma["nome"], "codigo": turma["codigo"]})

        return render_template("turmas_aluno.html",
                               turmas=turmas_aluno,
                               usuario=session["usuario"],
                               tipo=session["tipo"])

    # 👨‍💼 Admin
    if session.get("tipo") == "admin":
        if request.method == "POST":
            acao = request.form.get("acao", "").strip()

            # ➕ Criar turma
            if acao == "criar_turma":
                nome = request.form["nome_turma"]
                codigo = request.form["codigo_turma"]
                turmas.append({"nome": nome, "codigo": codigo, "alunos": []})

            # ❌ Excluir turma
            elif acao == "excluir_turma":
                codigo = request.form["codigo_turma"]
                turmas = [t for t in turmas if t["codigo"] != codigo]

            # ➕ Adicionar aluno
            elif acao == "adicionar_aluno":
                codigo = request.form["codigo_turma"]
                matricula = request.form["matricula"]
                aluno = next((a for a in alunos if a["matricula"] == matricula), None)
                if aluno:
                    for turma in turmas:
                        if turma["codigo"] == codigo:
                            if not any(x["matricula"] == matricula for x in turma["alunos"]):
                                turma["alunos"].append({
                                    "nome": aluno["nome"],
                                    "matricula": aluno["matricula"],
                                    "np1": None,
                                    "np2": None,
                                    "pim": None,
                                    "media": None,
                                    "faltas": 0
                                })

            # ❌ Remover aluno — CORRIGIDO
            elif acao == "remover_aluno":
                codigo = request.form.get("codigo_turma")
                matricula = request.form.get("matricula")
                for turma in turmas:
                    if turma["codigo"] == codigo:
                        antes = len(turma["alunos"])
                        turma["alunos"] = [a for a in turma["alunos"] if a["matricula"] != matricula]
                        depois = len(turma["alunos"])
                        print(f"Removendo aluno {matricula} da turma {codigo}: {antes}->{depois}")
                        break

            # 🧮 Atualizar notas e faltas
            elif acao == "atualizar_dados":
                codigo = request.form["codigo_turma"]
                matricula = request.form["matricula"]
                np1 = request.form.get("np1")
                np2 = request.form.get("np2")
                pim = request.form.get("pim")
                faltas = request.form.get("faltas")

                for turma in turmas:
                    if turma["codigo"] == codigo:
                        for aluno in turma["alunos"]:
                            if aluno["matricula"] == matricula:
                                aluno["np1"] = float(np1) if np1 else None
                                aluno["np2"] = float(np2) if np2 else None
                                aluno["pim"] = float(pim) if pim else None
                                aluno["faltas"] = int(faltas) if faltas else 0
                                if aluno["np1"] is not None and aluno["np2"] is not None and aluno["pim"] is not None:
                                    aluno["media"] = round(((aluno["np1"] * 4) + (aluno["pim"] * 2) + (aluno["np2"] * 4)) / 10, 2)
                                break

            # 💾 Sempre salva após qualquer ação
            salvar_json(ARQ_TURMAS, turmas)
            return redirect(url_for("pagina_turmas"))

        return render_template("turmas_admin.html",
                               turmas=turmas,
                               alunos=alunos,
                               usuario=session["usuario"],
                               tipo=session["tipo"])
# ------------------------------------------------------------
# 📊 RELATÓRIOS
# ------------------------------------------------------------
@app.route("/relatorios")
def pagina_relatorios():
    if session.get("tipo") != "admin":
        return redirect(url_for("index"))

    alunos = carregar_json(ARQ_ALUNOS)
    turmas = carregar_json(ARQ_TURMAS)

    total_alunos = len(alunos)
    total_turmas = len(turmas)
    media_alunos_por_turma = round(total_alunos / total_turmas, 2) if total_turmas else 0

    notas, faltas = [], []
    resumo_turmas = []

    for turma in turmas:
        medias = [a.get("media") for a in turma.get("alunos", []) if a.get("media") is not None]
        faltas_turma = [a.get("faltas", 0) for a in turma.get("alunos", [])]
        media_notas = round(sum(medias) / len(medias), 2) if medias else 0
        media_faltas = round(sum(faltas_turma) / len(faltas_turma), 2) if faltas_turma else 0
        resumo_turmas.append({
            "nome": turma["nome"],
            "codigo": turma["codigo"],
            "qtd_alunos": len(turma.get("alunos", [])),
            "media_notas": media_notas,
            "media_faltas": media_faltas
        })
        notas.extend(medias)
        faltas.extend(faltas_turma)

    media_geral_notas = round(sum(notas) / len(notas), 2) if notas else 0
    media_geral_faltas = round(sum(faltas) / len(faltas), 2) if faltas else 0

    return render_template("relatorio.html",
                           usuario=session["usuario"],
                           tipo=session["tipo"],
                           total_alunos=total_alunos,
                           total_turmas=total_turmas,
                           media_alunos_por_turma=media_alunos_por_turma,
                           media_geral_notas=media_geral_notas,
                           media_geral_faltas=media_geral_faltas,
                           resumo_turmas=resumo_turmas)

# ------------------------------------------------------------
# 🚀 EXECUÇÃO
# ------------------------------------------------------------
if __name__ == "__main__":
    garantir_arquivos()
    app.run(debug=True)
