# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_file
import tempfile, os, subprocess, sys, json

app = Flask(__name__)

# ── Scripts Python dos PDFs ───────────────────────────────────────────────────

SCRIPTS = {}

SCRIPTS["lotofacil"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes  = data['combinacoes']
offsetX      = data.get('offsetX', 0)
offsetY      = data.get('offsetY', 0)
espLinha     = data.get('espLinha', 0)
colOffset    = data.get('colOffset', [0,0,0,0,0])
linhaOffset  = data.get('linhaOffset',  [0,0,0,0,0])
linhaOffset2 = data.get('linhaOffset2', linhaOffset)
linhaOffset3 = data.get('linhaOffset3', linhaOffset)
gapJogo12    = data.get('gapJogo12', 0)
gapJogo23    = data.get('gapJogo23', 0)
elW          = data.get('elW', 11)
elH          = data.get('elH', 8)
resumo       = data.get('resumo', '')
valor_comb   = data.get('valorCombinacaoUnit', 0)
tei_mult     = data.get('teimosinhaMult', 1)
total_pag    = data.get('totalPaginas', 1)
dez_por_aposta = data.get('dezPorAposta', 15)
mdz_pos_x      = data.get('mdzPosX', [0, 42, 86, 132, 178, 222])
mdz_offset_x   = data.get('mdzOffsetX', 0)
mdz_offset_y   = data.get('mdzOffsetY', 0)
teimosinha   = data.get('teimosinha', 0)
tei_pos_x    = data.get('teiPosX', [0, 88, 178, 268, 357])
spr_offset_x = data.get('sprOffsetX', 0)
spr_offset_y = data.get('sprOffsetY', 0)

PW = 82.0 * mm
PH = 186.0 * mm
SCALE = mm / (578 / 82.0)

BOLHAS = {
  1:(322,243),2:(322,273),3:(322,300),4:(322,326),5:(322,353),
  6:(283,243),7:(283,273),8:(283,300),9:(283,326),10:(283,353),
  11:(245,243),12:(245,273),13:(245,300),14:(245,326),15:(245,353),
  16:(210,243),17:(210,273),18:(210,300),19:(210,326),20:(210,353),
  21:(103,243),22:(103,273),23:(103,300),24:(103,326),25:(103,353),
}
DEZ_COL = {1:0,2:0,3:0,4:0,5:0,6:1,7:1,8:1,9:1,10:1,
           11:2,12:2,13:2,14:2,15:2,16:3,17:3,18:3,19:3,20:3,
           21:4,22:4,23:4,24:4,25:4}
DEZ_LIN = {1:0,6:0,11:0,16:0,21:0,2:1,7:1,12:1,17:1,22:1,
           3:2,8:2,13:2,18:2,23:2,4:3,9:3,14:3,19:3,24:3,
           5:4,10:4,15:4,20:4,25:4}
JOGO2 = 179; JOGO3 = 328

def jogo_oy(j):
    if j==1: return 0
    if j==2: return JOGO2 + gapJogo12
    return JOGO3 + gapJogo23

COMBOS_POR_PAG = 3
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]

    if resumo:
        c.setFont(_font_name, 10)
        c.setFillColorRGB(0,0,0)
        pg_num = pg//COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X','.')
        base_idx = pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        if len(nums_pag) == 1:
            comb_txt = 'Combinacao: ' + nums_pag[0]
        else:
            comb_txt = 'Combinacoes: ' + ', '.join(nums_pag[:-1]) + ' e ' + nums_pag[-1]
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.1 * mm
        linha_h  = 3.5 * mm
        y_inicio = PH - 19.4*mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        txt_bil = 'Bilhete ' + str(pg_num) + ' de ' + str(total_pag)
        c.drawString(margem_x, y_inicio - len(linhas_resumo) * linha_h, txt_bil)

    c.setFillColorRGB(0,0,0)
    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy_jogo = jogo_oy(jogo)
        for dez in combo:
            bx, by = BOLHAS[dez]
            col_idx = DEZ_COL[dez]
            lin_idx = DEZ_LIN[dez]
            cx_px = bx + offsetX + colOffset[col_idx]
            lo = linhaOffset if jogo == 1 else (linhaOffset2 if jogo == 2 else linhaOffset3)
            cy_px = by + oy_jogo + offsetY + lin_idx * espLinha + lo[lin_idx]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW/2) * SCALE
            rh = (elH/2) * SCALE
            c.ellipse(cx_pt-rw, cy_pt-rh, cx_pt+rw, cy_pt+rh, fill=1, stroke=0)

    rw = (elW/2) * SCALE
    rh = (elH/2) * SCALE
    ultima_linha_py = BOLHAS[25][1]
    jogo3_oy = jogo_oy(3)  # marcador fixo no bloco 3, independente de quantos jogos

    mdz_idx = dez_por_aposta - 15
    if 0 <= mdz_idx < len(mdz_pos_x):
        mdz_base_x = 103 + offsetX + colOffset[4] + mdz_offset_x + mdz_pos_x[mdz_idx]
        mdz_base_y = ultima_linha_py + jogo3_oy + offsetY + 40 + mdz_offset_y
        cx_pt = mdz_base_x * SCALE
        cy_pt = PH - mdz_base_y * SCALE
        c.ellipse(cx_pt-rw, cy_pt-rh, cx_pt+rw, cy_pt+rh, fill=1, stroke=0)

    tei_opcoes = [3, 6, 12, 18, 24]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tei_base_x = 103 + offsetX + colOffset[4] + spr_offset_x + tei_pos_x[tei_idx]
        tei_base_y = ultima_linha_py + jogo3_oy + offsetY + 40 + spr_offset_y
        cx_pt = tei_base_x * SCALE
        cy_pt = PH - tei_base_y * SCALE
        c.ellipse(cx_pt-rw, cy_pt-rh, cx_pt+rw, cy_pt+rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["megasena"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes    = data['combinacoes']
offsetX        = data.get('offsetX', 0) - 4  # DELTA_X calibrado
offsetY        = data.get('offsetY', 0)
espLinha       = data.get('espLinha', 0)
colOffset      = data.get('colOffset', [0]*10)
linhaOffset    = data.get('linhaOffset',  [0]*6)
linhaOffset2   = data.get('linhaOffset2', linhaOffset)
linhaOffset3   = data.get('linhaOffset3', linhaOffset)
gapJogo12      = data.get('gapJogo12', 0) - 22  # DELTA_GAP12 calibrado
gapJogo23      = data.get('gapJogo23', 0) + 39  # DELTA_GAP23 calibrado
elW            = data.get('elW', 11)
elH            = data.get('elH', 8)
resumo         = data.get('resumo', '')
header_color_hex = data.get('headerColor', '#6a0dad')
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
hdr_r, hdr_g, hdr_b = hex_to_rgb(header_color_hex)
valor_comb     = data.get('valorCombinacaoUnit', 0)
tei_mult       = data.get('teimosinhaMult', 1)
total_pag      = data.get('totalPaginas', 1)
pagina_inicio  = data.get('paginaInicio', 0)
dez_por_aposta = data.get('dezPorAposta', 6)
mdz_pos_x      = data.get('mdzPosX', [0, 45, 90, 135, 180, 225, 270, 315, 360, 405])
mdz_offset_x   = data.get('mdzOffsetX', 0)
mdz_offset_y   = data.get('mdzOffsetY', 0)
teimosinha     = data.get('teimosinha', 0)
tei_pos_x      = data.get('teiPosX', [0, 90, 180])
spr_offset_x   = data.get('sprOffsetX', 0)
spr_offset_y   = data.get('sprOffsetY', 0)
col_x_base     = data.get('colXBase', [75, 125, 175, 226, 277, 327, 378, 429, 479, 530])
col1_x_base    = data.get('col1XBase', col_x_base)
col2_x_base    = data.get('col2XBase', col_x_base)
lin_y_base     = data.get('linYBase', [295, 323, 351, 379, 407, 435])
lin1_y_base    = data.get('lin1YBase', lin_y_base)
jogo2_base     = data.get('jogo2Base', 185)
jogo3_base     = data.get('jogo3Base', 370)

PW = 82.0 * mm
PH = 186.0 * mm
SCALE = mm / (578 / 82.0)

def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

def jogo_oy(j):
    if j == 1: return 0
    if j == 2: return jogo2_base + gapJogo12
    return jogo3_base + gapJogo23

COMBOS_POR_PAG = 3
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]

    if resumo:
        c.setFont(_font_name, 10)
        c.setFillColorRGB(0, 0, 0)
        pg_num = pagina_inicio + pg // COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X', '.')
        base_idx = pagina_inicio + pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        if len(nums_pag) == 1:
            comb_txt = 'Combinacao: ' + nums_pag[0]
        else:
            comb_txt = 'Combinacoes: ' + ', '.join(nums_pag[:-1]) + ' e ' + nums_pag[-1]
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.1 * mm
        linha_h  = 3.5 * mm
        y_inicio = PH - 19.4 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        txt_bil = 'Bilhete ' + str(pg_num) + ' de ' + str(total_pag)
        c.drawString(margem_x, y_inicio - len(linhas_resumo) * linha_h, txt_bil)

    c.setFillColorRGB(0, 0, 0)

    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy   = jogo_oy(jogo)
        lo   = linhaOffset if jogo == 1 else (linhaOffset2 if jogo == 2 else linhaOffset3)
        for dez in combo:
            col   = get_col(dez)
            lin   = get_lin(dez)
            cx_px = col_x_base[col] + offsetX + colOffset[col]
            cy_px = lin_y_base[lin] + oy + offsetY + lin * espLinha + lo[lin]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW / 2) * SCALE
            rh = (elH / 2) * SCALE
            c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    rw = (elW / 2) * SCALE
    rh = (elH / 2) * SCALE
    n_jogos   = len(combos_pag)
    ultima_y  = lin_y_base[5] + jogo_oy(3) + offsetY  # marcador fixo no bloco 3, independente de quantos jogos

    mdz_idx = dez_por_aposta - 6
    if 0 <= mdz_idx < len(mdz_pos_x):
        mdz_bx = col_x_base[0] + offsetX + colOffset[0] + mdz_offset_x + mdz_pos_x[mdz_idx]
        mdz_by = ultima_y + 55 + mdz_offset_y
        cx_pt  = mdz_bx * SCALE
        cy_pt  = PH - mdz_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    tei_opcoes = [2, 4, 8]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tei_bx  = col_x_base[0] + offsetX + colOffset[0] + spr_offset_x + tei_pos_x[tei_idx]
        tei_by  = ultima_y + 213 + spr_offset_y
        cx_pt   = tei_bx * SCALE
        cy_pt   = PH - tei_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["quina"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes    = data['combinacoes']
offsetX        = data.get('offsetX', 0) - 4  # DELTA_X calibrado
offsetY        = data.get('offsetY', 0)
espLinha       = data.get('espLinha', 0)
colOffset      = data.get('colOffset', [0]*10)
linhaOffset    = data.get('linhaOffset',  [0]*8)
linhaOffset2   = data.get('linhaOffset2', linhaOffset)
linhaOffset3   = data.get('linhaOffset3', linhaOffset)
gapJogo1       = data.get('gapJogo1', 0)
gapJogo12      = data.get('gapJogo12', 0) - 22  # DELTA_GAP12 calibrado
gapJogo23      = data.get('gapJogo23', 0) + 39  # DELTA_GAP23 calibrado
elW            = data.get('elW', 11)
elH            = data.get('elH', 8)
resumo         = data.get('resumo', '')
valor_comb     = data.get('valorCombinacaoUnit', 0)
tei_mult       = data.get('teimosinhaMult', 1)
total_pag      = data.get('totalPaginas', 1)
pagina_inicio  = data.get('paginaInicio', 0)
dez_por_aposta = data.get('dezPorAposta', 5)
header_color_hex = data.get('headerColor', '#6a0dad')
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
hdr_r, hdr_g, hdr_b = hex_to_rgb(header_color_hex)
mdz_pos_x      = data.get('mdzPosX', [0, 41, 82, 123, 164, 205, 250, 296, 345, 394, 441])
mdz_offset_x   = data.get('mdzOffsetX', 0)
mdz_offset_y   = data.get('mdzOffsetY', 0)
teimosinha     = data.get('teimosinha', 0)
tei_pos_x      = data.get('teiPosX', [41, 123, 210, 296, 381])
tei_base_y     = data.get('teiBaseY', 21)
spr_offset_x   = data.get('sprOffsetX', 0)
spr_offset_y   = data.get('sprOffsetY', 0)
col_x_base     = data.get('colXBase', [99, 142, 184, 226, 269, 310, 356, 399, 438, 480])
lin_y_base     = data.get('linYBase', [228, 251, 272, 293, 316, 338, 361, 384])
jogo1_base     = data.get('jogo1Base', 25)
jogo2_base     = data.get('jogo2Base', 235)
jogo3_base     = data.get('jogo3Base', 448)

PW = 86.4 * mm
PH = 187.3 * mm
SCALE = mm / (578 / 86.4)

def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

def jogo_oy(j):
    if j == 1: return jogo1_base + gapJogo1
    if j == 2: return jogo2_base + gapJogo12
    return jogo3_base + gapJogo23

COMBOS_POR_PAG = 3
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]

    if resumo:
        c.setFont(_font_name, 8)
        c.setFillColorRGB(1, 0, 0)  # vermelho
        pg_num = pagina_inicio + pg // COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X', '.')
        base_idx = pagina_inicio + pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        if len(nums_pag) == 1:
            comb_txt = 'Combinacao: ' + nums_pag[0]
        else:
            comb_txt = 'Combinacoes: ' + ', '.join(nums_pag[:-1]) + ' e ' + nums_pag[-1]
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.1 * mm
        linha_h  = 2.8 * mm
        y_inicio = PH - 18.7 * mm  # desceu 2.8mm (1 linha) em relacao a tentativa anterior
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        txt_bil = 'Bilhete ' + str(pg_num) + ' de ' + str(total_pag)
        c.drawString(margem_x, y_inicio - len(linhas_resumo) * linha_h, txt_bil)

    c.setFillColorRGB(0, 0, 0)

    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy   = jogo_oy(jogo)
        lo   = linhaOffset if jogo == 1 else (linhaOffset2 if jogo == 2 else linhaOffset3)
        for dez in combo:
            col   = get_col(dez)
            lin   = get_lin(dez)
            cx_px = col_x_base[col] + offsetX + colOffset[col]
            cy_px = lin_y_base[lin] + oy + offsetY + lin * espLinha + lo[lin]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW / 2) * SCALE
            rh = (elH / 2) * SCALE
            c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    rw = (elW / 2) * SCALE
    rh = (elH / 2) * SCALE
    n_jogos   = len(combos_pag)
    ultima_y  = lin_y_base[7] + jogo_oy(3) + offsetY  # marcador fixo no bloco 3, independente de quantos jogos

    mdz_idx = dez_por_aposta - 5
    if 0 <= mdz_idx < len(mdz_pos_x):
        mdz_bx = col_x_base[0] + offsetX + colOffset[0] + mdz_offset_x + mdz_pos_x[mdz_idx]
        mdz_by = ultima_y + 55 + mdz_offset_y
        cx_pt  = mdz_bx * SCALE
        cy_pt  = PH - mdz_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    tei_opcoes = [3, 6, 12, 18, 24]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tei_bx  = col_x_base[0] + offsetX + colOffset[0] + spr_offset_x + tei_pos_x[tei_idx]
        tei_by  = ultima_y + 166 + tei_base_y + spr_offset_y
        cx_pt   = tei_bx * SCALE
        cy_pt   = PH - tei_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["duplasena"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes    = data['combinacoes']
offsetX        = data.get('offsetX', 0) - 4  # DELTA_X calibrado
offsetY        = data.get('offsetY', 0)
espLinha       = data.get('espLinha', 0)
colOffset      = data.get('colOffset', [0]*10)
linhaOffset    = data.get('linhaOffset',  [0]*5)
linhaOffset2   = data.get('linhaOffset2', linhaOffset)
linhaOffset3   = data.get('linhaOffset3', linhaOffset)
gapJogo12      = data.get('gapJogo12', 0) - 22  # DELTA_GAP12 calibrado
gapJogo23      = data.get('gapJogo23', 0) + 39  # DELTA_GAP23 calibrado
elW            = data.get('elW', 11)
elH            = data.get('elH', 8)
resumo         = data.get('resumo', '')
valor_comb     = data.get('valorCombinacaoUnit', 0)
tei_mult       = data.get('teimosinhaMult', 1)
total_pag      = data.get('totalPaginas', 1)
pagina_inicio  = data.get('paginaInicio', 0)
dez_por_aposta = data.get('dezPorAposta', 6)
mdz_offset_x   = data.get('mdzOffsetX', 0)
mdz_offset_y   = data.get('mdzOffsetY', 0)
mdz_l2_dy      = data.get('mdzL2DY', 22)
teimosinha     = data.get('teimosinha', 0)
spr_offset_x   = data.get('sprOffsetX', 0)
spr_offset_y   = data.get('sprOffsetY', 0)
col_x_base     = data.get('colXBase', [104, 147, 192, 238, 284, 329, 375, 420, 465, 513])
lin_y_base     = data.get('linYBase', [352, 374, 397, 419, 442])
jogo2_base     = data.get('jogo2Base', 162)
jogo3_base     = data.get('jogo3Base', 324)

# Posições X relativas para marcador qtd dezenas
MDZ_POS_X_L1 = [0, 45, 91, 137, 183, 229, 276, 322, 368, 414]  # opcoes 6-15
MDZ_POS_X_L2 = [0, 45, 91, 137, 183]                           # opcoes 16-20
MDZ_BASE_X   = 80  # X base (opcao 6)

# Posicoes X para Teimosinha [3, 6, 9, 12]
TEI_POS_X = [112, 200, 289, 378]

PW = 82.8 * mm
PH = 187.7 * mm
SCALE = mm / (578 / 82.8)

def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

def jogo_oy(j):
    if j == 1: return 0
    if j == 2: return jogo2_base + gapJogo12
    return jogo3_base + gapJogo23

COMBOS_POR_PAG = 3
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]

    if resumo:
        c.setFont('Helvetica-Bold', 9)
        c.setFillColorRGB(0.5, 0.11, 0.11)  # vinho
        pg_num = pagina_inicio + pg // COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X', '.')
        base_idx = pagina_inicio + pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        if len(nums_pag) == 1:
            comb_txt = 'Combinacao: ' + nums_pag[0]
        else:
            comb_txt = 'Combinacoes: ' + ', '.join(nums_pag[:-1]) + ' e ' + nums_pag[-1]
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.1 * mm
        linha_h  = 2.8 * mm
        y_inicio = PH - 18.5 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        txt_bil = 'Bilhete ' + str(pg_num) + ' de ' + str(total_pag)
        c.drawString(margem_x, y_inicio - len(linhas_resumo) * linha_h, txt_bil)

    c.setFillColorRGB(0, 0, 0)

    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy   = jogo_oy(jogo)
        lo   = linhaOffset if jogo == 1 else (linhaOffset2 if jogo == 2 else linhaOffset3)
        for dez in combo:
            col   = get_col(dez)
            lin   = get_lin(dez)
            cx_px = col_x_base[col] + offsetX + colOffset[col]
            cy_px = lin_y_base[lin] + oy + offsetY + lin * espLinha + lo[lin]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW / 2) * SCALE
            rh = (elH / 2) * SCALE
            c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    rw = (elW / 2) * SCALE
    rh = (elH / 2) * SCALE
    ultima_y = lin_y_base[4] + jogo_oy(3) + offsetY
    mdz_base_y = ultima_y + 55

    is_l2  = dez_por_aposta >= 16
    mdz_idx = dez_por_aposta - 16 if is_l2 else dez_por_aposta - 6
    mdz_arr = MDZ_POS_X_L2 if is_l2 else MDZ_POS_X_L1
    if 0 <= mdz_idx < len(mdz_arr):
        mdz_bx = MDZ_BASE_X + offsetX + mdz_offset_x + mdz_arr[mdz_idx]
        mdz_by = mdz_base_y + mdz_offset_y + (mdz_l2_dy if is_l2 else 0)
        cx_pt  = mdz_bx * SCALE
        cy_pt  = PH - mdz_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    tei_opcoes = [3, 6, 9, 12]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tei_bx  = MDZ_BASE_X + offsetX + spr_offset_x + TEI_POS_X[tei_idx]
        tei_by  = mdz_base_y + 110 + spr_offset_y
        cx_pt   = tei_bx * SCALE
        cy_pt   = PH - tei_by * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["diadesorte"] = """\
# -*- coding: utf-8 -*-
import sys, json, random
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes    = data['combinacoes']
meses_por_jogo = data.get('mesesPorJogo', [])
offsetX        = data.get('offsetX', 0) - 4  # DELTA_X calibrado
offsetY        = data.get('offsetY', 0) + 59  # DELTA_Y calibrado
espLinha       = data.get('espLinha', 0)
colOffset      = data.get('colOffset', [0]*10)
linhaOffset    = data.get('linhaOffset',  [0]*4)
linhaOffset2   = data.get('linhaOffset2', [0]*4)
linhaOffset3   = data.get('linhaOffset3', [0]*4)
gapJogo12      = data.get('gapJogo12', 0) - 22  # DELTA_GAP12 calibrado
gapJogo23      = data.get('gapJogo23', 0) + 39  # DELTA_GAP23 calibrado
elW            = data.get('elW', 11)
elH            = data.get('elH', 8)
resumo         = data.get('resumo', '')
valor_comb     = data.get('valorCombinacaoUnit', 0)
tei_mult       = data.get('teimosinhaMult', 1)
total_pag      = data.get('totalPaginas', 1)
pagina_inicio  = data.get('paginaInicio', 0)
dez_por_aposta = data.get('dezPorAposta', 7)
teimosinha     = data.get('teimosinha', 0)
mdzOffsetX     = data.get('mdzOffsetX', 0) - 1  # DELTA_MDZ_X calibrado
mdzOffsetY     = data.get('mdzOffsetY', 0) - 301  # DELTA_MDZ_Y calibrado
sprOffsetX     = data.get('sprOffsetX', 0) - 2  # DELTA_SPR_X calibrado
sprOffsetY     = 0  # hardcoded — calibrar via tei_base_y_off
mesOffsetX     = data.get('mesOffsetX', 0) - 3  # DELTA_MES_X calibrado
mesOffsetY     = data.get('mesOffsetY', 0) - 22  # DELTA_MES_Y calibrado
col_x_base     = data.get('colXBase',  [58,101,146,188,233,277,323,366,408,452])
lin_y_base     = data.get('linYBase',  [241,264,286,308])
mes_col_x      = data.get('mesColX',   [61,140,232,322,403,493])
mes_y_l1       = data.get('mesYL1',    373)
mes_y_l2       = data.get('mesYL2',    398)
mes_y_offset   = data.get('mesYOffset', 132)
jogo2_base     = data.get('jogo2Base', 243)
jogo3_base     = data.get('jogo3Base', 402)
mdz_pos_x      = data.get('mdzBasePosX', [0,44,88,132,176,220,264,308,352])
mdz_base_x     = data.get('mdzBaseX',    58)
mdz_base_y_off = data.get('mdzBaseYOffset', 509)
tei_pos_x      = [1, 90, 171, 266]  # hardcoded calibrado
tei_base_x     = 58   # hardcoded
tei_base_y_off = 327  # hardcoded calibrado

PW = 84.2 * mm
PH = 185.7 * mm
SCALE = mm / (578 / 84.2)

def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

def jogo_oy(j):
    if j == 1: return 0
    if j == 2: return jogo2_base + gapJogo12
    return jogo3_base + gapJogo23

COMBOS_POR_PAG = 3
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]
    meses_pag  = meses_por_jogo[pg:pg+COMBOS_POR_PAG] if meses_por_jogo else []

    if resumo:
        c.setFont('Helvetica-Bold', 9)
        c.setFillColorRGB(0.55, 0.42, 0.0)  # dourado
        pg_num = pagina_inicio + pg // COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X', '.')
        base_idx = pagina_inicio + pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        if len(nums_pag) == 1: comb_txt = 'Combinacao: ' + nums_pag[0]
        else: comb_txt = 'Combinacoes: ' + ', '.join(nums_pag[:-1]) + ' e ' + nums_pag[-1]
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.1 * mm
        linha_h  = 2.8 * mm
        y_inicio = PH - 18.5 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        c.drawString(margem_x, y_inicio - len(linhas_resumo) * linha_h, 'Bilhete ' + str(pg_num) + ' de ' + str(total_pag))

    c.setFillColorRGB(0, 0, 0)

    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy   = jogo_oy(jogo)
        lo   = linhaOffset if jogo == 1 else (linhaOffset2 if jogo == 2 else linhaOffset3)

        # Dezenas
        for dez in combo:
            col   = get_col(dez)
            lin   = get_lin(dez)
            cx_px = col_x_base[col] + offsetX + colOffset[col]
            cy_px = lin_y_base[lin] + oy + offsetY + lin * espLinha + lo[lin]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW / 2) * SCALE; rh = (elH / 2) * SCALE
            c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

        # Mês de Sorte
        mes_idx = meses_pag[j_idx] if j_idx < len(meses_pag) else random.randint(0, 11)
        mx_px = mes_col_x[mes_idx % 6] + offsetX + mesOffsetX
        my_base = lin_y_base[0] + oy + mes_y_offset + offsetY + mesOffsetY
        my_extra = 0 if mes_idx < 6 else (mes_y_l2 - mes_y_l1)
        my_px = my_base + my_extra
        mx_pt = mx_px * SCALE; my_pt = PH - my_px * SCALE
        rw = (elW / 2) * SCALE; rh = (elH / 2) * SCALE
        c.ellipse(mx_pt - rw, my_pt - rh, mx_pt + rw, my_pt + rh, fill=1, stroke=0)

    # Marcador qtd dezenas
    jogo3_oy = jogo_oy(3)
    mdz_by   = lin_y_base[0] + jogo3_oy + mdz_base_y_off + offsetY + mdzOffsetY
    mdz_idx  = dez_por_aposta - 7
    if 0 <= mdz_idx < len(mdz_pos_x):
        mdz_bx = mdz_base_x + offsetX + mdzOffsetX + mdz_pos_x[mdz_idx]
        cx_pt = mdz_bx * SCALE; cy_pt = PH - mdz_by * SCALE
        rw = (elW / 2) * SCALE; rh = (elH / 2) * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    # Teimosinha
    tei_opcoes = [3, 6, 9, 12]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tei_bx  = tei_base_x + offsetX + sprOffsetX + tei_pos_x[tei_idx]
        tei_by  = lin_y_base[0] + jogo3_oy + tei_base_y_off + offsetY + sprOffsetY
        cx_pt = tei_bx * SCALE; cy_pt = PH - tei_by * SCALE
        rw = (elW / 2) * SCALE; rh = (elH / 2) * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["timemania"] = """\
# -*- coding: utf-8 -*-
import sys, json, random
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data        = json.loads(open(sys.argv[1], encoding='utf-8').read())
out         = sys.argv[2]

combinacoes  = data['combinacoes']
offsetX      = data.get('offsetX', 0)
offsetY      = data.get('offsetY', 0)
espLinha     = data.get('espLinha', 0)
colOffset    = data.get('colOffset',   [0]*10)
linhaOffset  = data.get('linhaOffset', [0]*8)
elW          = data.get('elW', 11)
elH          = data.get('elH', 8)
teimosinha   = data.get('teimosinha', 0)
teiOffsetX   = data.get('teiOffsetX', 0)
teiOffsetY   = data.get('teiOffsetY', 0)
timeMarcado  = data.get('timeMarcado', None)
timeIdx      = data.get('timeIdx', None)
timeOffsetX  = data.get('timeOffsetX', 0)
timeOffsetY  = data.get('timeOffsetY', 0)
resumo       = data.get('resumo', '')
valor_comb   = data.get('valorCombinacaoUnit', 0)
total_pag    = data.get('totalPaginas', 1)

PW    = 84.2 * mm
PH    = 185.7 * mm
SCALE = mm / (578 / 84.2)

# Grade de dezenas calibrada (10 colunas x 8 linhas)
COL_X_BASE = [96, 141, 185, 228, 274, 316, 362, 404, 448, 493]
LIN_Y_BASE = [226, 251, 276, 301, 325, 350, 375, 400]

# Teimosinha [03][06][09][12]
TEI_Y = 1104
TEI_X = [184, 228, 273, 319]

# Times do Coracao — posicoes calibradas (x, y) no canvas 578x1274
TIMES_POS = {
    'ABC/RN': [54, 399],
    'Altos/PI': [54, 424],
    'América/MG': [54, 449],
    'América/RN': [54, 474],
    'Aparecidense/GO': [54, 499],
    'Athletico/PR': [54, 524],
    'Atlético/AC': [54, 549],
    'Atlético/CE': [54, 574],
    'Atlético/GO': [54, 599],
    'Atlético/MG': [54, 624],
    'Avaí/SC': [54, 649],
    'Bahia/BA': [54, 674],
    'Boa Esporte/MG': [54, 699],
    'Boavista/RJ': [54, 724],
    'Botafogo/PB': [54, 749],
    'Botafogo/RJ': [54, 774],
    'Botafogo/SP': [54, 799],
    'Bragantino/SP': [54, 824],
    'Brasil/RS': [54, 849],
    'Brasiliense/DF': [54, 874],
    'Brusque/SC': [54, 899],
    'Campinense/PB': [54, 924],
    'Caxias/RS': [54, 949],
    'Ceará/CE': [54, 974],
    'Chapecoense/SC': [54, 999],
    'Cianorte/PR': [54, 1024],
    'Confiança/SE': [54, 1049],
    'Corinthians/SP': [230, 399],
    'Coritiba/PR': [230, 424],
    'CRB/AL': [230, 449],
    'Criciúma/SC': [230, 474],
    'Cruzeiro/MG': [230, 499],
    'CSA/AL': [230, 524],
    'Cuiabá/MT': [230, 549],
    'Ferroviária/SP': [230, 574],
    'Ferroviário/CE': [230, 599],
    'Figueirense/SC': [230, 624],
    'Flamengo/RJ': [230, 649],
    'Floresta/CE': [230, 674],
    'Fluminense/RJ': [230, 699],
    'Fortaleza/CE': [230, 724],
    'Goiás/GO': [230, 749],
    'Grêmio/RS': [230, 774],
    'Guarani/SP': [230, 799],
    'Imperatriz/MA': [230, 824],
    'Internacional/RS': [230, 849],
    'Ituano/SP': [230, 874],
    'Jacuipense/BA': [230, 899],
    'Joinville/SC': [230, 924],
    'Juazeirense/BA': [230, 949],
    'Juventude/RS': [230, 974],
    'Londrina/PR': [230, 999],
    'Luverdense/MT': [230, 1024],
    'Manaus/AM': [230, 1049],
    'Mirassol/SP': [406, 401],
    'Moto Club/MA': [406, 426],
    'Náutico/PE': [406, 451],
    'Novorizontino/SP': [406, 476],
    'Oeste/SP': [406, 501],
    'Operário/PR': [406, 526],
    'Palmeiras/SP': [406, 551],
    'Paraná/PR': [406, 576],
    'Paysandu/PA': [406, 601],
    'Ponte Preta/SP': [406, 626],
    'Remo/PA': [406, 651],
    'Samp Corrêa/MA': [406, 676],
    'Santa Cruz/PE': [406, 701],
    'Santos/SP': [406, 726],
    'São Bento/SP': [406, 751],
    'São José/RS': [406, 776],
    'São Paulo/SP': [406, 801],
    'S Raimundo/RR': [406, 826],
    'Sport/PE': [406, 851],
    'Tombense/MG': [406, 876],
    'Treze/PB': [406, 901],
    'Vasco/RJ': [406, 926],
    'Vila Nova/GO': [406, 951],
    'Vitória/BA': [406, 976],
    'V Redonda/RJ': [406, 1001],
    'Ypiranga/RS': [406, 1026]
}

LISTA_TIMES = list(TIMES_POS.keys())

def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

COMBOS_POR_PAG = 1
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg, combo in enumerate(combinacoes):
    if pg > 0: c.showPage()

    # Resumo
    if resumo:
        c.setFont(_font_name, 9)
        c.setFillColorRGB(0.18, 0.49, 0.18)  # verde Timemania
        pg_num = pg + 1
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X','.')
        tei_mult = data.get('teimosinhaMult', 1)
        valor_bilhete = valor_comb * tei_mult
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append('Bilhete ' + str(pg_num) + ' de ' + str(total_pag))
        margem_x = 7.1 * mm
        linha_h  = 2.8 * mm
        y_inicio = PH - 18.5 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())

    c.setFillColorRGB(0, 0, 0)
    rw = (elW / 2) * SCALE
    rh = (elH / 2) * SCALE

    # Dezenas
    for dez in combo:
        col   = get_col(dez)
        lin   = get_lin(dez)
        cx_px = COL_X_BASE[col] + offsetX + colOffset[col]
        cy_px = LIN_Y_BASE[lin] + offsetY + lin * espLinha + linhaOffset[lin]
        cx_pt = cx_px * SCALE
        cy_pt = PH - cy_px * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

    # Teimosinha
    tei_opcoes = [3, 6, 9, 12]
    if teimosinha > 0 and teimosinha in tei_opcoes:
        tei_idx = tei_opcoes.index(teimosinha)
        tx_px = TEI_X[tei_idx] + teiOffsetX
        ty_px = TEI_Y + teiOffsetY
        tx_pt = tx_px * SCALE
        ty_pt = PH - ty_px * SCALE
        c.ellipse(tx_pt - rw, ty_pt - rh, tx_pt + rw, ty_pt + rh, fill=1, stroke=0)

    # Time do Coracao
    if timeMarcado and timeMarcado in TIMES_POS:
        time_nome = timeMarcado
    elif timeIdx is not None and 0 <= timeIdx < len(LISTA_TIMES):
        time_nome = LISTA_TIMES[timeIdx]
    else:
        time_nome = random.choice(LISTA_TIMES)
    if time_nome in TIMES_POS:
        tx, ty = TIMES_POS[time_nome]
        tx_px = tx + timeOffsetX
        ty_px = ty + timeOffsetY
        tx_pt = tx_px * SCALE
        ty_pt = PH - ty_px * SCALE
        c.ellipse(tx_pt - rw, ty_pt - rh, tx_pt + rw, ty_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))

"""

SCRIPTS["supersete"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes  = data['combinacoes']
offsetX      = data.get('offsetX', 0)
offsetY      = data.get('offsetY', 0)
colOffset    = data.get('colOffset',   [0]*7)
linhaOffset  = data.get('linhaOffset', [0]*10)
elW          = data.get('elW', 11)
elH          = data.get('elH', 8)
resumo       = data.get('resumo', '')
valor_comb   = data.get('valorCombinacaoUnit', 0)
tei_mult     = data.get('teimosinhaMult', 1)
total_pag    = data.get('totalPaginas', 1)
pagina_inicio = data.get('paginaInicio', 0)

# Posicoes X das 7 colunas (calibrar via sliders no componente)
col_x_base = data.get('colXBase',  [76, 141, 207, 272, 337, 401, 467])
# Posicoes Y dos 10 digitos 0-9 (calibrar via sliders no componente)
lin_y_base = data.get('linYBase',  [221, 249, 277, 305, 333, 361, 389, 417, 445, 473])

PW = 82.0 * mm
PH = 186.0 * mm
SCALE = mm / (578 / 82.0)

COMBOS_POR_PAG = 1
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg, combo in enumerate(combinacoes):
    if pg > 0: c.showPage()

    if resumo:
        c.setFont(_font_name, 10)
        c.setFillColorRGB(0, 0, 0)
        pg_num = pagina_inicio + pg + 1
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X','.')
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_comb * tei_mult)).split('|')
        linhas_resumo.append('Bilhete ' + str(pg_num) + ' de ' + str(total_pag))
        margem_x = 7.1 * mm
        linha_h  = 3.5 * mm
        y_inicio = PH - 19.4 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())

    c.setFillColorRGB(0, 0, 0)
    rw = (elW / 2) * SCALE
    rh = (elH / 2) * SCALE

    # combo pode ser:
    # - lista de 7 inteiros [d0,d1,...,d6] (um digito por coluna)
    # - lista de 7 listas [[d0],[d1],...] (formato cartesiano do gerador)
    for col_idx, item in enumerate(combo):
        if col_idx >= 7: break
        digito = item[0] if isinstance(item, (list, tuple)) else item
        lin_idx = int(digito)  # digito 0-9 = linha 0-9
        cx_px = col_x_base[col_idx] + offsetX + colOffset[col_idx]
        cy_px = lin_y_base[lin_idx] + offsetY + linhaOffset[lin_idx]
        cx_pt = cx_px * SCALE
        cy_pt = PH - cy_px * SCALE
        c.ellipse(cx_pt - rw, cy_pt - rh, cx_pt + rw, cy_pt + rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["quina_sao_joao"] = """\
# -*- coding: utf-8 -*-
import sys, json, os
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_name = 'Helvetica'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font_name = 'CustomFont'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

combinacoes    = data['combinacoes']
offsetX        = data.get('offsetX', 0)
offsetY        = data.get('offsetY', 0)
espLinha       = data.get('espLinha', 0)
colOffset1     = data.get('colOffset1', [0]*10)
colOffset2     = data.get('colOffset2', [0]*10)
linhaOffset1   = data.get('linhaOffset1', [0]*8)
linhaOffset2   = data.get('linhaOffset2', [0]*8)
lin_x_offset1  = data.get('linhaOffsetX1', [0]*8)
lin_x_offset2  = data.get('linhaOffsetX2', [0]*8)
lin2_col_x1    = data.get('lin2ColX1', [0]*10)
gapJogo1       = data.get('gapJogo1', 0)
gapJogo12      = data.get('gapJogo12', 0)
elW            = data.get('elW', 10.8)
elH            = data.get('elH', 9.7)
resumo         = data.get('resumo', '')
valor_comb     = data.get('valorCombinacaoUnit', 0)
tei_mult       = data.get('teimosinhaMult', 1)
total_pag      = data.get('totalPaginas', 1)
pagina_inicio  = data.get('paginaInicio', 0)
dez_por_aposta = data.get('dezPorAposta', 5)
header_color_hex = data.get('headerColor', '#6a0dad')
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
hdr_r, hdr_g, hdr_b = hex_to_rgb(header_color_hex)
mdz_pos_x      = data.get('mdzPosX', [0, 41, 82, 123, 164, 205, 250, 296, 345, 394, 441])
mdz_offset_x   = data.get('mdzOffsetX', 0)
mdz_offset_y   = data.get('mdzOffsetY', 0)
col_x_base     = data.get('colXBase', [107.3]*10)
col1_x_base    = data.get('col1XBase', col_x_base)
col2_x_base    = data.get('col2XBase', col_x_base)
lin_y_base     = data.get('linYBase', [223.9,247.3,268.7,290.1,313.5,335.9,359.3,382.7])
lin1_y_base    = data.get('lin1YBase', lin_y_base)
jogo1_base     = data.get('jogo1Base', 220)
jogo2_base     = data.get('jogo2Base', 445)

PW = 77.7 * mm
PH = 169.3 * mm
SCALE = mm / (578 / 77.7)


def get_col(dez): return (dez - 1) % 10
def get_lin(dez): return (dez - 1) // 10

def jogo_oy(j):
    if j == 1: return jogo1_base + gapJogo1
    return jogo2_base + gapJogo12

COMBOS_POR_PAG = 2
c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

for pg in range(0, len(combinacoes), COMBOS_POR_PAG):
    if pg > 0: c.showPage()
    combos_pag = combinacoes[pg:pg+COMBOS_POR_PAG]


    if resumo:
        # Retangulo de fundo do cabecalho
        c.setFont('Helvetica-Bold', 10)
        c.setFillColorRGB(hdr_r, hdr_g, hdr_b)
        pg_num = pagina_inicio + pg // COMBOS_POR_PAG + 1
        n_jogos = len(combos_pag)
        valor_bilhete = valor_comb * n_jogos * tei_mult
        def fmt_brl(v):
            return 'R$ {:,.2f}'.format(v).replace(',','X').replace('.', ',').replace('X','.')
        base_idx = pagina_inicio + pg // COMBOS_POR_PAG
        nums_pag = [str(base_idx * COMBOS_POR_PAG + i + 1).zfill(2) for i in range(n_jogos)]
        comb_txt = ('Combinacao: ' + nums_pag[0]) if len(nums_pag)==1 else ('Combinacoes: ' + ' e '.join(nums_pag))
        linhas_resumo = resumo.replace('[POR_BILHETE]', fmt_brl(valor_bilhete)).split('|')
        linhas_resumo.append(comb_txt)
        margem_x = 7.0 * mm
        linha_h  = 4.0 * mm
        y_inicio = PH - 23.5 * mm
        for li, linha in enumerate(linhas_resumo):
            c.drawString(margem_x, y_inicio - li * linha_h, linha.strip())
        c.drawString(margem_x, y_inicio - len(linhas_resumo)*linha_h, 'Bilhete '+str(pg_num)+' de '+str(total_pag))

    c.setFillColorRGB(0, 0, 0)
    for j_idx, combo in enumerate(combos_pag):
        jogo = j_idx + 1
        oy   = jogo_oy(jogo)
        co   = colOffset1 if jogo == 1 else colOffset2
        lo   = linhaOffset1 if jogo == 1 else linhaOffset2
        col_b = col1_x_base if jogo == 1 else col2_x_base
        lin_b = lin1_y_base if jogo == 1 else lin_y_base
        lx   = lin_x_offset1 if jogo == 1 else lin_x_offset2
        for dez in combo:
            col   = get_col(dez)
            lin   = get_lin(dez)
            lin2x = lin2_col_x1[col] if (jogo == 1 and lin == 1) else 0
            cx_px = col_b[col] + offsetX + co[col] + lx[lin] + lin2x
            cy_px = lin_b[lin] + oy + offsetY + lin * espLinha + lo[lin]
            cx_pt = cx_px * SCALE
            cy_pt = PH - cy_px * SCALE
            rw = (elW/2)*SCALE; rh = (elH/2)*SCALE
            c.ellipse(cx_pt-rw, cy_pt-rh, cx_pt+rw, cy_pt+rh, fill=1, stroke=0)

    rw = (elW/2)*SCALE; rh = (elH/2)*SCALE
    ultima_y = lin_y_base[7] + jogo_oy(2) + offsetY

    mdz_idx = dez_por_aposta - 5
    if 0 <= mdz_idx < len(mdz_pos_x):
        mdz_bx = col1_x_base[0] + offsetX + colOffset1[0] + mdz_offset_x + mdz_pos_x[mdz_idx]
        mdz_by = ultima_y + 76.5 + mdz_offset_y
        cx_pt = mdz_bx*SCALE; cy_pt = PH - mdz_by*SCALE
        c.ellipse(cx_pt-rw, cy_pt-rh, cx_pt+rw, cy_pt+rh, fill=1, stroke=0)

c.save()
print('OK:' + str(len(combinacoes)))
"""

SCRIPTS["conferencia"] = """\
# -*- coding: utf-8 -*-
import sys, json, os
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_bold_paths = [
    'C:/Windows/Fonts/arialbd.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]
_font = 'Helvetica'
_font_bold = 'Helvetica-Bold'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CF', _fp))
            _font = 'CF'
        except: pass
        break
for _fp in _font_bold_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CFB', _fp))
            _font_bold = 'CFB'
        except: pass
        break

data = json.loads(open(sys.argv[1], encoding='utf-8').read())
out  = sys.argv[2]

modalidade       = data.get('modalidade', '')
concurso         = data.get('concurso', {})
arquivo          = data.get('arquivo', '')
id_jogo          = data.get('idJogo', '')
total_comb       = data.get('totalCombinacoes', 0)
contagem         = data.get('contagem', {})
premiadas        = data.get('premiadas', [])
faixas           = data.get('faixas', [])
faixas1          = data.get('faixas1', None)
faixas2          = data.get('faixas2', None)
sorteados2       = concurso.get('sorteados2', [])
total_premio     = data.get('total_premio', 0)

num_concurso  = concurso.get('num', '')
data_concurso = concurso.get('data', '')
sorteados     = concurso.get('sorteados', [])
acumulado     = concurso.get('acumulado', False)
valor_proximo = concurso.get('valorProximo', '')
rateios       = concurso.get('rateios', [])

DIAS = ['Dom','Seg','Ter','Qua','Qui','Sex','Sab']

def parse_dia(data_str):
    try:
        import datetime
        d, m, a = data_str.split('/')
        dt = datetime.date(int(a), int(m), int(d))
        return DIAS[(dt.weekday() + 1) % 7]
    except:
        return ''

def fmt_brl(v):
    try:
        return 'R$ {:,.2f}'.format(float(v)).replace(',','X').replace('.', ',').replace('X','.')
    except:
        return 'R$ 0,00'

NOMES_MOD = {
    'lotofacil': 'Lotofacil',
    'megasena': 'Mega Sena',
    'quina': 'Quina',
    'duplasena': 'Dupla Sena',
    'lotomania': 'Lotomania',
    'diadesorte': 'Dia de Sorte',
    'timemania': 'Timemania',
    'supersete': 'Super Sete',
    'mais-milionaria': '+Milionaria',
}
nome_mod = NOMES_MOD.get(modalidade, modalidade)

COR_VERDE       = colors.HexColor('#1b7a1b')
COR_VERDE_LIGHT = colors.HexColor('#e8f5e9')
COR_VERDE_MID   = colors.HexColor('#c8e6c9')
COR_CINZA       = colors.HexColor('#f5f5f5')
COR_BORDA       = colors.HexColor('#e0e0e0')
COR_TEXTO       = colors.HexColor('#1a1a1a')
COR_SUB         = colors.HexColor('#757575')
COR_BRANCO      = colors.white
COR_OURO        = colors.HexColor('#f9a825')

PW = 210 * mm
PH = 297 * mm
M  = 14 * mm
CW = PW - 2 * M

c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

# ── CABECALHO ────────────────────────────────────────────────────────────────
c.setFillColor(COR_VERDE)
c.rect(0, PH - 30*mm, PW, 30*mm, fill=1, stroke=0)
c.setFont(_font_bold, 16)
c.setFillColor(COR_BRANCO)
c.drawString(M, PH - 13*mm, 'VCVL -- Verificador e Combinador de Loterias')
c.setFont(_font, 10)
c.drawString(M, PH - 21*mm, 'Resultado da Conferencia -- ' + nome_mod)
c.setFont(_font, 8)
c.setFillColor(colors.HexColor('#c8e6c9'))
c.drawRightString(PW - M, PH - 13*mm, 'Concurso N. ' + str(num_concurso))
dia_sem = parse_dia(str(data_concurso))
c.drawRightString(PW - M, PH - 20*mm, 'Data: ' + dia_sem + ' ' + str(data_concurso))

y = PH - 34*mm

# ── NUMEROS SORTEADOS ────────────────────────────────────────────────────────
c.setFillColor(COR_VERDE_LIGHT)
c.setStrokeColor(COR_BORDA)
c.setLineWidth(0.5)
c.roundRect(M, y - 16*mm, CW, 16*mm, 3*mm, fill=1, stroke=1)
c.setFont(_font_bold, 9)
c.setFillColor(COR_VERDE)
c.drawString(M + 3*mm, y - 5*mm, 'Numeros Sorteados:')
c.setFont(_font_bold, 11)
c.setFillColor(COR_TEXTO)
nums_str = '   '.join([str(n).zfill(2) for n in sorteados])
c.drawString(M + 3*mm, y - 12*mm, nums_str)
if acumulado:
    c.setFont(_font_bold, 9)
    c.setFillColor(COR_OURO)
    c.drawRightString(PW - M - 3*mm, y - 8*mm, 'ACUMULADO')
    if valor_proximo:
        c.setFont(_font, 8)
        c.drawRightString(PW - M - 3*mm, y - 13*mm, 'Proximo: ' + str(valor_proximo))
y -= 20*mm

# ── INFO DO JOGO ─────────────────────────────────────────────────────────────
c.setFont(_font, 8)
c.setFillColor(COR_SUB)
c.drawString(M, y, 'Arquivo: ' + str(arquivo) + '   |   ID: ' + str(id_jogo) + '   |   Total de combinacoes: ' + str(total_comb))
y -= 8*mm

# ── TABELA DE RESULTADOS ─────────────────────────────────────────────────────
c.setFillColor(COR_VERDE)
c.rect(M, y - 8*mm, CW, 8*mm, fill=1, stroke=0)
c.setFont(_font_bold, 9)
c.setFillColor(COR_BRANCO)
c.drawString(M + 3*mm, y - 5.5*mm, 'Faixa')
c.drawString(M + 60*mm, y - 5.5*mm, 'Combinacoes Premiadas')
c.drawRightString(M + CW - 3*mm, y - 5.5*mm, 'Valor Total')
y -= 8*mm

# Dupla Sena: faixas separadas por sorteio
if faixas1 is not None and faixas2 is not None:
    COR_DS1 = colors.HexColor('#c62828')
    COR_DS2 = colors.HexColor('#e65100')
    # 1o sorteio
    c.setFillColor(colors.HexColor('#ffebee'))
    c.rect(M, y - 7*mm, CW, 7*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 9); c.setFillColor(COR_DS1)
    c.drawString(M + 3*mm, y - 4.5*mm, '1º SORTEIO DO CONCURSO N. ' + str(num_concurso))
    y -= 7*mm
    f1p = [f for f in faixas1 if f.get('quantidade', 0) > 0]
    if not f1p:
        c.setFillColor(COR_CINZA); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
        c.setFont(_font, 8); c.setFillColor(COR_SUB)
        c.drawString(M + 3*mm, y - 3.8*mm, 'Nenhum premio no 1. sorteio')
        y -= 6*mm
    else:
        for i, f in enumerate(f1p):
            bg = COR_BRANCO if i % 2 == 0 else COR_CINZA
            c.setFillColor(bg); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
            c.setFont(_font_bold, 9); c.setFillColor(COR_DS1)
            c.drawString(M + 3*mm, y - 3.8*mm, str(f.get('acertos', f.get('faixa',''))) + ' acertos')
            c.setFont(_font, 9); c.setFillColor(COR_TEXTO)
            c.drawString(M + 40*mm, y - 3.8*mm, str(f.get('quantidade', 0)) + ' combinacao(oes)')
            c.setFont(_font_bold, 9); c.setFillColor(COR_DS1)
            c.drawRightString(M + CW - 3*mm, y - 3.8*mm, fmt_brl(f.get('valor_total', 0)))
            y -= 6*mm
    sub1 = sum(f.get('valor_total',0) for f in f1p)
    c.setFillColor(colors.HexColor('#ffcdd2')); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 9); c.setFillColor(COR_DS1)
    c.drawString(M + 3*mm, y - 3.8*mm, 'Subtotal 1º sorteio')
    c.drawRightString(M + CW - 3*mm, y - 3.8*mm, fmt_brl(sub1))
    y -= 8*mm
    # 2o sorteio
    c.setFillColor(colors.HexColor('#fff3e0'))
    c.rect(M, y - 7*mm, CW, 7*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 9); c.setFillColor(COR_DS2)
    c.drawString(M + 3*mm, y - 4.5*mm, '2º SORTEIO DO CONCURSO N. ' + str(num_concurso))
    y -= 7*mm
    f2p = [f for f in faixas2 if f.get('quantidade', 0) > 0]
    if not f2p:
        c.setFillColor(COR_CINZA); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
        c.setFont(_font, 8); c.setFillColor(COR_SUB)
        c.drawString(M + 3*mm, y - 3.8*mm, 'Nenhum premio no 2. sorteio')
        y -= 6*mm
    else:
        for i, f in enumerate(f2p):
            bg = COR_BRANCO if i % 2 == 0 else COR_CINZA
            c.setFillColor(bg); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
            c.setFont(_font_bold, 9); c.setFillColor(COR_DS2)
            c.drawString(M + 3*mm, y - 3.8*mm, str(f.get('acertos', f.get('faixa',''))) + ' acertos')
            c.setFont(_font, 9); c.setFillColor(COR_TEXTO)
            c.drawString(M + 40*mm, y - 3.8*mm, str(f.get('quantidade', 0)) + ' combinacao(oes)')
            c.setFont(_font_bold, 9); c.setFillColor(COR_DS2)
            c.drawRightString(M + CW - 3*mm, y - 3.8*mm, fmt_brl(f.get('valor_total', 0)))
            y -= 6*mm
    sub2 = sum(f.get('valor_total',0) for f in f2p)
    c.setFillColor(colors.HexColor('#ffe0b2')); c.rect(M, y - 6*mm, CW, 6*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 9); c.setFillColor(COR_DS2)
    c.drawString(M + 3*mm, y - 3.8*mm, 'Subtotal 2º sorteio')
    c.drawRightString(M + CW - 3*mm, y - 3.8*mm, fmt_brl(sub2))
    y -= 8*mm
else:
    faixas_com_premio = [f for f in faixas if f.get('quantidade', 0) > 0]
    if not faixas_com_premio:
        c.setFillColor(COR_CINZA)
        c.rect(M, y - 10*mm, CW, 10*mm, fill=1, stroke=0)
        c.setFont(_font, 10)
        c.setFillColor(COR_SUB)
        c.drawCentredString(M + CW/2, y - 6.5*mm, 'Nenhuma combinacao premiada neste concurso.')
        y -= 14*mm
    else:
        for i, f in enumerate(faixas_com_premio):
            bg = COR_BRANCO if i % 2 == 0 else COR_CINZA
            c.setFillColor(bg)
            c.rect(M, y - 8*mm, CW, 8*mm, fill=1, stroke=0)
            c.setFont(_font_bold, 9)
            c.setFillColor(COR_VERDE)
            c.drawString(M + 3*mm, y - 5.5*mm, str(f.get('faixa', '')))
            c.setFont(_font, 9)
            c.setFillColor(COR_TEXTO)
            c.drawString(M + 60*mm, y - 5.5*mm, str(f.get('quantidade', 0)) + ' combinacao(oes)')
            c.setFont(_font_bold, 9)
            c.setFillColor(COR_VERDE)
            c.drawRightString(M + CW - 3*mm, y - 5.5*mm, fmt_brl(f.get('valor_total', 0)))
            y -= 8*mm
        y -= 4*mm

# ── TOTAL ────────────────────────────────────────────────────────────────────
c.setFillColor(COR_VERDE_LIGHT)
c.setStrokeColor(COR_VERDE)
c.setLineWidth(1.5)
c.roundRect(M, y - 12*mm, CW, 12*mm, 3*mm, fill=1, stroke=1)
c.setFont(_font_bold, 11)
c.setFillColor(COR_TEXTO)
c.drawString(M + 4*mm, y - 8*mm, 'TOTAL GANHO NESTE CONCURSO N. ' + str(num_concurso))
c.setFont(_font_bold, 16)
c.setFillColor(COR_VERDE)
c.drawRightString(M + CW - 4*mm, y - 8.5*mm, fmt_brl(total_premio))
y -= 16*mm



# ── GANHADORES POR FAIXA ────────────────────────────────────────────────────────
if rateios:
    y -= 4*mm
    # Separar rateios por sorteio para Dupla Sena
    rateios_s1 = [r for r in rateios if '1' in str(r.get('faixa','')) and 'sorteio' in str(r.get('faixa','')).lower()] if faixas1 is not None else []
    rateios_s2 = [r for r in rateios if '2' in str(r.get('faixa','')) and 'sorteio' in str(r.get('faixa','')).lower()] if faixas2 is not None else []
    rateios_outros = [r for r in rateios if r not in rateios_s1 and r not in rateios_s2] if faixas1 is not None else rateios

    def bloco_rateio(lista, titulo, cor_titulo, cor_fundo, y_pos):
        c.setFillColor(cor_fundo)
        c.rect(M, y_pos - 7*mm, CW, 7*mm, fill=1, stroke=0)
        c.setFont(_font_bold, 8); c.setFillColor(cor_titulo)
        c.drawString(M + 3*mm, y_pos - 4.5*mm, titulo)
        y_pos -= 7*mm
        for i, r in enumerate(lista):
            bg = COR_BRANCO if i % 2 == 0 else COR_CINZA
            c.setFillColor(bg); c.rect(M, y_pos - 6*mm, CW, 6*mm, fill=1, stroke=0)
            c.setFont(_font, 7.5); c.setFillColor(COR_TEXTO)
            c.drawString(M + 3*mm, y_pos - 4*mm, str(r.get('faixa', '')))
            c.drawString(M + 70*mm, y_pos - 4*mm, str(r.get('ganhadores', 0)) + ' ganhador(es)')
            c.setFont(_font_bold, 7.5); c.setFillColor(cor_titulo)
            c.drawRightString(M + CW - 3*mm, y_pos - 4*mm, fmt_brl(r.get('valor', 0)) + ' cada')
            y_pos -= 6*mm
        return y_pos

    if faixas1 is not None and (rateios_s1 or rateios_s2):
        if rateios_s1:
            y = bloco_rateio(rateios_s1, '1º Sorteio -- Ganhadores por faixa -- Concurso N. ' + str(num_concurso), colors.HexColor('#c62828'), colors.HexColor('#ffebee'), y)
        if rateios_s2:
            y = bloco_rateio(rateios_s2, '2º Sorteio -- Ganhadores por faixa -- Concurso N. ' + str(num_concurso), colors.HexColor('#e65100'), colors.HexColor('#fff3e0'), y)
        if rateios_outros:
            y = bloco_rateio(rateios_outros, 'Demais premios -- Concurso N. ' + str(num_concurso), COR_VERDE, COR_VERDE_MID, y)
    else:
        y = bloco_rateio(rateios, 'Numero de ganhadores por faixa de premios -- Concurso N. ' + str(num_concurso), COR_VERDE, COR_VERDE_MID, y)
    y -= 4*mm

# ── RODAPE ────────────────────────────────────────────────────────────────────
c.setFont(_font, 7)
c.setFillColor(COR_SUB)
c.setStrokeColor(COR_BORDA)
c.setLineWidth(0.5)
c.line(M, 10*mm, PW - M, 10*mm)
c.drawString(M, 7*mm, 'VCVL -- Relatorio gerado automaticamente')
c.drawRightString(PW - M, 7*mm, 'Pagina 1 de 1')

c.save()
print('OK')
"""

SCRIPTS["historico"] = """\
# -*- coding: utf-8 -*-
import sys, json
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
import os, datetime

_font_paths = [
    'C:/Windows/Fonts/arial.ttf',
    'C:/Windows/Fonts/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
_font_bold_paths = [
    'C:/Windows/Fonts/arialbd.ttf',
    'C:/Windows/Fonts/ArialBD.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
]
_font = 'Helvetica'
_font_bold = 'Helvetica-Bold'
for _fp in _font_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFont', _fp))
            _font = 'CustomFont'
        except: pass
        break
for _fp in _font_bold_paths:
    if os.path.exists(_fp):
        try:
            pdfmetrics.registerFont(TTFont('CustomFontBold', _fp))
            _font_bold = 'CustomFontBold'
        except: pass
        break

data       = json.loads(open(sys.argv[1], encoding='utf-8').read())
out        = sys.argv[2]
itens      = data['itens']        # lista de conferencias ordenadas
modalidade = data['modalidade']
resumo     = data['resumo']       # { faixas: [{faixa, quantidade, valor_total}], somaTotal }
agora      = data['agora']

DIAS = ['Dom','Seg','Ter','Qua','Qui','Sex','Sab']

def parse_dia(data_str):
    try:
        d, m, a = data_str.split('/')
        dt = datetime.date(int(a), int(m), int(d))
        return DIAS[dt.weekday() + 1 if dt.weekday() < 6 else 0]
    except:
        return ''

def fmt_brl(v):
    try:
        return 'R$ {:,.2f}'.format(float(v)).replace(',','X').replace('.', ',').replace('X','.')
    except:
        return 'R$ 0,00'

# Pagina A4
PW = 210 * mm
PH = 297 * mm
MARGIN = 14 * mm
CONTENT_W = PW - 2 * MARGIN

COR_VERDE       = colors.HexColor('#1b7a1b')
COR_VERDE_LIGHT = colors.HexColor('#e8f5e9')
COR_VERDE_MID   = colors.HexColor('#c8e6c9')
COR_CINZA       = colors.HexColor('#f5f5f5')
COR_CINZA_BORDA = colors.HexColor('#e0e0e0')
COR_TEXTO       = colors.HexColor('#1a1a1a')
COR_SUBTEXTO    = colors.HexColor('#757575')
COR_BRANCO      = colors.white

c = pdfcanvas.Canvas(out, pagesize=(PW, PH))
c.setViewerPreference('PrintScaling', 'None')

def nova_pagina(primeira=False):
    if not primeira:
        c.showPage()
    # Cabeçalho
    c.setFillColor(COR_VERDE)
    c.rect(0, PH - 28*mm, PW, 28*mm, fill=1, stroke=0)
    # Linha decorativa
    c.setFillColor(colors.HexColor('#2e7d32'))
    c.rect(0, PH - 30*mm, PW, 2*mm, fill=1, stroke=0)
    # Titulo
    c.setFont(_font_bold, 16)
    c.setFillColor(COR_BRANCO)
    c.drawString(MARGIN, PH - 13*mm, 'VCVL -- Verificador e Combinador de Loterias')
    c.setFont(_font, 10)
    c.drawString(MARGIN, PH - 20*mm, 'Relatorio de Conferencias -- ' + modalidade)
    # Data e periodo
    periodo = ''
    if itens:
        datas = sorted([h.get('data_concurso','') for h in itens])
        if datas[0] != datas[-1]:
            periodo = 'Periodo: ' + datas[0] + ' a ' + datas[-1]
        else:
            periodo = 'Data: ' + datas[0]
    c.setFont(_font, 8)
    c.setFillColor(colors.HexColor('#c8e6c9'))
    c.drawRightString(PW - MARGIN, PH - 13*mm, 'Gerado em: ' + agora)
    c.drawRightString(PW - MARGIN, PH - 19*mm, periodo)
    return PH - 32*mm  # y inicial disponivel

def rodape(pag_num, total_pags):
    c.setFont(_font, 7)
    c.setFillColor(COR_SUBTEXTO)
    c.setStrokeColor(COR_CINZA_BORDA)
    c.setLineWidth(0.5)
    c.line(MARGIN, 10*mm, PW - MARGIN, 10*mm)
    c.drawString(MARGIN, 7*mm, 'VCVL -- Relatorio gerado automaticamente em ' + agora)
    c.drawRightString(PW - MARGIN, 7*mm, 'Pagina ' + str(pag_num) + ' de ' + str(total_pags))

# ── Cards de estatísticas ────────────────────────────────────────────────────
def desenhar_cards(y):
    total_conc = len(itens)
    total_comb = itens[0].get('total_combinacoes', 0) if itens else 0
    total_prm  = sum(h.get('total_premio', 0) for h in itens)
    n_faixas   = len(resumo.get('faixas', []))

    card_w = (CONTENT_W - 9*mm) / 4
    card_h = 16*mm
    cards  = [
        (str(total_conc),  'Concursos'),
        (str(total_comb),  'Combinacoes por concurso'),
        (str(n_faixas),    'Faixas premiadas'),
        (fmt_brl(total_prm), 'Total ganho'),
    ]
    for i, (val, lbl) in enumerate(cards):
        x = MARGIN + i * (card_w + 3*mm)
        c.setFillColor(COR_CINZA)
        c.setStrokeColor(COR_CINZA_BORDA)
        c.setLineWidth(0.5)
        c.roundRect(x, y - card_h, card_w, card_h, 3*mm, fill=1, stroke=1)
        # Barra lateral verde
        c.setFillColor(COR_VERDE)
        c.rect(x, y - card_h, 2*mm, card_h, fill=1, stroke=0)
        # Valor
        font_sz = 13 if len(val) <= 8 else 10
        c.setFont(_font_bold, font_sz)
        c.setFillColor(COR_VERDE)
        c.drawString(x + 4*mm, y - 8*mm, val)
        # Label
        c.setFont(_font, 7)
        c.setFillColor(COR_SUBTEXTO)
        c.drawString(x + 4*mm, y - 13*mm, lbl)
    return y - card_h - 5*mm

# ── Cabeçalho da tabela principal ──────────────────────────────────────────
COL_WIDTHS = [32*mm, 18*mm, 32*mm, 18*mm, 28*mm, 30*mm]
COL_HEADERS = ['Data', 'Concurso', 'Faixa', 'Qtd', 'Vl. Unitario', 'Total']

def desenhar_header_tabela(y):
    x = MARGIN
    h = 7*mm
    c.setFillColor(COR_VERDE)
    c.rect(x, y - h, CONTENT_W, h, fill=1, stroke=0)
    c.setFont(_font_bold, 8)
    c.setFillColor(COR_BRANCO)
    xs = [x]
    for w in COL_WIDTHS[:-1]:
        xs.append(xs[-1] + w)
    for i, (hdr, xi) in enumerate(zip(COL_HEADERS, xs)):
        if i >= 3:
            c.drawRightString(xi + COL_WIDTHS[i] - 1*mm, y - 5*mm, hdr)
        else:
            c.drawString(xi + 1.5*mm, y - 5*mm, hdr)
    return y - h

def desenhar_linha(y, cols, bg, is_subtotal=False, borda_bottom=False):
    x = MARGIN
    h = 6*mm if not is_subtotal else 7*mm
    c.setFillColor(bg)
    c.rect(x, y - h, CONTENT_W, h, fill=1, stroke=0)
    if borda_bottom:
        c.setStrokeColor(COR_CINZA_BORDA)
        c.setLineWidth(0.3)
        c.line(x, y - h, x + CONTENT_W, y - h)
    xs = [x]
    for w in COL_WIDTHS[:-1]:
        xs.append(xs[-1] + w)
    font_sz = 8 if not is_subtotal else 8.5
    for i, (col, xi) in enumerate(zip(cols, xs)):
        if is_subtotal:
            c.setFont(_font_bold, font_sz)
            c.setFillColor(COR_VERDE if i == len(cols)-1 else COR_TEXTO)
        else:
            c.setFont(_font_bold if i < 2 else _font, font_sz)
            c.setFillColor(COR_VERDE if i < 2 else COR_TEXTO)
        if i >= 3:
            c.drawRightString(xi + COL_WIDTHS[i] - 1*mm, y - h + 1.8*mm, str(col))
        else:
            c.drawString(xi + 1.5*mm, y - h + 1.8*mm, str(col))
    return y - h

# ── Resumo final ────────────────────────────────────────────────────────────
def desenhar_resumo(y):
    faixas = resumo.get('faixas', [])
    soma   = resumo.get('somaTotal', 0)
    needed = (len(faixas) + 3) * 7*mm + 20*mm
    if y - needed < 15*mm:
        rodape(pag_atual[0], '?')
        pag_atual[0] += 1
        y = nova_pagina()

    # Titulo
    c.setFillColor(COR_VERDE)
    c.rect(MARGIN, y - 8*mm, CONTENT_W, 8*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 10)
    c.setFillColor(COR_BRANCO)
    c.drawString(MARGIN + 3*mm, y - 5.5*mm, 'Resumo Consolidado -- ' + str(len(itens)) + ' concurso(s) selecionado(s)')
    y -= 8*mm

    # Cabeçalho resumo
    rw = [60*mm, 50*mm, 50*mm]
    hdrs = ['Faixa', 'Total Combinacoes', 'Total R$']
    c.setFillColor(COR_VERDE_LIGHT)
    c.rect(MARGIN, y - 6*mm, CONTENT_W, 6*mm, fill=1, stroke=0)
    c.setFont(_font_bold, 8)
    c.setFillColor(COR_VERDE)
    rxs = [MARGIN, MARGIN+rw[0], MARGIN+rw[0]+rw[1]]
    for i, (hdr, rx) in enumerate(zip(hdrs, rxs)):
        c.drawString(rx + 1.5*mm, y - 4*mm, hdr)
    y -= 6*mm

    for fi, f in enumerate(faixas):
        bg = COR_BRANCO if fi % 2 == 0 else COR_CINZA
        c.setFillColor(bg)
        c.rect(MARGIN, y - 6*mm, CONTENT_W, 6*mm, fill=1, stroke=0)
        c.setFont(_font, 8)
        c.setFillColor(COR_TEXTO)
        c.drawString(MARGIN + 1.5*mm, y - 4*mm, str(f.get('faixa','')))
        c.drawString(rxs[1] + 1.5*mm, y - 4*mm, str(f.get('quantidade',0)))
        c.setFont(_font_bold, 8)
        c.setFillColor(COR_VERDE)
        c.drawString(rxs[2] + 1.5*mm, y - 4*mm, fmt_brl(f.get('valor_total',0)))
        y -= 6*mm

    # Total geral
    c.setFillColor(COR_VERDE_LIGHT)
    c.setStrokeColor(COR_VERDE)
    c.setLineWidth(1.5)
    c.rect(MARGIN, y - 9*mm, CONTENT_W, 9*mm, fill=1, stroke=1)
    c.setFont(_font_bold, 11)
    c.setFillColor(COR_TEXTO)
    c.drawString(MARGIN + 3*mm, y - 6*mm, 'TOTAL GERAL')
    c.setFont(_font_bold, 14)
    c.setFillColor(COR_VERDE)
    c.drawRightString(MARGIN + CONTENT_W - 3*mm, y - 6.5*mm, fmt_brl(soma))
    y -= 9*mm
    return y

# ── Renderização principal ───────────────────────────────────────────────────
pag_atual = [1]
y = nova_pagina(primeira=True)
y = desenhar_cards(y)
y -= 4*mm

y = desenhar_header_tabela(y)

cor_alterna = True
for h in itens:
    faixas_h = [f for f in (h.get('faixas') or []) if f.get('quantidade', 0) > 0]
    total_conc = sum(f.get('valor_total', 0) for f in faixas_h)
    dia = parse_dia(h.get('data_concurso', ''))
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

    if not faixas_h:
        y = desenhar_linha(y, [data_str, num_conc, 'Sem premiacao', '-', '-', 'R$ 0,00'], bg, borda_bottom=True)
    else:
        for i, f in enumerate(faixas_h):
            cols = [
                data_str if i == 0 else '',
                num_conc if i == 0 else '',
                str(f.get('faixa', '')),
                str(f.get('quantidade', 0)),
                fmt_brl(f.get('valor_unitario', 0)),
                fmt_brl(f.get('valor_total', 0)),
            ]
            y = desenhar_linha(y, cols, bg)
        # Subtotal do concurso
        id_jogo = h.get('id_jogo', '')
        n_combs = str(h.get('total_combinacoes', 0)) + ' comb. | ID: ' + id_jogo
        sub_cols = [n_combs, '', '', '', 'SUBTOTAL', fmt_brl(total_conc)]
        # Linha subtotal em verde claro
        c.setFillColor(COR_VERDE_MID)
        c.setStrokeColor(COR_CINZA_BORDA)
        c.setLineWidth(0.3)
        c.rect(MARGIN, y - sub_h, CONTENT_W, sub_h, fill=1, stroke=1)
        xs = [MARGIN]
        for w in COL_WIDTHS[:-1]:
            xs.append(xs[-1] + w)
        c.setFont(_font, 7)
        c.setFillColor(COR_SUBTEXTO)
        c.drawString(xs[0] + 1.5*mm, y - sub_h + 1.8*mm, n_combs)
        c.setFont(_font_bold, 9)
        c.setFillColor(COR_VERDE)
        c.drawRightString(xs[4] + COL_WIDTHS[4] - 1*mm, y - sub_h + 1.8*mm, 'SUBTOTAL')
        c.drawRightString(xs[5] + COL_WIDTHS[5] - 1*mm, y - sub_h + 1.8*mm, fmt_brl(total_conc))
        y -= sub_h + 1*mm

y -= 8*mm
y = desenhar_resumo(y)

# Atualizar número total de páginas
total_pags = pag_atual[0]
rodape(pag_atual[0], total_pags)

c.save()
print('OK:' + str(len(itens)))
"""


# ── Mapeamento de modalidade → script ─────────────────────────────────────────

def get_script_bilhete(modalidade):
    m = modalidade.lower().replace('-', '_').replace(' ', '_')
    if m in SCRIPTS:
        return SCRIPTS[m]
    return SCRIPTS.get('lotofacil', '')

# ── Rotas ─────────────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'ok': True, 'service': 'vcvl-pdf-server'})

@app.route('/bilhete-pdf', methods=['POST'])
def bilhete_pdf():
    try:
        body = request.get_json()
        if not body:
            return jsonify({'erro': 'Payload vazio'}), 400

        modalidade = body.get('modalidade', 'lotofacil')
        script_code = get_script_bilhete(modalidade)
        if not script_code:
            return jsonify({'erro': f'Modalidade nao suportada: {modalidade}'}), 400

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w', encoding='utf-8') as tmp_json:
            json.dump(body, tmp_json, ensure_ascii=False)
            tmp_json_path = tmp_json.name

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as tmp_py:
            tmp_py.write(script_code)
            tmp_py_path = tmp_py.name

        tmp_pdf_path = tmp_json_path.replace('.json', '.pdf')

        try:
            result = subprocess.run(
                [sys.executable, tmp_py_path, tmp_json_path, tmp_pdf_path],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return jsonify({'erro': 'Erro ao gerar PDF', 'detalhe': result.stderr}), 500

            filename = f"{modalidade}.pdf"
            return send_file(
                tmp_pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )
        finally:
            for p in [tmp_json_path, tmp_py_path]:
                try: os.unlink(p)
                except: pass

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/conferencia-pdf', methods=['POST'])
def conferencia_pdf():
    try:
        body = request.get_json()
        if not body:
            return jsonify({'erro': 'Payload vazio'}), 400

        modalidade = body.get('modalidade', 'lotofacil')
        script_code = SCRIPTS.get('conferencia', '')

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w', encoding='utf-8') as tmp_json:
            json.dump(body, tmp_json, ensure_ascii=False)
            tmp_json_path = tmp_json.name

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as tmp_py:
            tmp_py.write(script_code)
            tmp_py_path = tmp_py.name

        tmp_pdf_path = tmp_json_path.replace('.json', '.pdf')

        try:
            result = subprocess.run(
                [sys.executable, tmp_py_path, tmp_json_path, tmp_pdf_path],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return jsonify({'erro': 'Erro ao gerar PDF', 'detalhe': result.stderr}), 500

            return send_file(
                tmp_pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'conferencia-{modalidade}.pdf'
            )
        finally:
            for p in [tmp_json_path, tmp_py_path]:
                try: os.unlink(p)
                except: pass

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/historico-pdf', methods=['POST'])
def historico_pdf():
    try:
        body = request.get_json()
        if not body:
            return jsonify({'erro': 'Payload vazio'}), 400

        modalidade = body.get('modalidade', 'lotofacil')
        script_code = SCRIPTS.get('historico', '')

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w', encoding='utf-8') as tmp_json:
            json.dump(body, tmp_json, ensure_ascii=False)
            tmp_json_path = tmp_json.name

        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w', encoding='utf-8') as tmp_py:
            tmp_py.write(script_code)
            tmp_py_path = tmp_py.name

        tmp_pdf_path = tmp_json_path.replace('.json', '.pdf')

        try:
            result = subprocess.run(
                [sys.executable, tmp_py_path, tmp_json_path, tmp_pdf_path],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return jsonify({'erro': 'Erro ao gerar PDF', 'detalhe': result.stderr}), 500

            data_str = __import__('datetime').date.today().isoformat()
            return send_file(
                tmp_pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'relatorio-{modalidade}-{data_str}.pdf'
            )
        finally:
            for p in [tmp_json_path, tmp_py_path]:
                try: os.unlink(p)
                except: pass

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
