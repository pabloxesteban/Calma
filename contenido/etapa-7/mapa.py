"""Mapa de temas del Inicio: la ciberpsicología en el centro y cinco temas
alrededor. Los artículos de cada tema y las conexiones entre temas salen de la
taxonomía real (contenido/etapa-5/taxonomia.json): dos temas se unen por las
etiquetas que comparten sus artículos. Lo usa generar-bloques.py.

Sin JavaScript se ve la lista completa de temas con sus artículos; con JS,
calma-organismo.js la convierte en un mapa interactivo (un tema por vez).
"""
import itertools
import json
import math
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
C = 'https://codigocalma.com'

# Títulos de las entradas tal como se publican (con las correcciones de las etapas 1–5).
TITULOS = {
    'por-que-tu-fuerza-de-voluntad-es-mas-lista-de-lo-que-crees': 'Por qué tu fuerza de voluntad es más lista de lo que crees',
    'la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia': 'La diferencia entre «querer» y «ser capaz»: entendiendo la autoeficacia',
    'por-que-fallamos-al-intentar-cambiar-conductas': '¿Por qué fallamos al intentar cambiar conductas?',
    'descubriendo-que-modela-nuestro-comportamiento': '¿Qué modela nuestro comportamiento?',
    'el-arte-de-redisenar-tu-entorno': 'El arte de rediseñar tu entorno',
    'ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva': 'IA y apoyo emocional: saber la autoría cambia tu perspectiva',
    'el-estigma-de-la-estructura-x-entonces-y': 'El estigma de la estructura: «X entonces Y»',
    'reflexiones-eticas-sobre-el-desarrollo-de-la-inteligencia-artificial': 'Reflexiones éticas sobre el desarrollo de la inteligencia artificial',
    'infancias-figitales': 'Infancias «Figitales»',
    'calidad-vs-cantidad-la-hipotesis-de-ricitos-de-oro': 'Calidad vs. cantidad: la hipótesis de Ricitos de Oro',
    'autoevaluacion-del-consumo-digital-como-estamos-manejando-nuestro-tiempo-frente-a-las-pantallas': 'Autoevaluación del consumo digital: ¿cómo estamos manejando nuestro tiempo frente a las pantallas?',
    'la-tecnologia-te-supera-como-identificar-y-gestionar-el-tecnoestres': 'La tecnología te supera: cómo identificar y gestionar el tecnoestrés',
    'preguntas-clave-para-entender-y-cuidar-nuestro-cerebro': 'Preguntas clave para entender y cuidar nuestro cerebro',
    '5-puntos-clave-que-el-caso-de-meta-nos-deja-en-salud-mental': '5 puntos clave que el caso de Meta nos deja en salud mental',
    'como-un-te-quiero-infecto-45-millones-de-computadoras-en-todo-el-mundo': 'Cómo un «te quiero» infectó 45 millones de computadoras en todo el mundo',
}

# Los seis temas del mapa y su relación con las categorías del blog (Etapa 5).
# Descripciones: resumen de las descripciones de categoría de taxonomia.json
# (pendientes de validación de la autora, como esas descripciones).
TEMAS = [
    dict(k='ciberpsicologia', nombre='Ciberpsicología', sub='El centro', categorias=[],
         texto='El campo de la psicología que estudia la mente y el comportamiento humanos en su interacción con la tecnología. Cruza todos los temas del mapa.',
         enlaces=[('¿Qué es la ciberpsicología?', f'{C}/ciberpsicologia/'), ('Todos los artículos', f'{C}/blog/')]),
    dict(k='psicologia', nombre='Psicología', sub='Hábitos y conducta', categorias=['habitos-y-conducta'],
         texto='Por qué repetimos ciertos gestos con la tecnología, qué papel tiene el entorno y por qué la fuerza de voluntad no lo explica todo.',
         enlaces=[('Ver Hábitos y conducta', f'{C}/category/habitos-y-conducta/')]),
    dict(k='neurociencia', nombre='Neurociencia', sub='Neurociencia y atención', categorias=['neurociencia'],
         texto='El cerebro en la vida digital: cómo funciona la atención, qué la fragmenta y cómo se relacionan el descanso y la carga cognitiva con las pantallas.',
         enlaces=[('Ver Neurociencia y atención', f'{C}/category/neurociencia/')]),
    dict(k='ia', nombre='IA', sub='IA y mente', categorias=['ia-y-mente'],
         texto='Cómo pensamos, sentimos y confiamos cuando la inteligencia artificial entra en la conversación, y las preguntas éticas que abre.',
         enlaces=[('Ver IA y mente', f'{C}/category/ia-y-mente/')]),
    dict(k='tecnologia', nombre='Tecnología', sub='Plataformas y ciberseguridad', categorias=['redes-sociales', 'ciberseguridad'],
         texto='Cómo influyen las plataformas y sus algoritmos en lo que ves y sientes, y por qué confiamos en un mensaje que no deberíamos abrir.',
         enlaces=[('Ver Redes sociales y plataformas', f'{C}/category/redes-sociales/'), ('Ver Ciberseguridad y factor humano', f'{C}/category/ciberseguridad/')]),
    dict(k='bienestar', nombre='Bienestar digital', sub='Bienestar digital', categorias=['bienestar'],
         texto='Convivir con las pantallas sin que te desborden: el tiempo y la calidad de uso, el tecnoestrés y la vida digital de niñas, niños y adolescentes.',
         enlaces=[('Ver Bienestar digital', f'{C}/bienestar-digital/')]),
]


def datos():
    tax = json.loads((RAIZ / 'contenido/etapa-5/taxonomia.json').read_text(encoding='utf-8'))
    etiquetas = {e['slug']: e['nombre'] for e in tax['etiquetas']}
    for t in TEMAS:
        t['articulos'] = [a['slug_entrada'] for a in tax['asignacion'] if a['categoria'] in t['categorias']]
        t['etiquetas'] = set(e for a in tax['asignacion'] if a['categoria'] in t['categorias'] for e in a['etiquetas'])
    # Posiciones: la ciberpsicología en el centro, el resto en un pentágono.
    TEMAS[0]['x'], TEMAS[0]['y'] = 50, 50
    for i, t in enumerate(TEMAS[1:]):
        ang = math.radians(-90 + i * 72)
        t['x'], t['y'] = round(50 + 37 * math.cos(ang), 1), round(50 + 37 * math.sin(ang), 1)
    aristas = []
    for t in TEMAS[1:]:
        aristas.append((TEMAS[0], t, []))
    for a, b in itertools.combinations(TEMAS[1:], 2):
        comun = sorted(etiquetas[e] for e in a['etiquetas'] & b['etiquetas'])
        if comun:
            aristas.append((a, b, comun))
    return aristas


def curva(a, b):
    # Las uniones entre temas del borde se curvan hacia el centro.
    if a['k'] == 'ciberpsicologia':
        return f'M{a["x"]} {a["y"]} L{b["x"]} {b["y"]}'
    mx, my = (a['x'] + b['x']) / 2, (a['y'] + b['y']) / 2
    cx, cy = mx + (50 - mx) * 0.35, my + (50 - my) * 0.35
    return f'M{a["x"]} {a["y"]} Q{cx:.1f} {cy:.1f} {b["x"]} {b["y"]}'


def mapa(cabecera):
    aristas = datos()
    # Cada unión tiene dos trazos: la línea y, encima, la señal que la recorre.
    lineas = ''.join(
        f'<path class="calma-mapa__arista" data-a="{a["k"]}" data-b="{b["k"]}" style="--i:{n};--peso:{max(1, len(c))}" pathLength="1" d="{curva(a, b)}"/>'
        f'<path class="calma-mapa__senal" data-a="{a["k"]}" data-b="{b["k"]}" pathLength="1" d="{curva(a, b)}"/>'
        for n, (a, b, c) in enumerate(aristas))
    nodos = ''.join(
        f'<button type="button" class="calma-mapa__nodo{" calma-mapa__nodo--centro" if t["k"] == "ciberpsicologia" else ""}" '
        f'style="--x:{t["x"]};--y:{t["y"]}" data-tema="{t["k"]}" aria-controls="tema-{t["k"]}" aria-pressed="false">'
        f'<span class="calma-mapa__punto" aria-hidden="true"></span><span class="calma-mapa__nombre">{t["nombre"]}</span></button>'
        for t in TEMAS)
    paneles = ''
    for t in TEMAS:
        conecta = []
        for a, b, comun in aristas:
            if not comun or t['k'] not in (a['k'], b['k']):
                continue
            otro = b if a['k'] == t['k'] else a
            conecta.append((len(comun), f'<li><strong>{otro["nombre"]}</strong>: {", ".join(comun[:3]).lower().capitalize()}</li>'))
        conecta = [c for _, c in sorted(conecta, key=lambda x: -x[0])][:3]
        arts = ''.join(f'<li><a href="{C}/{s}/">{TITULOS[s]}</a></li>' for s in t['articulos'])
        enlaces = ''.join(f'<a class="calma-link" href="{h}">{txt}</a>' for txt, h in t['enlaces'])
        paneles += (
            f'<article class="calma-mapa__panel" id="tema-{t["k"]}" data-tema="{t["k"]}" aria-labelledby="tema-{t["k"]}-titulo">\n'
            f'<h3 id="tema-{t["k"]}-titulo">{t["nombre"]}'
            + (f' <span class="calma-mapa__sub">· {t["sub"]}</span>' if t['sub'] != t['nombre'] and t['k'] != 'ciberpsicologia' else '')
            + f'</h3>\n<p class="calma-mapa__texto">{t["texto"]}</p>\n'
            + (f'<p class="calma-mapa__rotulo">Artículos</p><ul class="calma-mapa__articulos">{arts}</ul>\n' if arts else '')
            + (f'<p class="calma-mapa__rotulo">Se conecta con</p><ul class="calma-mapa__conexiones">{"".join(conecta)}</ul>\n' if conecta else '')
            + f'<p class="calma-mapa__enlaces">{enlaces}</p>\n</article>\n')
    return (cabecera('Inicio · mapa de temas',
                     'Va entre "¿Cómo son tus momentos con la tecnología?" y los accesos. Bloque "HTML personalizado" a ancho completo.\n'
                     '     Artículos y conexiones salen de contenido/etapa-5/taxonomia.json. Los enlaces a categorías nuevas funcionan después de la Etapa 5 (Paso 2).')
            + '<section class="calma-mapa" aria-labelledby="mapa-titulo">\n<div class="calma-mapa__head">\n'
            '<h2 id="mapa-titulo">Explora por <em>temas</em></h2>\n'
            '<p class="calma-sub">La ciberpsicología está en el centro: cruza la psicología con la tecnología. Elige un tema para ver sus artículos y con qué se conecta.</p>\n'
            '</div>\n<div class="calma-mapa__cuerpo">\n'
            f'<div class="calma-mapa__grafo" hidden>\n<svg class="calma-mapa__svg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true" focusable="false">{lineas}</svg>\n'
            f'<div class="calma-mapa__nodos" role="group" aria-label="Temas del mapa">{nodos}</div>\n</div>\n'
            f'<div class="calma-mapa__paneles" aria-live="polite">\n{paneles}</div>\n</div>\n</section>\n')
