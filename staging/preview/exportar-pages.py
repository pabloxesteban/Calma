#!/usr/bin/env python3
"""Exporta la vista previa como sitio estático para GitHub Pages.

GitHub Pages publica este repositorio desde la raíz de la rama en
https://pabloxesteban.github.io/Calma/. Este script genera:
  - vista-previa/<ruta>/index.html para cada página de la vista previa
  - vista-previa/codigo-calma/assets/  (CSS, JS y fuentes del plugin)
  - index.html en la raíz que lleva a vista-previa/
  - .nojekyll
Los enlaces entre páginas de la vista previa quedan internos; el resto (y los
CSS, JS e imágenes de Kadence) se siguen cargando desde codigocalma.com.
Cada página lleva noindex, un aviso de "vista previa" y los formularios
desactivados (no envían nada al sitio real).

Uso: python3 staging/preview/exportar-pages.py   (construye antes la etapa 7)
"""
import pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BUILD = pathlib.Path(__file__).with_name('build')
OUT = ROOT / 'vista-previa'
BASE = '/Calma/vista-previa/'
PROD = 'https://codigocalma.com/'
PLUGIN_PROD = PROD + 'wp-content/plugins/codigo-calma/'

subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name('build.py')), 'etapa-7'], check=True)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'wp-content/plugins/codigo-calma/assets', OUT / 'codigo-calma/assets')

def ruta_de(slug):
    if slug == 'home':
        return ''
    for prefijo in ('equipo_', 'category_'):
        if slug.startswith(prefijo):
            return prefijo[:-1] + '/' + slug[len(prefijo):] + '/'
    return slug + '/'

# "sobre_tatiana" y "entradas" redirigen (a /equipo/tatiana-x-stacul/ y /blog/): no se exportan.
paginas = {ruta_de(f.stem): f for f in BUILD.glob('*.html') if f.stem not in ('sobre_tatiana', 'entradas')}
ALIAS = {'descargas/': 'descargas-2/', 'sobre_tatiana/': 'equipo/tatiana-x-stacul/', 'entradas/': 'blog/'}

AVISO = '''
<meta name="robots" content="noindex, nofollow">
<style>
.calma-preview-bar{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:100001;display:flex;gap:10px;align-items:center;
max-width:calc(100% - 32px);padding:10px 16px;border-radius:999px;background:rgba(22,33,77,.92);color:#fff;font:600 13px/1.3 Inter,system-ui,sans-serif;
box-shadow:0 10px 30px -10px rgba(0,0,0,.45);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.calma-preview-bar a{color:#dad4f6;text-decoration:underline}
.calma-preview-note{margin:12px 0 0;padding:10px 14px;border-radius:10px;background:#fff4d6;color:#6b4a00;font-size:14px}
@media print{.calma-preview-bar{display:none}}
</style>
'''
SCRIPT = '''
<div class="calma-preview-bar" role="note">Vista previa del rediseño · no es el sitio publicado</div>
<script>
/* Vista previa: los formularios no envían nada al sitio real. */
document.addEventListener('submit', function (e) {
  var f = e.target;
  if (f.matches('.search-form, [role=search]')) { return; }
  e.preventDefault(); e.stopImmediatePropagation();
  if (!f.querySelector('.calma-preview-note')) {
    var p = document.createElement('p'); p.className = 'calma-preview-note'; p.setAttribute('role', 'status');
    p.textContent = 'Esto es una vista previa: el formulario no envía mensajes.';
    f.appendChild(p);
  }
}, true);
</script>
'''

def reescribir(html):
    html = html.replace(PLUGIN_PROD, BASE + 'codigo-calma/')

    def enlace(m):
        attr, url = m.group(1), m.group(2)
        resto = url[len(PROD):]
        m2 = re.match(r'([^?#]*)(.*)', resto)
        ruta, sep, extra = m2.group(1), m2.group(2), ''
        ruta = ruta if (ruta == '' or ruta.endswith('/')) else ruta + '/'
        ruta = ALIAS.get(ruta, ruta)
        if ruta in paginas:
            return f'{attr}="{BASE}{ruta}{sep}{extra}"'
        return m.group(0)

    html = re.sub(r'(href)="(https://codigocalma\.com/[^"]*)"', enlace, html)
    html = html.replace('<head>', '<head>' + AVISO, 1) if '<head>' in html else re.sub(r'(<head[^>]*>)', r'\1' + AVISO, html, count=1)
    html = html.replace('</body>', SCRIPT + '</body>', 1)
    return html

for ruta, f in paginas.items():
    destino = OUT / ruta / 'index.html'
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(reescribir(f.read_text(encoding='utf-8')), encoding='utf-8')

(ROOT / 'index.html').write_text('''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Código Calma · vista previa del rediseño</title>
<meta http-equiv="refresh" content="0; url=/Calma/vista-previa/">
<link rel="canonical" href="https://codigocalma.com/"></head>
<body><p><a href="/Calma/vista-previa/">Ir a la vista previa del rediseño de Código Calma</a></p></body></html>
''', encoding='utf-8')
(ROOT / '.nojekyll').write_text('', encoding='utf-8')
print(f'{len(paginas)} páginas exportadas en {OUT.relative_to(ROOT)}/ → https://pabloxesteban.github.io{BASE}')
