# -*- coding: utf-8 -*-
"""
Adiciona a linha "Dezenas sorteadas: ..." no PDF de historico
(SCRIPTS["historico"] em app.py), para cada concurso, antes das
faixas de premiacao.

Rode dentro de A:\\PROJETO\\vcvl-pdf-server-git\\
"""
import os
import shutil

CAMINHO = "app.py"

if not os.path.exists(CAMINHO):
    print(f"[ERRO] Nao encontrado: {CAMINHO}. Rode dentro de vcvl-pdf-server-git\\")
    raise SystemExit(1)

conteudo = open(CAMINHO, "r", encoding="utf-8").read()

ANTIGO = """    dia = parse_dia(h.get('data_concurso', ''))
    data_str = dia + ' ' + h.get('data_concurso', '')
    num_conc = 'N. ' + str(h.get('num_concurso', ''))
    bg = COR_BRANCO if cor_alterna else COR_CINZA
    cor_alterna = not cor_alterna

    n_linhas = max(len(faixas_h), 1)
    linha_h  = 6*mm
    sub_h    = 6*mm
    bloco_h  = n_linhas * linha_h + sub_h + 1*mm

    # Verificar se cabe na página
    if y - bloco_h < 15*mm:
        rodape(pag_atual[0], '?')
        pag_atual[0] += 1
        y = nova_pagina()
        y = desenhar_header_tabela(y)
        cor_alterna = True

    if not faixas_h:"""

NOVO = """    dia = parse_dia(h.get('data_concurso', ''))
    data_str = dia + ' ' + h.get('data_concurso', '')
    num_conc = 'N. ' + str(h.get('num_concurso', ''))
    bg = COR_BRANCO if cor_alterna else COR_CINZA
    cor_alterna = not cor_alterna

    sorteados_h = h.get('sorteados') or []
    sorteados_str = '  '.join(str(n).zfill(2) for n in sorteados_h)

    n_linhas = max(len(faixas_h), 1)
    linha_h  = 6*mm
    sub_h    = 6*mm
    linha_sorteados_h = 5*mm if sorteados_h else 0
    bloco_h  = n_linhas * linha_h + sub_h + linha_sorteados_h + 1*mm

    # Verificar se cabe na página
    if y - bloco_h < 15*mm:
        rodape(pag_atual[0], '?')
        pag_atual[0] += 1
        y = nova_pagina()
        y = desenhar_header_tabela(y)
        cor_alterna = True

    if sorteados_h:
        c.setFont(_font, 6.5)
        c.setFillColor(COR_SUBTEXTO)
        c.drawString(MARGIN + 1.5*mm, y - 3.5*mm, 'Dezenas sorteadas: ' + sorteados_str)
        y -= linha_sorteados_h

    if not faixas_h:"""

if ANTIGO not in conteudo:
    print("[ERRO] Trecho nao encontrado. Nenhuma alteracao foi feita.")
else:
    shutil.copy(CAMINHO, CAMINHO + ".bak4")
    conteudo = conteudo.replace(ANTIGO, NOVO, 1)
    with open(CAMINHO, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] {CAMINHO} atualizado (backup em {CAMINHO}.bak4)")
