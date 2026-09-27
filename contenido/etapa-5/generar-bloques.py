#!/usr/bin/env python3
"""Convierte el copy de la Etapa 5 (Markdown) en bloques "HTML personalizado".
- pilar-ciberpsicologia.md  -> bloques/ciberpsicologia.html (reemplaza /ciberpsicologia/)
- bienestar-digital-apertura.md -> bloques/bienestar-digital-apertura.html
Los [COMPLETAR: …] quedan visibles; los [verificar: …] se convierten en
comentarios HTML (notas editoriales, no huecos de datos). Ejecutar:
python3 contenido/etapa-5/generar-bloques.py  (requiere `pip install markdown`)"""
import pathlib, re
import markdown

DIR = pathlib.Path(__file__).parent
OUT = DIR / 'bloques'
OUT.mkdir(exist_ok=True)
SITE = 'https://codigocalma.com'

def md_a_html(texto):
    lineas = []
    for l in texto.splitlines():
        if re.match(r'^## Bloque \d+', l) or l.strip() == '---':
            continue
        if re.match(r'^\[verificar:.*\]\s*$', l.strip()):
            lineas.append('<!-- ' + l.strip().replace('--', '—') + ' -->')
            continue
        lineas.append(l)
    html = markdown.markdown('\n'.join(lineas), extensions=['extra', 'sane_lists'])
    html = re.sub(r'\[COMPLETAR:([^\]]*)\]', r'<span class="calma-placeholder">[COMPLETAR:\1]</span>', html)
    html = re.sub(r'\[verificar:([^\]]*)\]', r'<!-- verificar:\1 -->', html)
    html = re.sub(r'href="/(?!/)', f'href="{SITE}/', html)
    # Las tablas se desplazan en horizontal en pantallas angostas: que se puedan
    # recorrer con el teclado (WCAG 2.1.1, axe scrollable-region-focusable).
    html = html.replace('<table>', '<table tabindex="0">')
    return html

def cabecera(titulo, instrucciones):
    return (f'<!-- Código Calma · {titulo} (Etapa 5)\n     {instrucciones}\n'
            '     Texto pendiente de revisión de Tatiana X. Stacul. Estilos: plugin codigo-calma. -->\n')

# ---------------------------------------------------------------- Pilar
src = (DIR / 'pilar-ciberpsicologia.md').read_text(encoding='utf-8')
cuerpo = src[src.index('# ¿Qué es la ciberpsicología?'):]
cuerpo = cuerpo[:cuerpo.index('### Placeholders')] if '### Placeholders' in cuerpo else cuerpo
html = md_a_html(cuerpo)
# Definición (primera oración en negrita) y "En resumen" como caja citable.
html = re.sub(r'<p><strong>(La ciberpsicología es .*?)</strong></p>', r'<p class="calma-definicion"><strong>\1</strong></p>', html, count=1)
html = re.sub(r'<p><strong>En resumen:</strong>(.*?)</p>', r'<aside class="calma-resumen" aria-label="En resumen"><p><strong>En resumen:</strong>\1</p></aside>', html, count=1, flags=re.S)
html = html.replace('<h3>¿Quieres trabajarlo uno a uno?</h3>', '<h2>¿Quieres trabajarlo uno a uno?</h2>')
bloque = cabecera('Página pilar ¿Qué es la ciberpsicología?', 'Reemplaza TODO el contenido de la página Ciberpsicología (/ciberpsicologia/). Un bloque "HTML personalizado". Ancho completo, sin caja, título de Kadence oculto (el H1 está aquí).')
bloque += '<div class="calma-page calma-pilar">\n<article class="calma-section calma-section--white"><div class="calma-container--text calma-prosa">\n' + html + '\n</div></article>\n</div>\n'
(OUT / 'ciberpsicologia.html').write_text(bloque, encoding='utf-8')

# ---------------------------------------------------------------- Bienestar digital
src = (DIR / 'bienestar-digital-apertura.md').read_text(encoding='utf-8')
cuerpo = src[src.index('**El bienestar digital es'):]
cuerpo = cuerpo.split('\n---')[0]
html = md_a_html(cuerpo)
html = re.sub(r'<p><strong>(El bienestar digital es .*?)</strong></p>', r'<p class="calma-definicion"><strong>\1</strong></p>', html, count=1)
html = re.sub(r'<p><strong>En resumen:</strong>(.*?)</p>', r'<aside class="calma-resumen" aria-label="En resumen"><p><strong>En resumen:</strong>\1</p></aside>', html, count=1, flags=re.S)
bloque = cabecera('Bienestar digital · apertura', 'Va justo debajo del H1 "Bienestar Digital" y reemplaza los dos párrafos "El bienestar digital emerge cuando…" y "Es usar los dispositivos con intención…". Bloque "HTML personalizado".')
bloque += '<div class="calma-page calma-prosa calma-apertura">\n' + html + '\n</div>\n'
(OUT / 'bienestar-digital-apertura.html').write_text(bloque, encoding='utf-8')
print('ok:', [p.name for p in OUT.glob('*.html')])
