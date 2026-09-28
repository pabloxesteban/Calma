"""Bienestar digital con el lenguaje de la Etapa 7 ("red clara").

Mismo texto que hoy (con la apertura de la Etapa 5); cambia la forma:

- La infografía en imagen (diagrama de Venn) pasa a una figura dibujada en el
  mismo lugar (arriba a la derecha): al cargar, se arma sola una vez (cada
  área aparece con su ícono y al final los tres círculos se juntan y se
  enciende "Bienestar digital" en la intersección). Es role="img" con descripción,
  y lo que decía la imagen dentro de cada círculo pasa a texto real en la
  tarjeta de cada área.
- Las tres áreas: tarjetas con ícono de línea, su texto y los tres temas de
  cada una. Al pasar el puntero por una, la figura destaca su círculo.
- "Primeros pasos hacia la calma": cuatro tarjetas numeradas con un
  micro-organismo cada una, en lugar de los bloques lavanda con íconos.
Lo usa generar-bloques.py.
"""
import math

# (clave, tono, nombre, texto de la tarjeta, temas que mostraba la infografía, centro del círculo)
AREAS = [
    ('ciberpsicologia', 'ia', 'Ciberpsicología',
     'Estudia cómo la tecnología impacta tu comportamiento, tus emociones y tus vínculos. Entiende tus patrones reales.',
     ['Comportamiento', 'Patrones digitales', 'Relaciones'], (170, 165)),
    ('ciberseguridad', 'neurociencia', 'Ciberseguridad',
     'Aprender a proteger tu privacidad, tus datos y tu autonomía en el ciberespacio. Comprender cómo se usan tus datos y elegir estar de acuerdo o no.',
     ['Privacidad', 'Protección de datos', 'Autonomía'], (290, 165)),
    ('humano', 'bienestar', 'Bienestar Humano',
     'El objetivo final: quizás, una vida donde la tecnología sirve a nuestras necesidades reales.',
     ['Calidad de vida', 'Salud mental', 'Presencia real'], (230, 268)),
]
TONOS = {'ia': ('#efedf9', '#bdb0ee', '#5b3fb8'), 'neurociencia': ('#e9f1f8', '#9cc3e3', '#1d5f94'),
         'bienestar': ('#e8f3ee', '#9fd0c0', '#1f6b47'), 'psicologia': ('#f6efe1', '#e2c17e', '#7a4d00'),
         'tecnologia': ('#f8ece6', '#ebb79c', '#9a3412')}

ICONOS = {
    # Ciberpsicología: dos nodos unidos por una onda (la persona y la tecnología).
    'ciberpsicologia': '<circle cx="8" cy="16" r="3"/><circle cx="24" cy="16" r="3"/><path d="M11 16c2-5 3.5-5 5 0s3 5 5 0"/>',
    # Ciberseguridad: un candado.
    'ciberseguridad': '<rect x="8" y="14" width="16" height="12" rx="3"/><path d="M11 14v-3a5 5 0 0 1 10 0v3"/><circle class="o-lleno" cx="16" cy="20" r="1.4"/>',
    # Bienestar humano: una hoja.
    'humano': '<path d="M8 24C8 13 15 7 25 7c0 10-6 17-17 17Z"/><path d="M8 24 18 14"/>',
}


def svg(contenido):
    return ('<svg class="calma-org" viewBox="0 0 160 100" width="160" height="100" aria-hidden="true" focusable="false">'
            + contenido + '</svg>')


def org_pantalla():
    # Un teléfono en pausa y el tiempo que se completa alrededor.
    return svg('<path class="o-trazo" pathLength="1" d="M80 12 A38 38 0 1 1 79.9 12"/>'
               '<rect x="66" y="28" width="28" height="44" rx="6"/>'
               '<path d="M76 43v14M84 43v14" stroke-width="2.2"/>')


def org_privacidad():
    # Un candado que se cierra entre datos dispersos.
    puntos = ''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="2.6"/>'
                     for i, (x, y) in enumerate(((28, 30), (40, 70), (122, 26), (134, 64), (22, 52), (140, 44))))
    return svg(puntos + '<path class="o-arco" d="M70 50v-8a10 10 0 0 1 20 0v8"/>'
               '<rect x="64" y="50" width="32" height="26" rx="5"/><circle class="o-nucleo" cx="80" cy="62" r="3"/>')


def org_respirar():
    # Anillos que respiran desde un centro.
    return svg(''.join(f'<circle class="o-anillo" style="--i:{i}" cx="80" cy="50" r="{r}"/>' for i, r in enumerate((14, 26, 38)))
               + '<circle class="o-nucleo" cx="80" cy="50" r="5"/>')


def org_conexion():
    # Dos personas unidas por un vínculo que se dibuja.
    return svg('<circle cx="40" cy="42" r="10"/><path d="M24 76c2-12 30-12 32 0"/>'
               '<circle cx="120" cy="42" r="10"/><path d="M104 76c2-12 30-12 32 0"/>'
               '<path class="o-trazo" pathLength="1" d="M52 46 C70 24 90 24 108 46"/>'
               '<circle class="o-nucleo" cx="80" cy="30" r="3.5"/>')


PASOS = [
    (org_pantalla, 'neurociencia', 'Tiempo de pantalla consciente',
     'Establecer límites y pausas en el uso de dispositivos ayuda a mantener un equilibrio saludable entre la vida digital y la presencial.'),
    (org_privacidad, 'tecnologia', 'Seguridad y privacidad',
     'Proteger tus datos y manejar permisos de aplicaciones garantiza una experiencia digital segura y confiable.'),
    (org_respirar, 'bienestar', 'Bienestar digital',
     'Incorporar hábitos como desconexión programada y mindfulness digital mejora tu salud mental y tu relación con la tecnología.'),
    (org_conexion, 'ia', 'Conexiones significativas',
     'Cultivar relaciones auténticas y presenciales mientras usas la tecnología de manera intencional fortalece tu bienestar emocional.'),
]


# Figura de la cabecera. Los círculos se cruzan lo justo para que cada área tenga su
# parte propia (con su ícono) y la zona común de las tres quede a la vista: esa zona
# se pinta de verde azulado y una línea fina la une con el nombre "Bienestar digital".
R = 125
CENTROS = {'ciberpsicologia': (190, 200), 'ciberseguridad': (345, 200), 'humano': (267, 335)}
ICONO_EN = {'ciberpsicologia': (135, 180), 'ciberseguridad': (400, 180), 'humano': (267, 400)}
NOMBRE_EN = {'ciberpsicologia': (160, 56), 'ciberseguridad': (380, 56), 'humano': (267, 492)}

ICONOS_GRANDES = {
    # Una onda entre dos nodos (la persona y la tecnología): la onda se mueve.
    'ciberpsicologia': '<circle cx="-22" cy="0" r="6"/><circle cx="22" cy="0" r="6"/>'
                       '<path class="o-onda-viva" d="M-16 0c4-10 7-10 10.7 0s6.6 10 10.6 0 7-10 10.7 0"/>',
    # Un candado: el arco se cierra.
    'ciberseguridad': '<path class="o-arco" d="M-11 -2v-8a11 11 0 0 1 22 0v8"/><rect x="-17" y="-2" width="34" height="26" rx="5"/>'
                      '<circle class="o-lleno" cx="0" cy="10" r="3"/>',
    # Una hoja que crece.
    'humano': '<path class="o-trazo" pathLength="1" d="M-16 20C-16 -4 -2 -18 20 -18c0 22-14 38-36 38Z"/>'
              '<path class="o-trazo" pathLength="1" d="M-16 20 8 -4"/>',
}


def venn():
    areas, clips = '', ''
    for i, (clave, tono, nombre, _, _, _) in enumerate(AREAS):
        t, a, x = TONOS[tono]
        cx, cy = CENTROS[clave]
        ix, iy = ICONO_EN[clave]
        nx, ny = NOMBRE_EN[clave]
        clips += f'<clipPath id="venn-{clave}"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
        areas += (f'<g class="calma-venn__area calma-venn__area--{clave}" data-area="{clave}" style="--acento:{a};--texto:{x};--i:{i}">'
                  f'<circle class="calma-venn__circulo" cx="{cx}" cy="{cy}" r="{R}"/>'
                  f'<g class="calma-venn__icono" transform="translate({ix} {iy}) scale(1.2)">{ICONOS_GRANDES[clave]}</g>'
                  f'<text class="calma-venn__nombre" x="{nx}" y="{ny}" text-anchor="middle">{nombre.replace("Bienestar Humano", "Bienestar humano")}</text></g>')
    cx, cy = CENTROS['humano']
    # Centro aproximado de la zona común (para la línea que va hacia el nombre).
    zx, zy = 267, 246
    return ('<figure class="calma-venn" data-calma-venn data-paso="4">'
            '<svg viewBox="0 0 660 510" width="660" height="510" role="img" aria-labelledby="venn-titulo venn-desc">'
            '<title id="venn-titulo">Las tres áreas del bienestar digital</title>'
            '<desc id="venn-desc">Tres círculos que se cruzan: ciberpsicología (comportamiento, patrones digitales y relaciones), '
            'ciberseguridad (privacidad, protección de datos y autonomía) y bienestar humano (calidad de vida, salud mental y '
            'presencia real). La zona donde se cruzan los tres es el bienestar digital.</desc>'
            f'<defs>{clips}</defs>'
            f'{areas}'
            '<g class="calma-venn__centro">'
            '<g clip-path="url(#venn-ciberpsicologia)"><g clip-path="url(#venn-ciberseguridad)">'
            f'<circle class="calma-venn__zona" cx="{cx}" cy="{cy}" r="{R}"/></g></g>'
            f'<circle class="calma-venn__nucleo" cx="{zx}" cy="{zy}" r="5"/>'
            f'<path class="calma-venn__linea" pathLength="1" d="M{zx + 8} {zy} H488"/>'
            '<g class="calma-venn__etiqueta"><rect x="490" y="212" width="160" height="70" rx="16"/>'
            '<text x="570" y="241" text-anchor="middle">Bienestar</text><text x="570" y="267" text-anchor="middle">digital</text></g>'
            '</g></svg></figure>')


def org_ciberpsicologia():
    # La persona y la tecnología: dos nodos unidos por una onda que se calma, y los patrones alrededor.
    puntos = ''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="2.4"/>'
                     for i, (x, y) in enumerate(((30, 22), (130, 22), (22, 78), (138, 78))))
    return svg(puntos + '<circle cx="42" cy="50" r="10"/><circle cx="118" cy="50" r="10"/>'
               '<path class="o-onda" d="M53 50c5-14 9-14 13 0s8 14 13 0 8-14 13 0 6 12 15 0"/>')


def org_ciberseguridad():
    # Un escudo que se dibuja y se completa con su marca.
    return svg('<path class="o-trazo" pathLength="1" d="M80 12 110 24v24c0 20-13 32-30 40-17-8-30-20-30-40V24Z"/>'
               '<path class="o-trazo" pathLength="1" style="--i:2" d="M68 50l9 9 17-19"/>')


def org_humano():
    # Una hoja que crece y un centro que late.
    return svg('<path class="o-trazo" pathLength="1" d="M52 84C52 50 72 22 112 18c0 40-24 66-60 66Z"/>'
               '<path class="o-trazo" pathLength="1" style="--i:1" d="M52 84 92 42"/>'
               '<circle class="o-nucleo" cx="52" cy="84" r="4"/>')


FIGURAS_AREA = {'ciberpsicologia': org_ciberpsicologia, 'ciberseguridad': org_ciberseguridad, 'humano': org_humano}


def bienestar(cabecera):
    # Las tres áreas y los cuatro pasos usan la misma tarjeta que Herramientas y el Test:
    # figura animada arriba, etiqueta, título y texto (con la luz que sigue al puntero).
    areas = ''.join(
        f'<li class="calma-habito calma-area calma-tono--{tono}" data-area="{clave}" style="--i:{i}">{FIGURAS_AREA[clave]()}'
        f'<h3>{nombre}</h3><p>{texto}</p>'
        f'<ul class="calma-area__temas" aria-label="Temas de {nombre.lower()}">' + ''.join(f'<li>{t}</li>' for t in temas) + '</ul></li>'
        for i, (clave, tono, nombre, texto, temas, _) in enumerate(AREAS))
    pasos = ''.join(
        f'<li class="calma-habito calma-tono--{tono}" style="--i:{i}">{fig()}'
        f'<span class="calma-habito__chip">Paso 0{i + 1}</span><h3>{titulo}</h3><p>{texto}</p></li>'
        for i, (fig, tono, titulo, texto) in enumerate(PASOS))
    return (cabecera('Bienestar digital',
                     'Reemplaza TODO el contenido de Bienestar digital (título, infografía, "La intersección", las tres cajas y "Primeros pasos hacia la calma").\n'
                     '     Un solo bloque "HTML personalizado", ancho completo, sin caja ni título de Kadence. Mismo texto; la infografía pasa a figura dibujada.')
            + f"""<div class="calma-page calma-recursos calma-bienestar">
<section class="calma-hero" aria-labelledby="bienestar-h1"><div class="calma-hero__inner calma-hero__inner--media"><div>
<h1 id="bienestar-h1">Bienestar <em>Digital</em></h1>
<p class="calma-hero__lead">La intersección entre ciberpsicología, ciberseguridad y bienestar humano.</p>
</div>{venn()}</div></section>
<section class="calma-section" aria-labelledby="interseccion-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="interseccion-h2">La <em>intersección</em></h2></div>
<div class="calma-bienestar__interseccion">
<p class="calma-definicion"><strong>El bienestar digital es usar la tecnología con intención: entender cómo funcionas con ella, proteger tu privacidad y decidir de forma consciente qué lugar quieres que ocupe en tu vida.</strong></p>
<aside class="calma-resumen" aria-label="En resumen"><p><strong>En resumen:</strong> en la práctica, significa saber por qué estás en cada plataforma, reconocer su costo real y decidir si vale la pena. Se apoya en tres áreas: la <a href="https://codigocalma.com/ciberpsicologia/">ciberpsicología</a>, que estudia cómo la tecnología influye en tu comportamiento, tus emociones y tus vínculos; la ciberseguridad, que cuida tu privacidad y tus datos; y el bienestar humano, que es el objetivo final.</p></aside>
</div>
<ul class="calma-habitos">{areas}</ul>
</div></section>
<section class="calma-section" aria-labelledby="pasos-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="pasos-h2">Primeros pasos hacia la <em>calma</em></h2>
<p>Cómo comenzar a construir una relación más consciente con la tecnología</p></div>
<ul class="calma-habitos calma-habitos--4">{pasos}</ul>
</div></section>
</div>
""")
