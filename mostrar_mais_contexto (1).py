# -*- coding: utf-8 -*-
"""
Mostra mais contexto para implementar a lista de combinacoes premiadas no PDF.

Rode em A:\\PROJETO\\vcvl-fase1\\  (mostra ConferenciaLotofacil.tsx)
Rode em A:\\PROJETO\\vcvl-pdf-server-git\\  (mostra app.py)
"""
import os

def mostrar(caminho, inicio, fim, titulo=""):
    if not os.path.exists(caminho):
        print(f"[NAO ENCONTRADO NESTA PASTA] {caminho}")
        return
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()
    print("=" * 70)
    print(f"{titulo}  Arquivo: {caminho}  (linhas {inicio}-{fim})")
    print("=" * 70)
    for i in range(max(0, inicio - 1), min(len(linhas), fim)):
        print(f"{i+1:5d}: {linhas[i]}", end="")
    print("\n")

def achar_e_mostrar(caminho, termo, contexto_antes=5, contexto_depois=40, max_ocorrencias=3):
    if not os.path.exists(caminho):
        print(f"[NAO ENCONTRADO NESTA PASTA] {caminho}")
        return
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()
    achou = 0
    for i, linha in enumerate(linhas):
        if termo in linha:
            achou += 1
            print("=" * 70)
            print(f"Ocorrencia de '{termo}' em {caminho}, linha {i+1}")
            print("=" * 70)
            inicio = max(0, i - contexto_antes)
            fim = min(len(linhas), i + contexto_depois)
            for j in range(inicio, fim):
                marcador = ">>" if j == i else "  "
                print(f"{marcador} {j+1:5d}: {linhas[j]}", end="")
            print("\n")
            if achou >= max_ocorrencias:
                break

# --- Lado Next.js ---
CAMINHO_TSX = os.path.join("src", "app", "dashboard", "lotofacil", "ConferenciaLotofacil.tsx")
mostrar(CAMINHO_TSX, 466, 520, "[premiadas - continuacao do map]")
achar_e_mostrar(CAMINHO_TSX, "function conferir", contexto_antes=2, contexto_depois=60)
achar_e_mostrar(CAMINHO_TSX, "function gerarPDF", contexto_antes=2, contexto_depois=40)
achar_e_mostrar(CAMINHO_TSX, "carregarArquivo", contexto_antes=2, contexto_depois=35, max_ocorrencias=1)

# --- Lado Python ---
achar_e_mostrar("app.py", "def gerar_conferencia", contexto_antes=2, contexto_depois=30)
achar_e_mostrar("app.py", "premiadas", contexto_antes=2, contexto_depois=10, max_ocorrencias=5)
