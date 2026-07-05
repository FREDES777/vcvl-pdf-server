# -*- coding: utf-8 -*-
"""
Adiciona as dezenas sorteadas tambem na faixa "Combinacoes Premiadas --
Concurso N. X", para ficar visivel junto com a lista de combinacoes.

Rode dentro de A:\\PROJETO\\vcvl-pdf-server-git\\
"""
import os
import shutil

CAMINHO = "app.py"

if not os.path.exists(CAMINHO):
    print(f"[ERRO] Nao encontrado: {CAMINHO}. Rode dentro de vcvl-pdf-server-git\\")
    raise SystemExit(1)

conteudo = open(CAMINHO, "r", encoding="utf-8").read()

ANTIGO = """        c.drawString(MARGIN + 3*mm, y - 4*mm, 'Combinacoes Premiadas -- Concurso N. ' + str(h.get('num_concurso', '')))
        y -= 6*mm"""

NOVO = """        c.drawString(MARGIN + 3*mm, y - 4*mm, 'Combinacoes Premiadas -- Concurso N. ' + str(h.get('num_concurso', '')) + '  ·  Sorteio: ' + sorteados_str)
        y -= 6*mm"""

if ANTIGO not in conteudo:
    print("[ERRO] Trecho nao encontrado. Nenhuma alteracao foi feita.")
else:
    shutil.copy(CAMINHO, CAMINHO + ".bak5")
    conteudo = conteudo.replace(ANTIGO, NOVO, 1)
    with open(CAMINHO, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] {CAMINHO} atualizado (backup em {CAMINHO}.bak5)")
