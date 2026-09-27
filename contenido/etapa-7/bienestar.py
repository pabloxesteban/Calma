"""Bienestar digital con el lenguaje de la Etapa 7 ("red clara").

Mismo texto que hoy (con la apertura de la Etapa 5); cambia la forma:

- La infografía en imagen (diagrama de Venn) pasa a un recorrido con scroll: la
  figura queda fija mientras se lee cada área; cada círculo aparece con su
  ícono animado y, en el último paso, los tres se juntan y se enciende
  "Bienestar digital" en la intersección (con la definición al lado). Es role="img" con descripción,
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


# Posiciones de cada círculo: separadas mientras se presenta cada área y juntas en el último paso.
SEPARADAS = {'ciberpsicologia': (150, 195), 'ciberseguridad': (330, 195), 'humano': (240, 350)}
JUNTAS = {'ciberpsicologia': (197, 215), 'ciberseguridad': (283, 215), 'humano': (240, 290)}

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
    circulos, iconos = '', ''
    for i, (clave, tono, nombre, _, _, _) in enumerate(AREAS):
        t, a, x = TONOS[tono]
        sx, sy = SEPARADAS[clave]
        jx, jy = JUNTAS[clave]
        circulos += (f'<g class="calma-venn__area calma-venn__area--{clave}" data-area="{clave}" '
                     f'style="--acento:{a};--texto:{x};--sx:{sx}px;--sy:{sy}px;--jx:{jx}px;--jy:{jy}px;--i:{i}">'
                     f'<circle class="calma-venn__circulo" r="112"/>'
                     f'<g class="calma-venn__icono">{ICONOS_GRANDES[clave]}</g>'
                     f'<text class="calma-venn__nombre" y="{-62 if clave != "humano" else 70}" text-anchor="middle">{nombre.replace("Bienestar Humano", "Bienestar humano")}</text></g>')
    return ('<figure class="calma-venn" data-calma-venn data-paso="4">'
            '<svg viewBox="0 0 480 480" width="480" height="480" role="img" aria-labelledby="venn-titulo venn-desc">'
            '<title id="venn-titulo">Las tres áreas del bienestar digital</title>'
            '<desc id="venn-desc">Tres círculos que se cruzan: ciberpsicología (comportamiento, patrones digitales y relaciones), '
            'ciberseguridad (privacidad, protección de datos y autonomía) y bienestar humano (calidad de vida, salud mental y '
            'presencia real). En la intersección de los tres está el bienestar digital.</desc>'
            '<circle class="calma-venn__orbita" cx="240" cy="245" r="200"/><circle class="calma-venn__orbita" cx="240" cy="245" r="150"/>'
            f'{circulos}'
            '<g class="calma-venn__centro"><circle class="calma-venn__halo" cx="240" cy="240" r="34"/>'
            '<circle class="calma-venn__nucleo" cx="240" cy="240" r="14"/>'
            '<rect x="156" y="262" width="168" height="40" rx="20"/>'
            '<text x="240" y="288" text-anchor="middle">Bienestar digital</text></g>'
            '</svg></figure>')


def bienestar(cabecera):
    icono = lambda clave: (f'<svg class="calma-historia__icono" viewBox="-32 -32 64 64" width="56" height="56" aria-hidden="true" focusable="false">'
                           f'{ICONOS_GRANDES[clave]}</svg>')
    areas = ''.join(
        f'<li class="calma-historia__paso calma-area calma-tono--{tono}" data-area="{clave}" data-paso="{i + 1}" style="--i:{i}">'
        f'{icono(clave)}<h3>{nombre}</h3><p>{texto}</p>'
        f'<ul class="calma-area__temas" aria-label="Temas de {nombre.lower()}">' + ''.join(f'<li>{t}</li>' for t in temas) + '</ul></li>'
        for i, (clave, tono, nombre, texto, temas, _) in enumerate(AREAS))
    areas += ('<li class="calma-historia__paso calma-historia__final" data-paso="4">'
              '<p class="calma-definicion"><strong>El bienestar digital es usar la tecnología con intención: entender cómo funcionas con ella, '
              'proteger tu privacidad y decidir de forma consciente qué lugar quieres que ocupe en tu vida.</strong></p></li>')
    pasos = ''.join(
        f'<li class="calma-paso-calma calma-tono--{tono}" style="--i:{i}"><span class="calma-paso-calma__num" aria-hidden="true">0{i + 1}</span>'
        f'{fig()}<h3>{titulo}</h3><p>{texto}</p></li>'
        for i, (fig, tono, titulo, texto) in enumerate(PASOS))
    return (cabecera('Bienestar digital',
                     'Reemplaza TODO el contenido de Bienestar digital (título, infografía, "La intersección", las tres cajas y "Primeros pasos hacia la calma").\n'
                     '     Un solo bloque "HTML personalizado", ancho completo, sin caja ni título de Kadence. Mismo texto; la infografía pasa a figura dibujada.')
            + f'''<div class="calma-page calma-recursos calma-bienestar">
<section class="calma-hero calma-bienestar__hero" aria-labelledby="bienestar-h1"><div class="calma-hero__inner"><div>
<h1 id="bienestar-h1">Bienestar <em>Digital</em></h1>
<p class="calma-hero__lead">La intersección entre ciberpsicología, ciberseguridad y bienestar humano.</p>
</div></div></section>
<section class="calma-section calma-historia" aria-labelledby="interseccion-h2"><div class="calma-container">
<div class="calma-bienestar__interseccion">
<h2 id="interseccion-h2">La intersección</h2>
<aside class="calma-resumen" aria-label="En resumen"><p><strong>En resumen:</strong> en la práctica, significa saber por qué estás en cada plataforma, reconocer su costo real y decidir si vale la pena. Se apoya en tres áreas: la <a href="https://codigocalma.com/ciberpsicologia/">ciberpsicología</a>, que estudia cómo la tecnología influye en tu comportamiento, tus emociones y tus vínculos; la ciberseguridad, que cuida tu privacidad y tus datos; y el bienestar humano, que es el objetivo final.</p></aside>
</div>
<div class="calma-historia__cuerpo">
<div class="calma-historia__figura">{venn()}</div>
<ol class="calma-historia__pasos">{areas}</ol>
</div>
</div></section>
<section class="calma-section" aria-labelledby="pasos-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="pasos-h2">Primeros pasos hacia la <em>calma</em></h2>
<p>Cómo comenzar a construir una relación más consciente con la tecnología</p></div>
<ol class="calma-pasos-calma">{pasos}</ol>
</div></section>
</div>
''')
