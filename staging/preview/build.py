#!/usr/bin/env python3
"""Vista previa de una etapa sobre el HTML real de producción.

Toma el snapshot (docs/auditoria/snapshot-*/html), aplica exactamente lo que se
va a cargar en WordPress —CSS del plugin codigo-calma, bloques de reemplazo,
correcciones.json y ajustes de página— y escribe staging/preview/build/<slug>.html.
Las capturas se sacan con staging/preview/capturas.js.

Uso: python3 staging/preview/build.py [etapa-1]
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SNAP = sorted((ROOT / 'docs/auditoria').glob('snapshot-*/html'))[-1]
ETAPA = sys.argv[1] if len(sys.argv) > 1 else 'etapa-1'
CONT = ROOT / 'contenido' / ETAPA
CHILD = ROOT / 'wp-content/plugins/codigo-calma/assets/css'
OUT = pathlib.Path(__file__).with_name('build')
OUT.mkdir(exist_ok=True)

log = []

def entry_bounds(s):
    a = s.index('<div class="entry-content single-content">')
    b = s.index('</div><!-- .entry-content -->', a)
    return a, b

def apply_correcciones(slug, s):
    data = json.loads((CONT / 'correcciones.json').read_text(encoding='utf-8'))
    for c in data['correcciones']:
        if c['tipo'] == 'categoria':
            continue
        if c['paginas'] != ['*'] and slug not in c['paginas']:
            continue
        find = c.get('html_buscar', c['antes'])
        repl = c.get('html_reemplazar', c['despues'])
        n = s.count(find)
        if not n:
            continue
        if 'encabezado' in c['tipo']:
            m_old = re.match(r'<(h[1-6]|p)\b', find)
            m_new = re.match(r'<(h[1-6]|p)\b', repl)
            i = s.index(find)
            s = s[:i] + repl + s[i + len(find):]
            old_tag, new_tag = m_old.group(1), m_new.group(1)
            if old_tag != new_tag and f'</{old_tag}>' not in find:
                # El editor cambia también la etiqueta de cierre del bloque.
                j = s.find(f'</{old_tag}>', i + len(repl))
                if j >= 0:
                    s = s[:j] + f'</{new_tag}>' + s[j + len(old_tag) + 3:]
        else:
            s = s.replace(find, repl)
        log.append(f'{slug}: {c["id"]} ×{n}')
    return s

def replace_home_timeline(s):
    i = s.index('<!DOCTYPE html>', s.index('entry-content'))
    j = s.index('</html>', i) + len('</html>')
    block = (CONT / 'bloques/inicio-linea-de-tiempo.html').read_text(encoding='utf-8')
    log.append('home: línea de tiempo reemplazada')
    return s[:i] + block + s[j:]

def replace_servicios(s):
    a, b = entry_bounds(s)
    block = (CONT / 'bloques/servicios.html').read_text(encoding='utf-8')
    head = '<div class="entry-content single-content">\n'
    s = s[:a] + head + block + '\n' + s[b:]
    # Ajuste de página: Kadence > Ancho completo + Sin caja + sin padding vertical
    s = re.sub(r'content-width-normal content-style-boxed content-vertical-padding-show',
               'content-width-fullwidth content-style-unboxed content-vertical-padding-hide', s, count=1)
    log.append('servicios: bloque reemplazado + página en ancho completo')
    return s

FORM_OLD_RE = re.compile(r'<div class="wp-block-kadence-advanced-form wp-block-kadence-advanced-form2625-cpt-id.*?</form>', re.S)

def replace_form(s):
    form = (CONT / 'bloques/formulario-contacto.preview.html').read_text(encoding='utf-8')
    s, n = FORM_OLD_RE.subn(lambda m: form, s, count=1)
    if n:
        log.append('contacto: formulario emulado con los ajustes del bloque')
    return s

def testimonios_title(s):
    a, _ = entry_bounds(s)
    s = s[:a] + '<header class="entry-header page-title title-align-inherit"><h1 class="entry-title">Testimonios</h1></header>\n' + s[a:]
    log.append('testimonios: título de página activado (H1)')
    return s

def blog_title(s):
    i = s.find('<ul id="archive-container"')
    if i >= 0:
        s = s[:i] + '<header class="calma-archive-header"><h1 class="calma-archive-title">Blog</h1></header>\n' + s[i:]
        log.append('blog: H1 del plugin codigo-calma')
    return s

def dequeue(s):
    s = re.sub(r"<link rel='stylesheet' id='otter-animation-css'[^>]*>\n?", '', s)
    s = re.sub(r'<script id="otter-[a-z-]+-js"[^>]*></script>\n?', '', s)
    s = re.sub(r'<style id="o-anim-hide-inline-css">.*?</style>\s*<noscript>.*?</noscript>', '', s, flags=re.S)
    s = re.sub(r"<link rel='stylesheet' id='contact-form-7-css'[^>]*>\n?", '', s)
    s = re.sub(r'<script id="(contact-form-7|swv)-js[a-z-]*"[^>]*>.*?</script>\n?', '', s, flags=re.S)
    return s

def inject_child(s):
    css = ''.join(f'<style id="calma-{n}-css">\n{(CHILD / f"calma-{n}.css").read_text(encoding="utf-8")}\n</style>\n'
                  for n in ('tokens', 'etapa1'))
    return s.replace('</head>', css + '</head>', 1)

SPECIAL = {
    'home': [replace_home_timeline],
    'servicios': [replace_servicios],
    'contacto': [replace_form],
    'testimonios': [testimonios_title],
    'blog': [blog_title],
}

for f in sorted(SNAP.glob('*.html')):
    slug = f.stem
    s = f.read_text(encoding='utf-8')
    for fn in SPECIAL.get(slug, []):
        s = fn(s)
    s = apply_correcciones(slug, s)
    s = dequeue(s)
    s = inject_child(s)
    (OUT / f.name).write_text(s, encoding='utf-8')

(OUT / 'build-log.txt').write_text('\n'.join(log) + '\n', encoding='utf-8')
print(f'{len(list(OUT.glob("*.html")))} páginas → {OUT} ({len(log)} cambios aplicados)')
