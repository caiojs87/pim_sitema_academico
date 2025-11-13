# media_cython.pyx
# Módulo híbrido (Python + C otimizado pelo Cython)
# Faz o cálculo da média de três notas

def calcular_media(n1: float, n2: float, n3: float) -> float:
    """
    Calcula a média aritmética de três notas.
    """
    return (n1 + n2 + n3) / 3