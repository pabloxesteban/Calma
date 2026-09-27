#!/usr/bin/env python3
"""Vista previa acumulativa de las etapas sobre el HTML real de producción.

Toma el snapshot (docs/auditoria/snapshot-*/html) y aplica, en orden, lo que se
va a cargar en WordPress en cada etapa hasta la indicada: CSS del plugin
codigo-calma, bloques de reemplazo, correcciones.json y ajustes que se hacen en
el editor o el Personalizador (emulados). Escribe staging/preview/build/<slug>.html.
Las capturas se sacan con staging/preview/capturas.js.

Uso: python3 staging/preview/build.py [etapa-1|etapa-2|etapa-3|etapa-5]  (la Etapa 4 no cambia el HTML visible)
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SNAP = sorted((ROOT / 'docs/auditoria').glob('snapshot-*/html'))[-1]
HASTA = int((sys.argv[1] if len(sys.argv) > 1 else 'etapa-5').split('-')[-1])
PLUGIN = ROOT / 'wp-content/plugins/codigo-calma'
CSS = PLUGIN / 'assets/css'
OUT = pathlib.Path(__file__).with_name('build')
OUT.mkdir(exist_ok=True)
PLUGIN_URL = 'https://codigocalma.com/wp-content/plugins/codigo-calma/'

log = []

def cont(etapa):
    return ROOT / 'contenido' / f'etapa-{etapa}'

def entry_bounds(s):
    a = s.index('<div class="entry-content single-content">')
    b = s.index('</div><!-- .entry-content -->', a)
    return a, b

# ---------------------------------------------------------------- correcciones
def apply_correcciones(etapa, slug, s):
    f = cont(etapa) / 'correcciones.json'
    if not f.exists():
        return s
    for c in json.loads(f.read_text(encoding='utf-8'))['correcciones']:
        if c['tipo'] in ('categoria', 'nota'):
            continue
        if c['paginas'] != ['*'] and slug not in c['paginas']:
            continue
        find = c.get('html_buscar', c['antes'])
        repl = c.get('html_reemplazar', c['despues'])
        n = s.count(find)
        if not n:
            continue
        if 'encabezado' in c['tipo']:
            old_tag = re.match(r'<(h[1-6]|p)\b', find).group(1)
            new_tag = re.match(r'<(h[1-6]|p)\b', repl).group(1)
            for _ in range(n if c.get('nota') == 'todas' else 1):
                i = s.index(find)
                s = s[:i] + repl + s[i + len(find):]
                if old_tag != new_tag and f'</{old_tag}>' not in find:
                    # El editor cambia también la etiqueta de cierre del bloque.
                    j = s.find(f'</{old_tag}>', i + len(repl))
                    if j >= 0:
                        s = s[:j] + f'</{new_tag}>' + s[j + len(old_tag) + 3:]
        else:
            s = s.replace(find, repl)
        log.append(f'{slug}: E{etapa} {c["id"]} ×{n}')
    return s

# ---------------------------------------------------------------- Etapa 1
def e1_home_timeline(s):
    i = s.index('<!DOCTYPE html>', s.index('entry-content'))
    j = s.index('</html>', i) + len('</html>')
    log.append('home: línea de tiempo reemplazada')
    return s[:i] + (cont(1) / 'bloques/inicio-linea-de-tiempo.html').read_text(encoding='utf-8') + s[j:]

def e1_servicios(s):
    a, b = entry_bounds(s)
    block = (cont(1) / 'bloques/servicios.html').read_text(encoding='utf-8')
    s = s[:a] + '<div class="entry-content single-content">\n' + block + '\n' + s[b:]
    # Ajuste de página: Kadence > Ancho completo + Sin caja + sin padding vertical
    s = s.replace('content-width-normal content-style-boxed content-vertical-padding-show',
                  'content-width-fullwidth content-style-unboxed content-vertical-padding-hide', 1)
    log.append('servicios: bloque reemplazado + página en ancho completo')
    return s

FORM_RE = re.compile(r'<div class="wp-block-kadence-advanced-form wp-block-kadence-advanced-form2625-cpt-id.*?</form>', re.S)

def e1_form(s):
    form = (cont(1) / 'bloques/formulario-contacto.preview.html').read_text(encoding='utf-8')
    s, n = FORM_RE.subn(lambda m: form, s, count=1)
    if n:
        log.append('contacto: formulario emulado')
    return s

def e1_testimonios(s):
    a, _ = entry_bounds(s)
    log.append('testimonios: título de página (H1)')
    return s[:a] + '<header class="entry-header page-title"><h1 class="entry-title">Testimonios</h1></header>\n' + s[a:]

def e1_blog(s):
    i = s.find('<ul id="archive-container"')
    if i >= 0:
        log.append('blog: H1 del plugin')
        s = s[:i] + '<header class="calma-archive-header"><h1 class="calma-archive-title">Blog</h1></header>\n' + s[i:]
    return s

def e1_global(s):
    # Lo que el plugin deja de cargar: Blocks Animation y Contact Form 7.
    s = re.sub(r"<link rel='stylesheet' id='otter-animation-css'[^>]*>\n?", '', s)
    s = re.sub(r'<script id="otter-[a-z-]+-js"[^>]*></script>\n?', '', s)
    s = re.sub(r'<style id="o-anim-hide-inline-css">.*?</style>\s*<noscript>.*?</noscript>', '', s, flags=re.S)
    s = re.sub(r"<link rel='stylesheet' id='contact-form-7-css'[^>]*>\n?", '', s)
    s = re.sub(r'<script id="(contact-form-7|swv)-js[a-z-]*"[^>]*>.*?</script>\n?', '', s, flags=re.S)
    return s

# ---------------------------------------------------------------- Etapa 2
MENU_MOBILE = [('Inicio', ''), ('Ciberpsicología', 'ciberpsicologia/'), ('Bienestar digital', 'bienestar-digital/'),
               ('Blog', 'blog/'), ('Herramientas', 'herramientas/'), ('Test de consumo digital', 'test/'),
               ('Descargas', 'descargas-2/'), ('Servicios', 'servicios/'),
               ('Equipo', 'equipo/') if HASTA >= 3 else ('Sobre Tatiana', 'sobre_tatiana/'), ('Contacto', 'contacto/')]

def e2_global(slug, s):
    # Plugin: sin Google Fonts de Kadence + preload de las fuentes locales.
    s = re.sub(r"<link rel='stylesheet' id='kadence-fonts-gfonts-css'[^>]*>\n?", '', s)
    pre = ''.join(f'<link rel="preload" href="{PLUGIN_URL}assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n'
                  for f in ('inter-latin-wght-normal.woff2', 'lora-latin-wght-normal.woff2'))
    s = s.replace('<meta name="viewport"', pre + '<meta name="viewport"', 1)
    # Plugin: sizes="48px" en el logo.
    s = s.replace('sizes="(max-width: 512px) 100vw, 512px" />', 'sizes="48px" />')
    # Personalizador: botón en el header de escritorio.
    btn = ('<div class="site-header-item site-header-focus-item" data-section="kadence_customizer_header_button">'
           '<div class="header-button-wrap"><div class="header-button-inner-wrap">'
           '<a href="https://codigocalma.com/contacto/" class="button header-button button-size-medium button-style-filled">'
           'Solicitar una consulta</a></div></div></div>')
    s = s.replace('</div><!-- data-section="header_search" -->', '</div><!-- data-section="header_search" -->' + btn, 1)
    # Menús: menú mobile plano (sin submenú) + botón al final del drawer.
    cur = '' if slug == 'home' else slug + '/'
    items = ''
    for name, url in MENU_MOBILE:
        actual = url == cur
        items += ('<li class="menu-item' + (' current-menu-item' if actual else '') + '">'
                  '<a href="https://codigocalma.com/' + url + '"' + (' aria-current="page"' if actual else '') + '>' + name + '</a></li>')
    s, n = re.subn(r'(<ul id="mobile-menu" class="menu[^"]*">).*?(</ul>\s*</div>\s*</nav>)',
                   lambda m: m.group(1) + items + m.group(2), s, count=1, flags=re.S)
    mbtn = ('<div class="mobile-header-button-wrap"><div class="mobile-header-button-inner-wrap">'
            '<a href="https://codigocalma.com/contacto/" class="button mobile-header-button button-size-medium button-style-filled">'
            'Solicitar una consulta</a></div></div>')
    s = s.replace('</div><!-- data-section="mobile_navigation" -->', '</div><!-- data-section="mobile_navigation" -->' + mbtn, 1)
    # Widgets: pie de página en 4 columnas.
    pie = (cont(2) / 'footer/pie-widget.html').read_text(encoding='utf-8')
    pie = re.sub(r'<!--.*?-->\s*', '', pie, count=1, flags=re.S)
    footer = ('<footer id="colophon" class="site-footer" role="contentinfo"><div class="site-footer-wrap">'
              '<div class="site-middle-footer-wrap site-footer-row-container"><div class="site-footer-row-container-inner">'
              '<div class="site-container"><div class="footer-widget-area widget-area site-footer-focus-item footer-widget1">'
              '<section class="widget widget_block">' + pie + '</section></div></div></div></div></div></footer>')
    s = re.sub(r'<footer id="colophon".*?</footer>', lambda m: footer, s, count=1, flags=re.S)
    return s

def e2_herramientas(s):
    i = s.index('<!-- ═══')
    j = s.index('</script>', s.index('id="ccSlider"')) + len('</script>')
    log.append('herramientas: bloque "Pequeños hábitos" reemplazado')
    return s[:i] + (cont(2) / 'bloques/herramientas-habitos.html').read_text(encoding='utf-8') + s[j:]

def e2_test(s):
    f = cont(2) / 'bloques/test-consumo-digital.html'
    if not f.exists():
        return s
    a, _ = entry_bounds(s)
    i = s.index('<style data-wp-block-html="css">', a)
    # El bloque HTML personalizado original = <style> + <script> + marcado de las
    # pantallas (#screen-0…), hasta el cierre de la columna/fila de Kadence que lo contiene.
    j = s.index('</div></div>\n\n</div></div>', s.index('id="screen-0"'))
    log.append('test: bloque accesible reemplazado')
    return s[:i] + f.read_text(encoding='utf-8') + s[j:]

# ---------------------------------------------------------------- Etapa 3
import subprocess

def div_balanceado(s, inicio):
    # Devuelve el índice de cierre del <div> que empieza en `inicio`.
    prof, i = 0, inicio
    for m in re.finditer(r'<div\b|</div>', s[inicio:]):
        prof += 1 if m.group(0) != '</div>' else -1
        if prof == 0:
            return inicio + m.end()
    raise ValueError('div sin cerrar')

def e3_home(s):
    a = s.index('<div class="kb-row-layout-wrap kb-row-layout-id1204_494dce-76')
    b = div_balanceado(s, a)
    log.append('home: hero nuevo')
    return s[:a] + (cont(3) / 'bloques/inicio-hero.html').read_text(encoding='utf-8') + s[b:]

def e3_servicios(s):
    a, b = entry_bounds(s)
    log.append('servicios: página de conversión')
    return s[:a] + '<div class="entry-content single-content">\n' + (cont(3) / 'bloques/servicios.html').read_text(encoding='utf-8') + '\n' + s[b:]

def e3_contacto(s):
    i = s.index('<h1 class="kt-adv-heading790_ebf638-02')
    j = s.index('<div class="wp-block-kadence-advanced-form', i)
    s = s[:i] + (cont(3) / 'bloques/contacto-intro.html').read_text(encoding='utf-8') + s[j:]
    form = (cont(3) / 'bloques/formulario-contacto.preview.html').read_text(encoding='utf-8')
    s = FORM_RE.sub(lambda m: form, s, count=1)
    log.append('contacto: intro + qué pasa después + campo de área')
    return s

CTAS = None
def e3_articulo(slug, s):
    # Con la Etapa 5, el mismo renderizador PHP agrega "En resumen" y "Fuentes".
    global CTAS
    if CTAS is None:
        args = ['php', str(pathlib.Path(__file__).with_name('php') / 'render-cta.php')] + (['--geo'] if HASTA >= 5 else [])
        CTAS = json.loads(subprocess.run(args, capture_output=True, text=True, check=True).stdout)
    if slug not in CTAS:
        return s
    a, b = entry_bounds(s)
    inicio = a + len('<div class="entry-content single-content">')
    s = s[:b] + CTAS[slug]['despues'] + s[b:]
    s = s[:inicio] + CTAS[slug]['antes'] + s[inicio:]
    log.append(f'{slug}: caja de consulta' + (' + resumen/fuentes' if HASTA >= 5 else ''))
    return s

# ---------------------------------------------------------------- Etapa 5
def e5_h2(slug, s):
    data = json.loads((cont(5) / 'articulos.json').read_text(encoding='utf-8'))
    art = next((x for x in data['articulos'] if x['slug'] == slug), None)
    if not art:
        return s
    for h in art.get('h2', []):
        de = h.get('nivel_actual', 'h3')
        pat = re.compile(r'<' + de + r'( class="wp-block-heading[^"]*")>(.*?)</' + de + '>', re.S)
        def cambiar(m):
            plano = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            import html as _h
            return '<h2' + m.group(1) + '>' + m.group(2) + '</h2>' if _h.unescape(plano) == h['antes'].strip() else m.group(0)
        s = pat.sub(cambiar, s)
    log.append(f'{slug}: encabezados de sección a H2')
    return s

def e5_pilar(s):
    a, b = entry_bounds(s)
    s = s[:a] + '<div class="entry-content single-content">\n' + (cont(5) / 'bloques/ciberpsicologia.html').read_text(encoding='utf-8') + '\n' + s[b:]
    s = s.replace('content-width-normal content-style-boxed content-vertical-padding-show', 'content-width-fullwidth content-style-unboxed content-vertical-padding-hide', 1)
    log.append('ciberpsicologia: página pilar')
    return s

def e5_bienestar(s):
    ap = (cont(5) / 'bloques/bienestar-digital-apertura.html').read_text(encoding='utf-8')
    i = s.index('El bienestar digital emerge cuando')
    i = s.rindex('<p', 0, i)
    j = s.index('</p>', s.index('Es usar los dispositivos con intención', i)) + 4
    log.append('bienestar-digital: apertura con definición')
    return s[:i] + ap + s[j:]

EQUIPO = {'equipo': ('El equipo', 'equipo.html'), 'equipo_tatiana-x-stacul': ('Tatiana X. Stacul', 'equipo-tatiana-x-stacul.html'),
          'equipo_francisca-cortes-santoro': ('Francisca Cortés Santoro', 'equipo-francisca-cortes-santoro.html'),
          'equipo_emanuel-c-franco': ('Emanuel C. Franco', 'equipo-emanuel-c-franco.html')}

def e3_menus(slug, s):
    # Menús: "Sobre Tatiana" → "Equipo" (activo en las páginas de equipo).
    s = re.sub(r'<a href="https://codigocalma.com/sobre_tatiana/"( aria-current="page")?>Sobre Tatiana</a>',
               lambda m: '<a href="https://codigocalma.com/equipo/"' + (' aria-current="page"' if slug.startswith('equipo') else '') + '>Equipo</a>', s)
    return s

# ---------------------------------------------------------------- CSS del plugin
def inject_css(s):
    files = ['calma-tokens', 'calma-etapa1'] + (['calma-fonts', 'calma-etapa2'] if HASTA >= 2 else []) + (['calma-etapa3'] if HASTA >= 3 else [])
    css = ''
    for n in files:
        txt = (CSS / f'{n}.css').read_text(encoding='utf-8')
        txt = txt.replace('url(../fonts/', f'url({PLUGIN_URL}assets/fonts/')
        css += f'<style id="{n}-css">\n{txt}\n</style>\n'
    s = s.replace('</head>', css + '</head>', 1)
    if HASTA >= 3:
        # El plugin encola calma-conversion.js (defer, en el pie).
        s = s.replace('</body>', f'<script src="{PLUGIN_URL}assets/js/calma-conversion.js" defer></script>\n</body>', 1)
    return s

E1 = {'home': [e1_home_timeline], 'servicios': [e1_servicios], 'contacto': [e1_form],
      'testimonios': [e1_testimonios], 'blog': [e1_blog]}
E2 = {'herramientas': [e2_herramientas], 'test': [e2_test]}

E3 = {'home': [e3_home], 'servicios': [e3_servicios], 'contacto': [e3_contacto]}
POSTS = {p['slug'] for p in json.loads((SNAP.parent / 'api/posts.json').read_text(encoding='utf-8'))}

def fuentes():
    for f in sorted(SNAP.glob('*.html')):
        yield f.stem, f.read_text(encoding='utf-8')
    if HASTA >= 3:
        base = (SNAP / 'sobre_tatiana.html').read_text(encoding='utf-8')
        for slug, (titulo, bloque) in EQUIPO.items():
            s = base.replace('Sobre Tatiana – Código Calma', titulo + ' – Código Calma')
            s = s.replace('content-width-normal content-style-boxed content-vertical-padding-show',
                          'content-width-fullwidth content-style-unboxed content-vertical-padding-hide')
            a, b = entry_bounds(s)
            s = s[:a] + '<div class="entry-content single-content">\n' + (cont(3) / 'bloques' / bloque).read_text(encoding='utf-8') + '\n' + s[b:]
            log.append(f'{slug}: página nueva')
            yield slug, s

for slug, s in fuentes():
    for fn in E1.get(slug, []):
        s = fn(s)
    s = apply_correcciones(1, slug, s)
    s = e1_global(s)
    if HASTA >= 2:
        for fn in E2.get(slug, []):
            s = fn(s)
        s = apply_correcciones(2, slug, s)
        if HASTA >= 3:
            for fn in E3.get(slug, []):
                s = fn(s)
            if slug in POSTS:
                s = e3_articulo(slug, s)
            s = apply_correcciones(3, slug, s)
        if HASTA >= 5:
            if slug in POSTS:
                s = e5_h2(slug, s)
            if slug == 'ciberpsicologia':
                s = e5_pilar(s)
            if slug == 'bienestar-digital':
                s = e5_bienestar(s)
        s = e2_global(slug, s)
        if HASTA >= 3:
            s = e3_menus(slug, s)
    s = inject_css(s)
    (OUT / f'{slug}.html').write_text(s, encoding='utf-8')

(OUT / 'build-log.txt').write_text('\n'.join(log) + '\n', encoding='utf-8')
print(f'etapa ≤ {HASTA}: {len(list(OUT.glob("*.html")))} páginas → {OUT} ({len(log)} cambios)')
