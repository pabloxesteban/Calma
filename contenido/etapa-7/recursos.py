"""Herramientas y Descargas con el lenguaje de la Etapa 7. Mismo texto que hoy
está publicado (con el bloque "Pequeños hábitos" de la Etapa 2); cambia la
forma:

- Herramientas: los tres hábitos con un micro-organismo cada uno (la misma
  familia visual que los seis estados del Inicio) y las apps como tarjetas
  con logo chico, nombre, descripción y enlace visible a la app.
- Descargas: cada guía como tarjeta con portada, autora, título, descripción
  y botón "Descargar" que dice qué se descarga (PDF).
Lo usa generar-bloques.py. Las imágenes son las que ya están en la
biblioteca de medios, con sus medidas declaradas.
"""
import html

SUBIDAS = 'https://codigocalma.com/wp-content/uploads/'
PEREZOSA = ' loading="lazy"'


def svg(contenido):
    return ('<svg class="calma-org" viewBox="0 0 160 100" width="160" height="100" aria-hidden="true" focusable="false">'
            + contenido + '</svg>')


# Micro-organismos de los hábitos: estado final dibujado; la animación parte de un "antes".
def org_diario():
    # Un trazo enredado que se ordena en renglones.
    return svg('<path class="o-trazo" pathLength="1" d="M18 30 C30 12 40 48 52 26 S70 40 78 30 L142 30"/>'
               '<path class="o-trazo" pathLength="1" style="--i:1" d="M18 52 C28 40 36 62 48 50 L142 50"/>'
               '<path class="o-trazo" pathLength="1" style="--i:2" d="M18 72 L110 72"/>'
               '<circle class="o-nucleo" cx="124" cy="72" r="4"/>')


def org_meditar():
    # Anillos que se abren desde un centro que late cada vez más lento.
    return svg(''.join(f'<circle class="o-anillo" style="--i:{i}" cx="80" cy="50" r="{r}"/>' for i, r in enumerate((14, 26, 38)))
               + '<circle class="o-nucleo" cx="80" cy="50" r="5"/>')


def org_app():
    # Un teléfono con una onda que se calma adentro.
    return svg('<rect x="58" y="10" width="44" height="80" rx="9"/>'
               '<path class="o-onda" d="M64 50 C68 38 72 62 76 50 S84 44 88 50 S94 54 96 50"/>'
               '<circle class="o-nucleo" cx="80" cy="80" r="3"/>')


HABITOS = [
    ('psicologia', org_diario, 'Regulación emocional', 'Llevar un diario',
     'Escribir lo que sientes activa el pensamiento reflexivo. Cinco minutos al día pueden cambiar cómo procesas el estrés.'),
    ('bienestar', org_meditar, 'Atención plena', 'Meditar',
     'La práctica regular entrena la atención y reduce la reactividad automática. No hace falta una hora: diez minutos hacen diferencia.'),
    ('neurociencia', org_app, 'Punto de entrada', 'Calm y similares',
     'Apps como Calm, Headspace o Insight Timer ofrecen guías accesibles. Útiles como complemento para crear el hábito inicial.'),
]

# (tema para el tono, título del grupo, [(nombre, descripción, url, imagen, lado, alt)])
APPS = [
    ('bienestar', 'Mindfulness, relajación y hábitos de bienestar', [
        ('Headspace', 'Una de las apps más populares de meditación y mindfulness con prácticas guiadas cortas, ejercicios de respiración y contenido para estrés, sueño o enfoque.',
         'https://www.headspace.com/', '2026/05/headspace.jpg', 270, 'Logo Headspace'),
        ('Finch', 'Combina mindfulness y autocuidado con un estilo lúdico (cuidar “una mascota virtual” mediante actividades de bienestar).',
         'https://finchcare.com/', '2026/05/finch.jpg', 270, 'Logo Finch'),
        ('Calm', 'Enfocada en la relajación y el sueño: historias para dormir, sonidos calmantes, meditaciones guiadas y ejercicios de respiración.',
         'https://health.calm.com/', '2026/05/calm.jpg', 330, 'Logo Calm'),
    ]),
    ('psicologia', 'Diario, hábitos y seguimiento', [
        ('Daylio', 'App de diario y seguimiento del humor, muy simple y visual: eliges cómo te sentiste y qué hiciste, y con el tiempo podrás identificar áreas de mejora.',
         'https://play.google.com/store/apps/details?id=net.daylio&hl=es_419&pli=1', '2026/05/daylio.jpg', 181, 'Logo Daylio'),
        ('PTSD Coach y Mindfulness Coach', 'Ejercicios de respiración, relajación y seguimiento de síntomas.',
         'https://play.google.com/store/apps/details?id=is.vertical.ptsdcoach', '2026/05/ptsd.jpg', 240, 'Logo PTSD Coach'),
    ]),
]

# (título, lang del título, descripción, lang de la descripción, pdf, portada, alt)
GUIAS = [
    ('Ansiedad funcional vs. ansiedad desbordada', None, 'Nuestra interacción digital y su impacto en la salud mental', None,
     '2026/06/Ansiedad-Funcional-vs-Ansiedad-Desbordada.pdf', '2026/05/ansiedad-1.jpg', 'Portada de la guía Ansiedad funcional vs. ansiedad desbordada'),
    ('Guía de ciberseguridad para psicólogos', None, 'Conceptos, herramientas y recomendaciones.', None,
     '2026/06/Guia-de-Ciberseguridad-para-Psicologos.pdf', '2026/05/guia-1.jpg', 'Portada de la Guía de ciberseguridad para psicólogos'),
    ('Psicología para devs', None, 'Conceptos para integrar psicología a tu desarrollo.', None,
     '2026/06/psicologia-para-devs.pdf', '2026/05/para_devs-1.jpg', 'Portada de la guía Psicología para devs'),
    ('The Psychology of Trust', 'en', 'Behavioral Science and Cybersecurity Awareness. A 3-phase Learning Journey with AI', 'en',
     '2026/06/The-psychology-of-trust-Tatiana-Stacul.pdf', '2026/05/trust-1.jpg', 'Portada de la guía The Psychology of Trust'),
]


def figura_herramientas():
    """Cabecera de Herramientas: un teléfono con apps que se encienden y tres hábitos en su órbita."""
    tonos = ['#e2c17e', '#bdb0ee', '#9cc3e3', '#9fd0c0', '#ebb79c', '#9cc3e3', '#bdb0ee', '#9fd0c0']
    apps = ''.join(f'<rect class="calma-hero-fig__app" style="--i:{i};--acento:{tonos[i]}" x="{104 + (i % 2) * 30}" y="{66 + (i // 2) * 30}" width="22" height="22" rx="6"/>'
                   for i in range(8))
    orbita = ''.join(f'<circle class="calma-hero-fig__nodo" style="--i:{i};--acento:{a}" cx="{130 + 112 * __import__("math").cos(__import__("math").radians(g))}" cy="{130 + 112 * __import__("math").sin(__import__("math").radians(g))}" r="9"/>'
                     for i, (g, a) in enumerate(((-150, '#e2c17e'), (-30, '#9fd0c0'), (90, '#9cc3e3'))))
    return ('<div class="calma-hero__media calma-hero-fig" aria-hidden="true"><svg viewBox="0 0 260 260" width="260" height="260" focusable="false">'
            '<circle class="calma-hero-fig__guia" cx="130" cy="130" r="112"/>' + orbita +
            '<rect class="calma-hero-fig__marco" x="92" y="40" width="76" height="180" rx="16"/>' + apps +
            '<circle class="calma-hero-fig__boton" cx="130" cy="202" r="4"/>'
            '<circle class="calma-hero-fig__halo" style="--acento:#9fd0c0" cx="145" cy="137" r="20"/></svg></div>')


def figura_descargas():
    """Cabecera de Descargas: tres guías apiladas y la flecha que las baja."""
    libros = ''.join(f'<g class="calma-hero-fig__libro" style="--i:{i};--acento:{a}"><rect x="{58 + i * 26}" y="{44 + (2 - i) * 14}" width="96" height="128" rx="8"/>'
                     f'<path d="M{72 + i * 26} {44 + (2 - i) * 14}v128"/><path d="M{84 + i * 26} {76 + (2 - i) * 14}h52M{84 + i * 26} {90 + (2 - i) * 14}h36"/></g>'
                     for i, a in enumerate(('#e2c17e', '#bdb0ee', '#9cc3e3')))
    return ('<div class="calma-hero__media calma-hero-fig" aria-hidden="true"><svg viewBox="0 0 260 260" width="260" height="260" focusable="false">'
            '<circle class="calma-hero-fig__guia" cx="130" cy="130" r="118"/>' + libros +
            '<path class="calma-hero-fig__flecha" pathLength="1" d="M130 186v42M116 214l14 14 14-14"/>'
            '<path class="calma-hero-fig__bandeja" d="M96 238h68"/></svg></div>')


def e(t):
    return html.escape(t, quote=True)


def herramientas(cabecera):
    habitos = ''.join(
        f'<li class="calma-habito calma-tono--{tema}" style="--i:{i}">{fig()}'
        f'<span class="calma-habito__chip">{chip}</span><h3>{titulo}</h3><p>{texto}</p></li>'
        for i, (tema, fig, chip, titulo, texto) in enumerate(HABITOS))
    grupos = ''
    for n, (tema, titulo, apps) in enumerate(APPS):
        tarjetas = ''.join(
            f'<li class="calma-app" style="--i:{i}"><a class="calma-app__enlace" href="{e(url)}" rel="noopener" target="_blank">'
            f'<img class="calma-app__logo" src="{SUBIDAS}{img}" width="{lado}" height="{lado}" alt="" loading="lazy" decoding="async">'
            f'<h3 class="calma-app__nombre">{e(nombre)}</h3><span class="calma-app__desc">{e(texto)}</span>'
            f'<span class="calma-app__ir" aria-hidden="true"></span><span class="screen-reader-text"> (se abre en una pestaña nueva)</span></a></li>'
            for i, (nombre, texto, url, img, lado, alt) in enumerate(apps))
        grupos += (f'<div class="calma-apps calma-tono--{tema}"><h2 class="calma-apps__titulo" id="apps-{n}">{titulo}</h2>'
                   f'<ul class="calma-apps__lista" aria-labelledby="apps-{n}">{tarjetas}</ul></div>')
    return (cabecera('Herramientas',
                     'Reemplaza TODO el contenido de Herramientas (título, textos, "Pequeños hábitos" y las dos filas de apps). Un solo bloque "HTML personalizado".\n'
                     '     Mismo texto que hoy; cambia la forma. Estilos: plugin (calma-etapa7.css). Ancho completo, sin caja, sin título de Kadence.')
            + f'''<div class="calma-page calma-recursos">
<section class="calma-hero" aria-labelledby="herramientas-h1"><div class="calma-hero__inner calma-hero__inner--media"><div>
<h1 id="herramientas-h1">Aplicaciones de <em>productividad</em> y <em>calma</em></h1>
<p class="calma-hero__lead">Aquí encontrarás recomendaciones de apps para salud mental y productividad.</p>
<p>Las aplicaciones de salud mental utilizan principios de la psicología para ofrecer técnicas de meditación que pueden reducir el estrés y la ansiedad. Además, herramientas como los dispositivos de seguimiento del sueño y la actividad física ayudan a los usuarios a monitorear y mejorar su salud general. Si bien están pensadas como apoyo al bienestar diario, es importante recordar que no reemplazan el acompañamiento profesional.</p>
</div>{figura_herramientas()}</div></section>
<section class="calma-section" aria-labelledby="habitos-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="habitos-h2">Pequeños hábitos, <em>gran diferencia</em>.</h2>
<p>Estas herramientas no reemplazan el acompañamiento profesional. Son puntos de partida que muchas personas encuentran útiles.</p></div>
<ul class="calma-habitos">{habitos}</ul>
<p class="calma-recursos__nota">Estas sugerencias son orientativas y no constituyen prescripción terapéutica.</p>
</div></section>
<section class="calma-section calma-recursos__apps" aria-label="Apps recomendadas"><div class="calma-container">
{grupos}
<p class="calma-notice calma-recursos__aviso">Este contenido es educativo. Las apps recomendadas acompañan el bienestar diario y no reemplazan atención profesional.</p>
</div></section>
</div>
''')


def descargas(cabecera):
    def lang(l):
        return f' lang="{l}"' if l else ''
    tarjetas = ''.join(
        f'<li class="calma-descarga" style="--i:{i}"><div class="calma-descarga__portada"><img src="{SUBIDAS}{img}" width="400" height="400" alt="{e(alt)}"'
        f'{"" if i < 2 else PEREZOSA} decoding="async"></div>'
        f'<div class="calma-descarga__texto"><p class="calma-descarga__autora">Por Tatiana X. Stacul</p>'
        f'<h2><span{lang(tl)}>{e(titulo)}</span>{" (en inglés)" if tl == "en" else ""}</h2><p{lang(dl)}>{e(texto)}</p>'
        f'<p class="calma-descarga__accion"><a class="calma-btn calma-btn--primary" href="https://codigocalma.com/wp-content/uploads/{pdf}" download>Descargar'
        f'<span class="screen-reader-text"> {e(titulo)}</span> <span class="calma-descarga__formato">PDF</span></a></p></div></li>'
        for i, (titulo, tl, texto, dl, pdf, img, alt) in enumerate(GUIAS))
    return (cabecera('Descargas',
                     'Reemplaza TODO el contenido de Descargas (título y las dos filas de guías). Un solo bloque "HTML personalizado".\n'
                     '     Mismo texto que hoy; cambia la forma. Estilos: plugin (calma-etapa7.css). Ancho completo, sin caja, sin título de Kadence.')
            + f'''<div class="calma-page calma-recursos">
<section class="calma-hero" aria-labelledby="descargas-h1"><div class="calma-hero__inner calma-hero__inner--media"><div>
<h1 id="descargas-h1">Libros de <em>descarga gratuita</em></h1>
</div>{figura_descargas()}</div></section>
<section class="calma-section" aria-label="Guías para descargar"><div class="calma-container">
<ul class="calma-descargas">{tarjetas}</ul>
</div></section>
</div>
''')
