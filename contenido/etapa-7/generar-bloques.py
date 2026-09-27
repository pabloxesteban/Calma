#!/usr/bin/env python3
"""Genera los bloques "HTML personalizado" de la Etapa 7 (dirección de arte
"organismo digital", ver docs/direccion-arte-organismo.md).

  bloques/inicio-momentos.html  → reemplaza la fila "¿Cómo son tus momentos con
                                  la tecnología?" y sus 6 tarjetas giratorias.
  bloques/inicio-cifras.html    → reemplaza las dos cajas de cifras (+74 %,
                                  +6 mil millones) de la fila de bienvenida.

Texto: el mismo que hoy está publicado en el Inicio (no se cambian hallazgos,
fuentes ni cifras). Estilos: plugin codigo-calma, calma-etapa7.css. El
movimiento lo agrega calma-organismo.js; sin JavaScript o con movimiento
reducido, todo el texto se ve y cada figura muestra su estado final.

Ejecutar: python3 contenido/etapa-7/generar-bloques.py
"""
import math, pathlib, random

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
<figure class="calma-estado__fig">{e['org']()}<figcaption class="calma-label">Fig. {n:02d} — {e['concepto']}</figcaption></figure>
<h3 class="calma-estado__titulo">{e['titulo']}</h3>
<p class="calma-estado__pregunta">{e['pregunta']}</p>
<button type="button" class="calma-estado__abrir" aria-expanded="true" aria-controls="estado-{e['slug']}" hidden>Ver el hallazgo<span class="screen-reader-text"> sobre {e['titulo'].lower()}</span></button>
<div class="calma-estado__hallazgo" id="estado-{e['slug']}"><div>
<p>{e['hallazgo']}</p>
<p class="calma-estado__fuente"><span class="calma-label">Fuente</span> {fuente}<br><span class="calma-estado__obra">{e['obra']}</span></p>
</div></div>
</li>
'''
    return (cabecera('Inicio · ¿Cómo son tus momentos con la tecnología?',
                     'Reemplaza la fila completa con el título "¿Cómo son tus momentos con la tecnología?" y las 6 tarjetas giratorias (ZoloBlocks).\n'
                     '     Bloque "HTML personalizado" a ancho completo. Borrar también la fila vacía que queda debajo de las 3 tarjetas de acceso.')
            + '''<section class="calma-momentos" aria-labelledby="momentos-titulo">
<div class="calma-momentos__head">
<p class="calma-eyebrow">Seis estados · Fig. 01–06</p>
<h2 id="momentos-titulo">¿Cómo son tus momentos con la <em>tecnología</em>?</h2>
<p class="calma-sub">6 escenarios en los que la tecnología y el comportamiento humano se cruzan.</p>
<p class="calma-momentos__ayuda">Abre cada tarjeta para explorar el hallazgo científico sobre cada tema.</p>
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
    return (cabecera('Inicio · cifras de la bienvenida',
                     'Reemplaza las dos cajas de información (+74 % y +6 mil millones) de la columna derecha de la fila "Te damos la bienvenida".\n'
                     '     Bloque "HTML personalizado". Falta la fuente de ambas cifras (docs/placeholders.md).')
            + f'''<div class="calma-cifras">
<figure class="calma-cifra">
{rejilla_74()}
<figcaption><strong class="calma-cifra__num">+74 %</strong> de la población global está interactuando con las TIC (Tecnologías de la Información y la Comunicación)</figcaption>
</figure>
<figure class="calma-cifra">
{red_conexiones()}
<figcaption><strong class="calma-cifra__num">+6 mil millones</strong> de personas acceden a Internet</figcaption>
</figure>
<p class="calma-cifras__fuente"><span class="calma-label">Fuente</span> {ph('fuente del 74 % y de los 6 mil millones (p. ej. UIT)')}</p>
</div>
''')


(OUT / 'inicio-momentos.html').write_text(momentos(), encoding='utf-8')
(OUT / 'inicio-cifras.html').write_text(cifras(), encoding='utf-8')
print('bloques:', ', '.join(p.name for p in sorted(OUT.glob('*.html'))))
