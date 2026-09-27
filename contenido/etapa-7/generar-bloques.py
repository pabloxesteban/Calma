#!/usr/bin/env python3
"""Genera los bloques "HTML personalizado" de la Etapa 7 (dirección de arte
"organismo digital", ver docs/direccion-arte-organismo.md).

  bloques/inicio-momentos.html  → reemplaza la fila "¿Cómo son tus momentos con
                                  la tecnología?" y sus 6 tarjetas giratorias.
  bloques/inicio-bienvenida.html → reemplaza la fila "Te damos la bienvenida"
                                  (texto, ilustración y cifras con visualización).
  bloques/inicio-linea-de-tiempo.html → reemplaza la línea de tiempo de la Etapa 1.

Texto: el mismo que hoy está publicado en el Inicio (no se cambian hallazgos,
fuentes ni cifras). Estilos: plugin codigo-calma, calma-etapa7.css. El
movimiento lo agrega calma-organismo.js; sin JavaScript o con movimiento
reducido, todo el texto se ve y cada figura muestra su estado final.

Ejecutar: python3 contenido/etapa-7/generar-bloques.py
"""
import math, pathlib, random, sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from escenas import accesos  # noqa: E402
from mapa import mapa  # noqa: E402
from paginas import servicios, contacto_intro, contacto_proceso  # noqa: E402
from equipo import equipo, perfil, PERSONAS  # noqa: E402
from recursos import herramientas, descargas  # noqa: E402

OUT = pathlib.Path(__file__).with_name('bloques')
OUT.mkdir(exist_ok=True)


def ph(texto):
    return f'<span class="calma-placeholder">[COMPLETAR: {texto}]</span>'


def cabecera(titulo, instrucciones):
    return (f'<!-- Código Calma · {titulo} (Etapa 7)\n     {instrucciones}\n'
            '     Generado por contenido/etapa-7/generar-bloques.py. Estilos: plugin codigo-calma. -->\n')


# --------------------------------------------------------------------------
# Micro-organismos: cada uno dibuja su estado final. La animación (CSS) parte
# de un estado "antes" y llega a este, así que sin movimiento se entiende igual.
# viewBox 0 0 160 100, trazo fino en currentColor.
# --------------------------------------------------------------------------
def svg(contenido):
    return ('<svg class="calma-org" viewBox="0 0 160 100" width="160" height="100" aria-hidden="true" focusable="false">'
            + contenido + '</svg>')


def org_disponibilidad():
    # Pulsación: un nodo que emite anillos sin pausa.
    anillos = ''.join(f'<circle class="o-anillo" style="--i:{i}" cx="80" cy="50" r="{12 + i * 11}" />' for i in range(4))
    return svg(anillos + '<circle class="o-nucleo" cx="80" cy="50" r="5" />')


def org_validacion():
    # Partículas que se agrupan alrededor de un centro (el "me gusta").
    rnd = random.Random(7)
    pts = ''
    for i in range(22):
        ang = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(5, 26)
        x, y = 80 + r * math.cos(ang), 50 + r * math.sin(ang) * 0.8
        # Posición de partida: dispersa (se usa en la animación).
        dx = rnd.uniform(-62, 62) - (x - 80) * 0.2
        dy = rnd.uniform(-38, 38) - (y - 50) * 0.2
        pts += f'<circle class="o-part" style="--dx:{dx:.1f}px;--dy:{dy:.1f}px;--i:{i}" cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice((1.6, 2, 2.4))}" />'
    return svg('<circle class="o-halo" cx="80" cy="50" r="34" />' + pts)


def org_presencia():
    # Un campo que se divide en dos.
    rnd = random.Random(3)
    izq, der = '', ''
    for i in range(34):
        ang = rnd.uniform(0, 2 * math.pi)
        r = math.sqrt(rnd.random()) * 30
        x, y = 80 + r * math.cos(ang), 50 + r * math.sin(ang)
        c = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" />'
        if x < 80:
            izq += c
        else:
            der += c
    return svg('<line class="o-corte" x1="80" y1="14" x2="80" y2="86" />'
               f'<g class="o-mitad o-mitad--izq">{izq}</g><g class="o-mitad o-mitad--der">{der}</g>')


def org_scroll():
    # Flujo que avanza sin llegar a ningún lado: se desvanece antes del final.
    return svg('<defs><linearGradient id="o-desv" x1="0" x2="1"><stop offset="0" stop-color="currentColor" stop-opacity="0"/>'
               '<stop offset=".25" stop-color="currentColor"/><stop offset=".75" stop-color="currentColor"/>'
               '<stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient></defs>'
               '<g stroke="url(#o-desv)">'
               + ''.join(f'<path class="o-flujo" style="--i:{i}" d="M4 {30 + i * 14} C 44 {18 + i * 14}, 76 {44 + i * 14}, 116 {30 + i * 14} S 150 {24 + i * 14}, 156 {30 + i * 14}" />' for i in range(4))
               + '</g>')


def org_ruido():
    # Una onda calma atravesada por interferencias.
    onda = 'M4 50 ' + ' '.join(f'Q {10 + j * 24} {38 if j % 2 == 0 else 62} {22 + j * 24} 50' for j in range(6))
    rnd = random.Random(11)
    ticks = ''
    for i in range(16):
        x = 10 + i * 9.2 + rnd.uniform(-2, 2)
        h = rnd.uniform(6, 22)
        ticks += f'<line class="o-tick" style="--i:{i}" x1="{x:.1f}" y1="{50 - h:.1f}" x2="{x:.1f}" y2="{50 + h:.1f}" />'
    return svg(f'<path class="o-onda" d="{onda}" />' + ticks)


def org_sueno():
    # Transición a baja frecuencia: la onda rápida se apaga y queda una lenta.
    rapida = 'M4 50 ' + ' '.join(f'Q {7 + j * 12} {40 if j % 2 == 0 else 60} {10 + j * 12} 50' for j in range(13))
    lenta = 'M4 50 C 30 34, 54 34, 80 50 S 130 66, 156 50'
    return svg('<rect class="o-noche" x="0" y="0" width="160" height="100" rx="12" />'
               f'<path class="o-rapida" d="{rapida}" /><path class="o-lenta" d="{lenta}" />'
               '<circle class="o-luna" cx="132" cy="24" r="6" />')


ESTADOS = [
    dict(slug='disponibilidad', org=org_disponibilidad, concepto='Pulsación',
         titulo='Disponibilidad permanente',
         pregunta='¿Entregamos nuestro espacio personal a cambio de la velocidad de respuesta?',
         hallazgo='Revisar el correo laboral fuera del horario reduce la desconexión psicológica del trabajo, aumenta el conflicto trabajo-familia y contribuye al agotamiento emocional crónico.',
         fuente='PMC · NIH, 2022', obra='Keeping Up With Work Email After Hours and Employee Wellbeing: Examining Relationships During and Prior to the COVID-19 Pandemic',
         url=''),  # En el sitio publicado este enlace está vacío.
    dict(slug='validacion', org=org_validacion, concepto='Agrupamiento',
         titulo='Validación métrica',
         pregunta='¿Quién decide qué es visible y quién se beneficia de nuestra atención?',
         hallazgo='El feedback positivo en redes activa regiones cerebrales vinculadas al refuerzo y la autoevaluación. Recibir likes sube la autoestima de forma medible; no recibirlos la baja.',
         fuente='Frontiers in Psychology, 2025', obra='A comparative study of state self-esteem responses to social media feedback loops in adolescents and adults · doi: 10.3389/fpsyg.2025.1625771',
         url='https://pubmed.ncbi.nlm.nih.gov/41064185/'),
    dict(slug='presencia', org=org_presencia, concepto='División',
         titulo='Presencia fragmentada',
         pregunta='¿Estamos viviendo el momento o posando para después?',
         hallazgo='En promedio, las personas usan el móvil durante el 27% del tiempo que pasan con su pareja. Ese uso —no el tiempo total de pantalla— predice menor satisfacción en la relación.',
         fuente='PMC · NIH, 2024', obra='Objective Phone Use During Time with One’s Partner: Associations with Relationship and Individual Well-being',
         url='https://pubmed.ncbi.nlm.nih.gov/41346411/'),
    dict(slug='scroll', org=org_scroll, concepto='Flujo sin destino',
         titulo='Scroll sin horizonte',
         pregunta='¿Cuántas veces abrimos una app sin saber qué buscábamos?',
         hallazgo='Aza Raskin, inventor del scroll infinito, declaró públicamente arrepentirse de haberlo creado. En 2026, la Comisión Europea determinó que el diseño adictivo de TikTok incumple la Ley de Servicios Digitales.',
         fuente='Aza Raskin, X (2019) · Comisión Europea, 2026', obra='EC Press release IP/26/312 · EU Digital Services Act enforcement against TikTok',
         url='https://ec.europa.eu/commission/presscorner/detail/en/ip_26_312'),
    dict(slug='ruido', org=org_ruido, concepto='Interferencia',
         titulo='Ruido constante',
         pregunta='¿Cuándo fue la última vez que tuvimos una conversación sin mirar el celular?',
         hallazgo='La simple presencia de un teléfono sobre la mesa —sin usarlo— reduce la calidad de la conversación y los niveles de empatía reportados, especialmente entre personas cercanas.',
         fuente='Misra et al. · Virginia Tech, 2014', obra='The iPhone Effect: The Quality of In-Person Social Interactions in the Presence of Mobile Devices · Environment and Behavior · doi: 10.1177/0013916514539755',
         url='https://journals.sagepub.com/doi/10.1177/0013916514539755'),
    dict(slug='sueno', org=org_sueno, concepto='Baja frecuencia',
         titulo='Pantalla hasta dormir',
         pregunta='¿Descansamos de verdad o solo apagamos la pantalla?',
         hallazgo='Un estudio con 122.058 participantes vinculó el uso de pantallas antes de dormir con menor duración del sueño y peor calidad autopercibida, especialmente en personas con cronotipos nocturnos.',
         fuente='JAMA Network Open, 2025', obra='Electronic Screen Use and Sleep Duration and Timing in Adults — American Cancer Society Cancer Prevention Study–3 · doi: 10.1001/jamanetworkopen.2025.2193',
         url='https://pmc.ncbi.nlm.nih.gov/articles/PMC11950897/'),
]


def momentos():
    tarjetas = ''
    for n, e in enumerate(ESTADOS, 1):
        fuente = (f'<a href="{e["url"]}" target="_blank" rel="noopener noreferrer">{e["fuente"]}<span class="screen-reader-text"> (se abre en una pestaña nueva)</span></a>'
                  if e['url'] else e['fuente'])
        tarjetas += f'''<li class="calma-estado" data-estado="{e['slug']}">
<div class="calma-estado__caras">
<div class="calma-estado__frente">
<div class="calma-estado__fig">{e['org']()}</div>
<h3 class="calma-estado__titulo" id="estado-{e['slug']}-titulo">{e['titulo']}</h3>
<p class="calma-estado__pregunta">{e['pregunta']}</p>
<button type="button" class="calma-estado__girar" aria-expanded="false" aria-controls="estado-{e['slug']}" hidden><span class="calma-estado__giro-texto">Ver más<span class="screen-reader-text">: hallazgo sobre {e['titulo'].lower()}</span></span><span class="calma-estado__giro-icono" aria-hidden="true"></span></button>
</div>
<div class="calma-estado__dorso" id="estado-{e['slug']}" role="region" aria-labelledby="estado-{e['slug']}-titulo">
<p class="calma-estado__dato">{e['hallazgo']}</p>
<p class="calma-estado__fuente"><span class="calma-fuente-rotulo">Fuente:</span> {fuente}<br><span class="calma-estado__obra">{e['obra']}</span></p>
<button type="button" class="calma-estado__volver" hidden><span class="calma-estado__giro-texto">Volver<span class="screen-reader-text"> a la pregunta</span></span><span class="calma-estado__giro-icono" aria-hidden="true"></span></button>
</div>
</div>
</li>
'''
    return (cabecera('Inicio · ¿Cómo son tus momentos con la tecnología?',
                     'Reemplaza la fila completa con el título "¿Cómo son tus momentos con la tecnología?" y las 6 tarjetas giratorias (ZoloBlocks).\n'
                     '     Bloque "HTML personalizado" a ancho completo. Borrar también la fila vacía que queda debajo de las 3 tarjetas de acceso.')
            + '''<section class="calma-momentos" aria-labelledby="momentos-titulo">
<div class="calma-momentos__head">
<h2 id="momentos-titulo">¿Cómo son tus momentos con la <em>tecnología</em>?</h2>
<p class="calma-sub">6 escenarios en los que la tecnología y el comportamiento humano se cruzan.</p>
<p class="calma-momentos__ayuda"><span class="calma-momentos__ayuda-icono" aria-hidden="true"></span>Haz clic en las tarjetas para explorar los hallazgos científicos sobre cada tema.</p>
</div>
<ul class="calma-estados" role="list">
''' + tarjetas + '''</ul>
</section>
''')


# --------------------------------------------------------------------------
# Cifras: la visualización acompaña al número, no lo reemplaza.
# --------------------------------------------------------------------------
def rejilla_74():
    # 100 puntos (10 × 10); 74 encendidos. El orden de encendido sigue una
    # onda orgánica desde abajo a la izquierda (--i lo usa la animación).
    rnd = random.Random(74)
    celdas = [(c, f) for f in range(10) for c in range(10)]
    orden = sorted(celdas, key=lambda cf: math.hypot(cf[0], 9 - cf[1]) + rnd.uniform(0, 2.2))
    encendidos = {cf: i for i, cf in enumerate(orden[:74])}
    pts = ''
    for c, f in celdas:
        x, y = 8 + c * 12, 8 + f * 12
        if (c, f) in encendidos:
            pts += f'<circle class="o-on" style="--i:{encendidos[(c, f)]}" cx="{x}" cy="{y}" r="3.4" />'
        else:
            pts += f'<circle class="o-off" cx="{x}" cy="{y}" r="3.4" />'
    return f'<svg class="calma-cifra__viz" viewBox="0 0 124 124" width="124" height="124" aria-hidden="true" focusable="false">{pts}</svg>'


def red_conexiones():
    # Red de nodos que se conectan: "acceder" como estar enlazado.
    rnd = random.Random(6)
    nodos = []
    while len(nodos) < 26:
        x, y = rnd.uniform(10, 150), rnd.uniform(10, 114)
        if all(math.hypot(x - a, y - b) > 17 for a, b in nodos):
            nodos.append((x, y))
    aristas = set()
    for i, (x, y) in enumerate(nodos):
        cerca = sorted(range(len(nodos)), key=lambda j: math.hypot(nodos[j][0] - x, nodos[j][1] - y))[1:3]
        for j in cerca:
            aristas.add(tuple(sorted((i, j))))
    lineas = ''.join(
        f'<line class="o-arista" style="--i:{k}" x1="{nodos[a][0]:.1f}" y1="{nodos[a][1]:.1f}" x2="{nodos[b][0]:.1f}" y2="{nodos[b][1]:.1f}" pathLength="1" />'
        for k, (a, b) in enumerate(sorted(aristas)))
    puntos = ''.join(f'<circle class="o-nodo" style="--i:{i}" cx="{x:.1f}" cy="{y:.1f}" r="2.6" />' for i, (x, y) in enumerate(nodos))
    return f'<svg class="calma-cifra__viz calma-cifra__viz--red" viewBox="0 0 160 124" width="160" height="124" aria-hidden="true" focusable="false">{lineas}{puntos}</svg>'


def cifras():
    return f'''<div class="calma-cifras">
<figure class="calma-cifra">
{rejilla_74()}
<figcaption><strong class="calma-cifra__num">+74 %</strong> de la población global está interactuando con las TIC (Tecnologías de la Información y la Comunicación)</figcaption>
</figure>
<figure class="calma-cifra">
{red_conexiones()}
<figcaption><strong class="calma-cifra__num">+6 mil millones</strong> de personas acceden a Internet</figcaption>
</figure>
<p class="calma-cifras__fuente"><span class="calma-fuente-rotulo">Fuente:</span> {ph('fuente del 74 % y de los 6 mil millones (p. ej. UIT)')}</p>
</div>'''


ILUSTRACION = 'https://codigocalma.com/wp-content/uploads/2026/07/Gemini_Generated_Image_24frf624frf624fr'


def bienvenida():
    # Texto y cifras en una columna, ilustración al lado: sin huecos.
    return (cabecera('Inicio · bienvenida y cifras',
                     'Reemplaza la fila completa "Te damos la bienvenida a Código Calma" (título, texto, ilustración y las dos cajas de cifras).\n'
                     '     Bloque "HTML personalizado" a ancho completo. Texto e ilustración: los mismos que hoy. Falta la fuente de las cifras (docs/placeholders.md).')
            + f'''<section class="calma-bienvenida" aria-labelledby="bienvenida-titulo">
<div class="calma-bienvenida__texto">
<h2 id="bienvenida-titulo">Te damos la bienvenida a <em>Código Calma</em></h2>
<p class="calma-bienvenida__lead">Nuestras decisiones digitales importan. Desde la <strong>ciberpsicología</strong>, te acercamos investigaciones, artículos y herramientas explicadas de forma clara y simple para ayudarte a vivir entre dispositivos en una relación más consciente.</p>
{cifras()}
</div>
<figure class="calma-bienvenida__ilustracion"><img loading="lazy" decoding="async" width="864" height="1219" src="{ILUSTRACION}-726x1024.png" srcset="{ILUSTRACION}-213x300.png 213w, {ILUSTRACION}-726x1024.png 726w, {ILUSTRACION}.png 864w" sizes="(min-width: 900px) 380px, 70vw" alt=""></figure>
</section>
''')


# --------------------------------------------------------------------------
# Línea de tiempo: una línea que crece con el scroll, épocas que se encienden
# y una figura que se transforma (objeto → red → dispositivo → plataforma →
# inteligencia). Texto original de la Etapa 1.
# --------------------------------------------------------------------------
GLIFOS = {
    'objeto': '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M9 20h6M12 16v4"/>',
    'red': '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.5 2.5 2.5 13.5 0 16M12 4c-2.5 2.5-2.5 13.5 0 16"/>',
    'dispositivo': '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
    'plataforma': '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
    'inteligencia': '<circle cx="12" cy="12" r="2.2"/><circle cx="5" cy="7" r="1.6"/><circle cx="19" cy="7" r="1.6"/><circle cx="6" cy="18" r="1.6"/><circle cx="18" cy="17" r="1.6"/><path d="M6.4 7.8l3.8 2.9M17.6 7.8l-3.8 2.9M7.2 17l3.2-3.4M16.6 16.1l-3-2.6"/>',
}

EPOCAS = [
    ('objeto', 'Objeto', '1975–1985', 'Computadora personal', 'La computadora personal (PC) entra en hogares y oficinas. Nace la informática doméstica.'),
    ('red', 'Red', '1990–2000', 'Internet y Web', 'La Web conecta al mundo. Aparecen buscadores, correo y navegación.'),
    ('dispositivo', 'Dispositivo', '2000–2010', 'Móvil y smartphones', 'La conexión se vuelve portátil, constante y personal.'),
    ('plataforma', 'Plataforma', '2010–2020', 'Redes sociales y nube', 'Identidad, vínculos y trabajo migran a plataformas digitales.'),
    ('inteligencia', 'Inteligencia', '2020–hoy', 'IA y hiperconexión', 'La inteligencia artificial transforma mente, emoción y bienestar.'),
]



def linea_tiempo():
    items = ''
    for n, (forma, concepto, anios, nombre, desc) in enumerate(EPOCAS, 1):
        items += f'''<li class="calma-tiempo__epoca" data-forma="{forma}" data-concepto="{concepto}">
<span class="calma-tiempo__punto" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" focusable="false">{GLIFOS[forma]}</svg></span>
<p class="calma-tiempo__anios">{anios}</p>
<h3 class="calma-tiempo__nombre">{nombre}</h3>
<p class="calma-tiempo__desc">{desc}</p>
</li>
'''
    return (cabecera('Inicio · línea de tiempo',
                     'Reemplaza el bloque "HTML personalizado" de la línea de tiempo de la Etapa 1 (sección calma-timeline). Mismo texto.')
            + '''<section class="calma-tiempo" aria-labelledby="tiempo-titulo">
<div class="calma-tiempo__head">
<h2 id="tiempo-titulo">Línea de tiempo: tecnología y adopción</h2>
<p class="calma-sub">Una mirada clara y organizada a cómo la tecnología se integró en la vida humana.</p>
</div>
<div class="calma-tiempo__cuerpo">
<div class="calma-tiempo__figura" aria-hidden="true" hidden><p class="calma-tiempo__anio">1975–1985</p><div class="calma-tiempo__lienzo"></div></div>
<ol class="calma-tiempo__lista">
''' + items + '''</ol>
</div>
</section>
''')


def lecturas_cabecera():
    return (cabecera('Inicio · cabecera de "Lecturas recientes"',
                     'Va justo encima del bloque de entradas (Kadence Posts) del Inicio. Bloque "HTML personalizado".\n'
                     '     La grilla bento la arma calma-etapa7.css sobre el bloque de entradas, sin cambiarlo.')
            + '''<div class="calma-lecturas__head">
<div>
<h2 id="lecturas-titulo">Lecturas <em>recientes</em></h2>
</div>
<a class="calma-link calma-lecturas__todas" href="https://codigocalma.com/blog/">Ver todos los artículos</a>
</div>
''')


(OUT / 'inicio-lecturas-cabecera.html').write_text(lecturas_cabecera(), encoding='utf-8')
(OUT / 'servicios.html').write_text(servicios(cabecera), encoding='utf-8')
(OUT / 'contacto-intro.html').write_text(contacto_intro(cabecera), encoding='utf-8')
(OUT / 'contacto-proceso.html').write_text(contacto_proceso(cabecera), encoding='utf-8')
(OUT / 'herramientas.html').write_text(herramientas(cabecera), encoding='utf-8')
(OUT / 'descargas.html').write_text(descargas(cabecera), encoding='utf-8')
(OUT / 'equipo.html').write_text(equipo(cabecera), encoding='utf-8')
for _slug in PERSONAS:
    (OUT / f'equipo-{_slug}.html').write_text(perfil(cabecera, _slug), encoding='utf-8')
(OUT / 'inicio-mapa.html').write_text(mapa(cabecera), encoding='utf-8')
(OUT / 'inicio-accesos.html').write_text(accesos(cabecera), encoding='utf-8')
(OUT / 'inicio-momentos.html').write_text(momentos(), encoding='utf-8')
(OUT / 'inicio-bienvenida.html').write_text(bienvenida(), encoding='utf-8')
(OUT / 'inicio-linea-de-tiempo.html').write_text(linea_tiempo(), encoding='utf-8')
print('bloques:', ', '.join(p.name for p in sorted(OUT.glob('*.html'))))
