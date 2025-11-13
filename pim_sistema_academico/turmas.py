import json
import os
import alunos  # 👈 Importa o módulo inteiro, não apenas a lista

CAMINHO_TURMAS = "dados/turmas.json"
turmas = []

def carregar_turmas():
    global turmas
    if os.path.exists(CAMINHO_TURMAS):
        try:
            with open(CAMINHO_TURMAS, "r", encoding="utf-8") as arquivo:
                turmas = json.load(arquivo)
        except json.JSONDecodeError:
            turmas = []
            salvar_turmas()
    else:
        turmas = []
        salvar_turmas()

def salvar_turmas():
    with open(CAMINHO_TURMAS, "w", encoding="utf-8") as arquivo:
        json.dump(turmas, arquivo, indent=4, ensure_ascii=False)

def criar_turma():
    carregar_turmas()
    nome = input("Nome da turma: ")
    codigo = input("Código da turma (ex: ADS01): ")
    
    turma = {
        "nome": nome,
        "codigo": codigo,
        "alunos": []
    }
    
    turmas.append(turma)
    salvar_turmas()
    print(f"\n✅ Turma '{nome}' criada com sucesso!")

def listar_turmas():
    carregar_turmas()
    if not turmas:
        print("\n⚠️ Nenhuma turma cadastrada.")
    else:
        print("\n--- LISTA DE TURMAS ---")
        for t in turmas:
            print(f"🏫 Turma: {t['nome']} | Código: {t['codigo']} | Alunos: {len(t['alunos'])}")

def adicionar_aluno_turma():
    carregar_turmas()
    alunos.carregar_alunos()  # 👈 garante que o JSON está carregado

    codigo = input("Código da turma: ")
    matricula = input("Matrícula do aluno: ")

    turma_encontrada = next((t for t in turmas if t["codigo"] == codigo), None)
    if not turma_encontrada:
        print("❌ Turma não encontrada!")
        return

    aluno_encontrado = next((a for a in alunos.alunos if a["matricula"] == matricula), None)
    if not aluno_encontrado:
        print("❌ Aluno não encontrado!")
        return

    # Evita duplicar aluno
    if any(a["matricula"] == matricula for a in turma_encontrada["alunos"]):
        print("⚠️ Este aluno já está nessa turma.")
        return

    turma_encontrada["alunos"].append(aluno_encontrado)
    salvar_turmas()
    print(f"✅ Aluno {aluno_encontrado['nome']} adicionado à turma {turma_encontrada['nome']}")
