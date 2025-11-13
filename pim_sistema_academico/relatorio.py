import alunos
import turmas
import json
import os

# Caminho para onde serão salvos os relatórios
CAMINHO_RELATORIOS = "dados/relatorios"
os.makedirs(CAMINHO_RELATORIOS, exist_ok=True)

def listar_alunos_por_turma():
    """Exibe e gera um arquivo com a lista de alunos de cada turma."""
    turmas.carregar_turmas()
    if not turmas.turmas:
        print("\n⚠️ Nenhuma turma cadastrada.")
        return

    for t in turmas.turmas:
        print(f"\n📘 Turma: {t['nome']} ({t['codigo']})")
        if not t["alunos"]:
            print("   - Nenhum aluno associado.")
        else:
            for a in t["alunos"]:
                print(f"   - {a['nome']} (Matrícula: {a['matricula']})")

    # Salva relatório em arquivo
    caminho = os.path.join(CAMINHO_RELATORIOS, "alunos_por_turma.txt")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        for t in turmas.turmas:
            arquivo.write(f"Turma: {t['nome']} ({t['codigo']})\n")
            if not t["alunos"]:
                arquivo.write("   - Nenhum aluno associado.\n")
            else:
                for a in t["alunos"]:
                    arquivo.write(f"   - {a['nome']} (Matrícula: {a['matricula']})\n")
            arquivo.write("\n")
    print(f"\n✅ Relatório salvo em: {caminho}")


def turmas_do_aluno():
    """Mostra em quais turmas um aluno está matriculado."""
    alunos.carregar_alunos()
    turmas.carregar_turmas()

    matricula = input("Informe a matrícula do aluno: ")
    aluno = next((a for a in alunos.alunos if a["matricula"] == matricula), None)

    if not aluno:
        print("\n❌ Aluno não encontrado!")
        return

    turmas_encontradas = [t for t in turmas.turmas if any(a["matricula"] == matricula for a in t["alunos"])]

    print(f"\n👤 Aluno: {aluno['nome']} ({aluno['matricula']})")
    if not turmas_encontradas:
        print("   - Este aluno ainda não está em nenhuma turma.")
    else:
        print("   - Turmas:")
        for t in turmas_encontradas:
            print(f"     📘 {t['nome']} ({t['codigo']})")


def gerar_resumo_geral():
    """Cria um relatório geral (quantidade de turmas, alunos e vínculos)."""
    alunos.carregar_alunos()
    turmas.carregar_turmas()

    total_alunos = len(alunos.alunos)
    total_turmas = len(turmas.turmas)
    total_vinculos = sum(len(t["alunos"]) for t in turmas.turmas)

    resumo = {
        "total_alunos": total_alunos,
        "total_turmas": total_turmas,
        "total_vinculos": total_vinculos
    }

    print("\n📊 RESUMO GERAL DO SISTEMA")
    print(f"👥 Alunos cadastrados: {total_alunos}")
    print(f"🏫 Turmas criadas: {total_turmas}")
    print(f"🔗 Associações aluno-turma: {total_vinculos}")

    caminho = os.path.join(CAMINHO_RELATORIOS, "resumo_geral.json")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(resumo, arquivo, indent=4, ensure_ascii=False)
    print(f"\n✅ Resumo salvo em: {caminho}")