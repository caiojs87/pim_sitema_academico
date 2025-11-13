# integracao_cython.py
# Importa a função 'calcular_media' do módulo 'media_cython'
# O comentário '# type: ignore' serve para o editor ignorar avisos de tipo,
# caso o arquivo Cython (.pyd/.so) não seja detectado corretamente pelo analisador.
from media_cython import calcular_media  # type: ignore

# Define uma função responsável por interagir com o usuário e calcular a média
def calcular_media_aluno():
    print("\n=== Cálculo de Média (via Cython) ===")  # Cabeçalho informativo

    try:
        # Solicita as três notas do aluno e converte para float
        n1 = float(input("Nota 1: "))
        n2 = float(input("Nota 2: "))
        n3 = float(input("Nota 3: "))

        # Chama a função 'calcular_media' (implementada em Cython)
        # Essa função faz o cálculo da média das três notas
        media = calcular_media(n1, n2, n3)

        # Exibe a média formatada com duas casas decimais
        print(f"\n📘 Média calculada: {media:.2f}")

        # Verifica se o aluno foi aprovado ou reprovado
        if media >= 6:
            print("✅ Aluno aprovado!")
        else:
            print("❌ Aluno reprovado.")
    
    # Caso o usuário digite algo que não seja número, cai no except
    except ValueError:
        print("❌ Erro: digite apenas números válidos.")
