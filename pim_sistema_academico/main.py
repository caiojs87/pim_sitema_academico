from turmas import criar_turma, listar_turmas, adicionar_aluno_turma
from alunos import cadastrar_aluno, listar_alunos
from relatorio import listar_alunos_por_turma, turmas_do_aluno, gerar_resumo_geral
from integracao_cython import calcular_media_aluno



def menu():
    while True:
        print("\n=== SISTEMA ACADÊMICO ===")
        print("1 - Cadastrar Aluno")
        print("2 - Listar Alunos")
        print("3 - Criar Turma")
        print("4 - Listar Turmas")
        print("5 - Adicionar Aluno à Turma")
        print("6 - Listar Alunos por Turma")
        print("7 - Mostrar Turmas de um Aluno")
        print("8 - Gerar Resumo Geral")
        print("9 - Calcular Média (usando módulo Cython)")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cadastrar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            criar_turma()
        elif opcao == "4":
            listar_turmas()
        elif opcao == "5":
            adicionar_aluno_turma()
        elif opcao == "6":
            listar_alunos_por_turma()
        elif opcao == "7":
            turmas_do_aluno()
        elif opcao == "8":
            gerar_resumo_geral()
        elif opcao == "9":
             calcular_media_aluno()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
    
    
    
   
# python main_web.py