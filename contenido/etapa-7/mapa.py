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


def exportar():
    """Escribe wp-content/plugins/codigo-calma/data/mapa-temas.json, que usa
    includes/mapa.php para el mapa de temas ([calma_mapa]) y para el mapa
    "Sigue explorando" al final de cada artículo."""
    tax = json.loads((RAIZ / 'contenido/etapa-5/taxonomia.json').read_text(encoding='utf-8'))
    etiquetas = {e['slug']: e['nombre'] for e in tax['etiquetas']}
    tema_de = {c: t['k'] for t in TEMAS for c in t['categorias']}
    nombres_cat = {c['slug']: c['nombre'] for c in tax['categorias']}
    articulos = {}
    for a in tax['asignacion']:
        articulos[a['slug_entrada']] = {
            'titulo': TITULOS[a['slug_entrada']],
            'categoria': a['categoria'],
            'categoria_nombre': nombres_cat.get(a['categoria'], a['categoria']),
            'tema': tema_de.get(a['categoria'], 'ciberpsicologia'),
            'etiquetas': a['etiquetas'],
        }
    temas = []
    for i, t in enumerate(TEMAS):
        if i == 0:
            x, y = 50, 50
        else:
            ang = math.radians(-90 + (i - 1) * 72)
            x, y = round(50 + 37 * math.cos(ang), 1), round(50 + 37 * math.sin(ang), 1)
        temas.append({
            'k': t['k'], 'nombre': t['nombre'], 'sub': t['sub'], 'texto': t['texto'], 'x': x, 'y': y,
            'categorias': t['categorias'],
            'enlaces': [[txt, h.replace(C, '')] for txt, h in t['enlaces']],
            'articulos': [s for s, v in articulos.items() if v['tema'] == t['k']],
        })
    datos = {
        '_meta': {
            'generado_por': 'contenido/etapa-7/generar-bloques.py (mapa.py)',
            'fuente': 'contenido/etapa-5/taxonomia.json (categorías, etiquetas y asignación de las 15 entradas)',
        },
        'etiquetas': etiquetas,
        'temas': temas,
        'articulos': articulos,
    }
    destino = RAIZ / 'wp-content/plugins/codigo-calma/data/mapa-temas.json'
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return destino


def mapa(cabecera):
    exportar()
    return (cabecera('Inicio · mapa de temas',
                     'Va entre "¿Cómo son tus momentos con la tecnología?" y los accesos: un bloque "Código corto" con [calma_mapa].\n'
                     '     Lo dibuja el plugin (includes/mapa.php) con data/mapa-temas.json, generado desde contenido/etapa-5/taxonomia.json.')
            + '[calma_mapa]\n')
