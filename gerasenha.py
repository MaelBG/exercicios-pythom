import random
import string
import re

# -----------------------------
# Gerador de Senhas
# -----------------------------
def gerar_senha(tamanho=12, usar_maiusculas=True, usar_minusculas=True,
                usar_numeros=True, usar_simbolos=True, evitar_ambiguous=True):
    if not any([usar_maiusculas, usar_minusculas, usar_numeros, usar_simbolos]):
        raise ValueError("Selecione pelo menos um tipo de caractere.")

    # Conjunto de caracteres
    conjuntos = []
    if usar_maiusculas:
        conjuntos.append(string.ascii_uppercase)
    if usar_minusculas:
        conjuntos.append(string.ascii_lowercase)
    if usar_numeros:
        conjuntos.append(string.digits)
    if usar_simbolos:
        # símbolos "seguros" para não confundir com shell/URL
        simbolos = "!@#$%^&*()-_=+[]{};:,.?"
        conjuntos.append(simbolos)

    # Evitar caracteres ambíguos (ex: 0/O, 1/l/I) se solicitado
    if evitar_ambiguous:
        conjuntos = [remover_ambiguous(c) for c in conjuntos]

    # Garante ao menos um caractere de cada grupo selecionado
    senha = [random.choice(c) for c in conjuntos]

    # Preenche o restante com a união de todos os conjuntos
    universo = "".join(conjuntos)
    senha += [random.choice(universo) for _ in range(max(0, tamanho - len(senha)))]

    # Embaralha para não deixar previsível
    random.shuffle(senha)
    return "".join(senha[:tamanho])

def remover_ambiguous(chars):
    ambiguous = set("O0oI1l|`'\"{}[>;:,.")
    return "".join(ch for ch in chars if ch not in ambiguous)

# -----------------------------
# Analisador de Força
# -----------------------------
def analisar_forca(senha):
    pontuacao = 0
    motivos = []

    comprimento = len(senha)
    if comprimento >= 16:
        pontuacao += 3; motivos.append("Comprimento ≥ 16")
    elif comprimento >= 12:
        pontuacao += 2; motivos.append("Comprimento ≥ 12")
    elif comprimento >= 8:
        pontuacao += 1; motivos.append("Comprimento ≥ 8")
    else:
        motivos.append("Comprimento curto (< 8)")

    # Diversidade de caracteres
    categorias = {
        "maiúsculas": any(c.isupper() for c in senha),
        "minúsculas": any(c.islower() for c in senha),
        "números": any(c.isdigit() for c in senha),
        "símbolos": any(c in "!@#$%^&*()-_=+[]{};:,.?" for c in senha),
    }
    diversidade = sum(categorias.values())
    pontuacao += max(0, diversidade - 1)  # 0..3 pontos
    if diversidade == 4:
        motivos.append("Usa maiúsculas, minúsculas, números e símbolos")
    elif diversidade >= 2:
        motivos.append("Boa diversidade de caracteres")
    else:
        motivos.append("Pouca diversidade de caracteres")

    # Penalidades por padrões comuns
    padroes_fracos = [
        r"(.)\1{2,}",          # caracteres repetidos 3+
        r"1234|2345|3456|4567|5678|6789|7890",
        r"abcd|bcde|cdef|qwerty|password|senha|admin",
    ]
    penalidades = 0
    for p in padroes_fracos:
        if re.search(p, senha.lower()):
            penalidades += 1
    pontuacao -= penalidades
    if penalidades:
        motivos.append("Contém padrões previsíveis")

    # Limita faixa e define classificação
    pontuacao = max(0, min(7, pontuacao))
    classificacao = [
        "Muito fraca", "Fraca", "Razoável", "Boa",
        "Forte", "Muito forte", "Excelente", "Impenetrável (prática)"
    ][pontuacao]

    # Recomendações
    recomendacoes = []
    if comprimento < 12:
        recomendacoes.append("Use pelo menos 12 caracteres.")
    if diversidade < 3:
        recomendacoes.append("Misture maiúsculas, minúsculas, números e símbolos.")
    if penalidades:
        recomendacoes.append("Evite sequências (1234, abcd) e repetições (aaa).")

    return {
        "pontuacao": pontuacao,
        "classificacao": classificacao,
        "motivos": motivos,
        "recomendacoes": recomendacoes,
        "detalhe_categorias": categorias,
    }

# -----------------------------
# Interface simples (CLI)
# -----------------------------
def menu():
    print("=== Gerador de Senhas + Analisador de Força ===")
    try:
        tamanho = int(input("Tamanho da senha (recomendado 12-20) [padrão 14]: ") or 14)
    except ValueError:
        tamanho = 14

    usar_maiusculas = ler_bool("Incluir MAIÚSCULAS? (S/n): ", True)
    usar_minusculas = ler_bool("Incluir minúsculas? (S/n): ", True)
    usar_numeros = ler_bool("Incluir números? (S/n): ", True)
    usar_simbolos = ler_bool("Incluir símbolos? (S/n): ", True)
    evitar_ambiguous = ler_bool("Evitar caracteres ambíguos (0/O, 1/l)? (S/n): ", True)

    senha = gerar_senha(
        tamanho,
        usar_maiusculas,
        usar_minusculas,
        usar_numeros,
        usar_simbolos,
        evitar_ambiguous
    )
    print("\nSenha gerada:", senha)

    analise = analisar_forca(senha)
    print(f"\nForça: {analise['classificacao']} (pontuação: {analise['pontuacao']}/7)")
    print("• Motivos:", "; ".join(analise["motivos"]))
    if analise["recomendacoes"]:
        print("• Recomendações:", " | ".join(analise["recomendacoes"]))

def ler_bool(prompt, padrao=True):
    resp = input(prompt).strip().lower()
    if resp == "":
        return padrao
    return resp in ("s", "sim", "y", "yes")

if __name__ == "__main__":
    menu()