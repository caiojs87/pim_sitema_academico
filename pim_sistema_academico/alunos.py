# alunos.py
import json
import os

# Caminho do arquivo onde os dados serão salvos
CAMINHO_ARQUIVO = "dados/alunos.json"

# Lista de alunos (carregados do arquivo se existir)
alunos = []

def carregar_alunos():
    global alunos
    if os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            alunos = json.load(arquivo)
    else:
        alunos = []

def salvar_alunos():
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, indent=4, ensure_ascii=False)

def cadastrar_aluno():
    carregar_alunos()
    nome = input("Nome do aluno: ")
    matricula = input("Matrícula: ")
    
    aluno = {
        "nome": nome,
        "matricula": matricula
    }
    
    alunos.append(aluno)
    salvar_alunos()
    print(f"\n✅ Aluno {nome} cadastrado e salvo com sucesso!")

def listar_alunos():
    carregar_alunos()
    if not alunos:
        print("\n⚠️ Nenhum aluno cadastrado.")
    else:
        print("\n--- LISTA DE ALUNOS (SALVOS) ---")
        for a in alunos:
            print(f"📌 Nome: {a['nome']} | Matrícula: {a['matricula']}")