#!/usr/bin/env python3
"""Genera los bloques "HTML personalizado" de la Etapa 3 a partir del copy
aprobado (contenido/etapa-3/copy.md). Estilos: plugin codigo-calma,
calma-etapa3.css. Ejecutar: python3 contenido/etapa-3/generar-bloques.py"""
import pathlib

OUT = pathlib.Path(__file__).with_name('bloques')
OUT.mkdir(exist_ok=True)
C = 'https://codigocalma.com'

def ph(texto):
    return f'<span class="calma-placeholder">[COMPLETAR: {texto}]</span>'

def avatar(iniciales, nombre, lg=False):
    # Sin foto todavía: iniciales + placeholder visible. Cuando llegue la foto,
    # reemplazar el <span> por <img class="calma-avatar" src=… width="144" height="144" alt="…">.
    return (f'<span class="calma-avatar{" calma-avatar--lg" if lg else ""}" role="img" aria-label="Foto de {nombre} pendiente">{iniciales}</span>')

def cabecera(titulo, instrucciones):
    return f'<!-- Código Calma · {titulo} (Etapa 3)\n     {instrucciones}\n     Texto: contenido/etapa-3/copy.md (pendiente de revisión humana). Estilos: plugin codigo-calma. -->\n'

URGENCIAS_LARGO = (
    '<aside class="calma-notice" aria-labelledby="calma-urgencias">'
    '<p><strong id="calma-urgencias">Si lo que te pasa es urgente.</strong> Código Calma ofrece mentoría y acompañamiento. '
    'No reemplaza la atención psicológica o médica de urgencia. Si estás pasando por una crisis, piensas en hacerte daño o te preocupa alguien cercano, '
    'no esperes nuestra respuesta: llama ahora al número de emergencias de tu país o a una línea de ayuda. '
    + ph('líneas de ayuda por país, verificadas con fuente oficial, y URL de la página de líneas de ayuda') + '</p></aside>')

PERSONAS = [
    dict(slug='tatiana-x-stacul', nombre='Tatiana X. Stacul', corto='Tatiana', ini='TS', etiqueta='Psicología',
         rol='Psicóloga · ciberpsicología y comportamiento', area='habitos',
         enfoque='Mira los hábitos digitales como conductas que el entorno refuerza cada día, no como falta de disciplina.',
         temas=['Desgaste y atención fragmentada en el trabajo digital', 'Hábitos tecnológicos que intentas cambiar y no se sostienen', 'Claridad profesional y próximos pasos'],
         linea='Hábitos digitales, desgaste y atención en el trabajo digital.'),
    dict(slug='francisca-cortes-santoro', nombre='Francisca Cortés Santoro', corto='Francisca', ini='FC', etiqueta='Accesibilidad cognitiva',
         rol='Accesibilidad cognitiva y lenguaje', area='accesibilidad',
         enfoque='Trabaja para que la información no solo se perciba, sino que se entienda.',
         temas=['Lectura fácil y lenguaje claro en webs y documentos', 'Carga cognitiva: qué estorba a quien intenta leer', 'Apoyos a la comunicación y al lenguaje'],
         linea='Lectura fácil, lenguaje claro y carga cognitiva.'),
    dict(slug='emanuel-c-franco', nombre='Emanuel C. Franco', corto='Emanuel', ini='EF', etiqueta='Proyectos',
         rol='Gestión de proyectos y procesos', area='proyectos',
         enfoque='Reconstruye dónde se desbordó un proyecto y le devuelve un alcance que puedas sostener.',
         temas=['Alcance, plazos y prioridades realistas', 'Normativa y procesos que no traben el día a día', 'Reconducir un proyecto que ya está en marcha'],
         linea='Alcance, plazos y procesos que se puedan sostener.'),
]

def lista(items, cls):
    return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def quote(texto, nombre, url):
    return (f'<figure class="calma-card calma-quote"><blockquote><p>«{texto}»</p></blockquote>'
            f'<figcaption><strong>{nombre}</strong> · <a href="{url}" rel="noopener">Ver reseña de {nombre} en Google</a></figcaption></figure>')

# ------------------------------------------------------------------ Servicios
tarjetas = ''
for p in PERSONAS:
    tarjetas += (f'<article class="calma-card calma-person">'
                 f'<div class="calma-person__head">{avatar(p["ini"], p["nombre"])}<div>'
                 f'<span class="calma-badge">{p["etiqueta"]}</span><h3>{p["nombre"]}</h3>'
                 f'<p class="calma-person__role">{p["rol"]}</p></div></div>'
                 f'<p>{p["enfoque"]}</p>'
                 + lista(p['temas'], 'calma-person__topics') +
                 f'<p class="calma-person__links"><a class="calma-btn calma-btn--primary" href="{C}/contacto/?area={p["area"]}">Consultar con {p["corto"]}</a>'
                 f'<a class="calma-link" href="{C}/equipo/{p["slug"]}/">Conocer a {p["corto"]}</a></p>'
                 f'<p class="calma-micro">{ph("foto de " + p["nombre"] + ", 1:1, ≥ 800 px, con texto alternativo")}</p></article>')

faq = [
    ('¿Cuánto dura el acompañamiento?', f'Empieza con un primer encuentro de una hora. Después acordamos un recorrido de tres a seis sesiones. Cada sesión dura {ph("duración de cada sesión")} y las espaciamos {ph("frecuencia habitual entre sesiones")}.'),
    ('¿Cómo son las sesiones?', f'Son online y con una persona por vez. {ph("plataforma de videollamada y si se admiten otras modalidades")} Área de servicio: {ph("países o «online, para personas hispanohablantes»")}.'),
    ('¿Qué pasa en el primer encuentro?', 'Durante una hora entendemos tu contexto y le ponemos un nombre preciso a lo que ocurre. Sales con un objetivo por escrito. Si vemos que lo que necesitas no es un acompañamiento como este, te lo decimos ahí mismo.'),
    ('¿Cuánto cuesta?', ph('honorarios, modalidad de pago y si el primer encuentro tiene costo; o «Te contamos los honorarios en nuestra respuesta, antes de agendar nada»')),
    ('¿Lo que cuento es confidencial?', f'{ph("política de confidencialidad / secreto profesional")} En el formulario te pedimos que no incluyas datos sensibles de salud, porque ese primer mensaje puede leerlo más de una persona del equipo.'),
    ('¿Es psicoterapia?', f'Lo que describimos en esta página es una mentoría: un acompañamiento acotado, con un objetivo y un plan por escrito. No reemplaza un tratamiento psicológico o médico. Si en el primer encuentro vemos que necesitas otro tipo de atención, te lo decimos y te orientamos. {ph("modalidades que ofrece cada profesional (mentoría / psicoterapia) y habilitación profesional correspondiente")}'),
]
faq_html = ''.join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in faq)

servicios = cabecera('Servicios', 'Reemplaza TODO el contenido de la página Servicios (el bloque de la Etapa 1). Un solo bloque "HTML personalizado". Página en ancho completo, sin caja, sin título de Kadence.') + f'''<div class="calma-page">
<section class="calma-hero" aria-labelledby="servicios-titulo">
<div class="calma-hero__inner">
<div>
<p class="calma-eyebrow">Acompañamiento individual</p>
<h1 id="servicios-titulo">Mentoría uno a uno para ordenar tu relación con la tecnología y tu trabajo</h1>
<p class="calma-hero__lead">Una persona por vez, de tres a seis sesiones online, con un plan por escrito para que puedas sostenerlo sin nosotros.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--primary" href="{C}/contacto/">Solicitar una consulta</a><a class="calma-btn calma-btn--secondary" href="#como-trabajamos">Ver cómo trabajamos</a></p>
<p class="calma-micro">Te respondemos en 48 horas hábiles. Honorarios: {ph("honorarios o «te los contamos en la respuesta»")}</p>
{lista(["Una persona por vez", "De tres a seis sesiones", "Online"], "calma-facts")}
</div>
</div>
</section>
<section class="calma-section calma-section--white" aria-labelledby="para-ti">
<div class="calma-container calma-fit">
<div>
<p class="calma-eyebrow">Antes de escribirnos</p>
<h2 id="para-ti">¿Es para ti?</h2>
<p style="margin-top:var(--calma-space-3)">Quizá te reconoces en alguna de estas frases:</p>
{lista(["«Intento cambiar mis hábitos con el móvil y no se sostienen.»", "«Termino el día con la atención partida en mil pestañas.»", "«Quiero ver con claridad cuál es mi próximo paso profesional.»", "«Escribo textos o cuido una web que a mi público le cuesta entender.»", "«Mi proyecto se desbordó y necesito un alcance y unos plazos que pueda sostener.»"], "calma-checklist")}
</div>
<div class="calma-card">
<h3>Cuándo no es para ti</h3>
<p style="margin-top:var(--calma-space-3)">Este acompañamiento no es un servicio de urgencias ni un tratamiento clínico. Si estás pasando por una crisis, o si lo que necesitas es un tratamiento psicológico o médico, te lo decimos con claridad y te orientamos hacia otros recursos. {ph("URL de la página de líneas de ayuda")}</p>
</div>
</div>
</section>
<section class="calma-section calma-section--soft" id="como-trabajamos" aria-labelledby="como-trabajamos-titulo" tabindex="-1">
<div class="calma-container">
<div class="calma-section__head"><p class="calma-eyebrow">Cómo trabajamos</p><h2 id="como-trabajamos-titulo">Qué pasa en cada etapa</h2><p>Lo dejamos escrito aquí para que no tengas que preguntarlo por correo.</p></div>
<ol class="calma-steps">
<li class="calma-card"><div><h3>Nos escribes y cuentas qué te pasa</h3><p>Con unas líneas basta. En 48 horas hábiles te respondemos quién del equipo encaja con lo que traes y qué puedes esperar del primer encuentro.</p><p style="margin-top:var(--calma-space-3)"><strong>Te llevas:</strong> saber con quién hablarías y cómo sería el primer paso.</p></div></li>
<li class="calma-card"><div><h3>Primer encuentro</h3><p>Una hora para entender tu contexto. Si lo que necesitas no es un acompañamiento como este, te lo decimos ahí mismo.</p><p style="margin-top:var(--calma-space-3)"><strong>Te llevas:</strong> un objetivo por escrito.</p></div></li>
<li class="calma-card"><div><h3>De tres a seis sesiones</h3><p>Trabajamos ese objetivo, online. En la última sesión repasamos lo hecho.</p><p style="margin-top:var(--calma-space-3)"><strong>Te llevas:</strong> un plan por escrito, pensado para que puedas sostenerlo sin nosotros.</p></div></li>
</ol>
<p class="calma-actions" style="justify-content:center"><a class="calma-btn calma-btn--primary" href="{C}/contacto/">Empezar por el paso 1</a></p>
<p class="calma-micro" style="text-align:center">Solo te pedimos tu nombre, tu correo y unas líneas.</p>
</div>
</section>
<section class="calma-section calma-section--white" aria-labelledby="equipo-titulo">
<div class="calma-container">
<div class="calma-section__head"><p class="calma-eyebrow">Con quién trabajas</p><h2 id="equipo-titulo">Quién te acompaña, según lo que traigas</h2><p>El recorrido es el mismo en los tres casos. Cambia el terreno.</p></div>
<div class="calma-people">{tarjetas}</div>
</div>
</section>
<section class="calma-section calma-section--soft" aria-labelledby="confianza-titulo">
<div class="calma-container">
<div class="calma-section__head"><p class="calma-eyebrow">Por qué confiar</p><h2 id="confianza-titulo">Quién está detrás y cómo trabajamos</h2></div>
<div class="calma-grid">
<div class="calma-card"><h3>Formación declarada de Tatiana</h3><p style="margin-top:var(--calma-space-3)">Tatiana X. Stacul declara la siguiente formación en ciencias del comportamiento:</p>
{lista([f"Grado en Psicología — {ph('universidad y año')}", f"Máster en Neurociencias — {ph('institución y año')}", f"Coaching Empresarial — {ph('entidad certificadora')}", "Concienciación en ciberseguridad", "Lectura y actualización permanentes en ciberpsicología y riesgo humano"], "calma-person__topics")}
<p class="calma-micro">Colegiación: {ph("matrícula o colegiación profesional (número, colegio, país), si corresponde")} · Francisca y Emanuel: {ph("formación declarada")}</p></div>
<div class="calma-card"><h3>Un enfoque basado en investigación</h3><p style="margin-top:var(--calma-space-3)">Lo que hacemos en las sesiones parte de lo mismo que escribimos en el blog: investigación sobre conducta y tecnología, explicada con claridad. Si quieres ver cómo pensamos, empieza por aquí:</p>
<ul class="calma-person__topics"><li><a href="{C}/por-que-tu-fuerza-de-voluntad-es-mas-lista-de-lo-que-crees/">Por qué tu fuerza de voluntad es más lista de lo que crees</a></li><li><a href="{C}/la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia/">La diferencia entre «querer» y «ser capaz»: entendiendo la autoeficacia</a></li><li><a href="{C}/el-arte-de-redisenar-tu-entorno/">El arte de rediseñar tu entorno</a></li></ul></div>
</div>
<h3 style="margin:var(--calma-space-12) 0 var(--calma-space-2);text-align:center">Lo que cuentan quienes trabajaron con Tatiana</h3>
<p class="calma-micro" style="text-align:center;margin-bottom:var(--calma-space-6)">Reseñas publicadas en Google. Puedes leer cada una completa.</p>
<div class="calma-quotes">
{quote("La confianza que se generó desde el primer día ha sido determinante, he notado un lugar de acogimiento y escucha para mis pensamientos.", "Hugo B.", "https://maps.app.goo.gl/T3GBuKRXATWYKdB68")}
{quote("[…] crear un espacio idóneo donde poder expresarse libremente y ayudarte a encontrar las herramientas para poder lidiar con los temas que se estén tratando.", "Briceida F.", "https://maps.app.goo.gl/qD3mwogm2hTviwpb6")}
{quote("Siempre atenta y predispuesta. Comprensiva y amorosa. A pesar de la distancia, siempre estuvo muy presente en cada sesión.", "Gabriela M.", "https://maps.app.goo.gl/Zwk8rKCshJVoxpxq6")}
</div>
<p class="calma-actions" style="justify-content:center"><a class="calma-link" href="{C}/testimonios/">Ver todos los testimonios</a></p>
<p class="calma-micro" style="text-align:center">Lo que nos cuentas queda entre tú y el equipo. {ph("política de confidencialidad / secreto profesional y enlace a la política de privacidad")}</p>
</div>
</section>
<section class="calma-section calma-section--white" aria-labelledby="faq-titulo">
<div class="calma-container--text">
<div class="calma-section__head"><p class="calma-eyebrow">Preguntas frecuentes</p><h2 id="faq-titulo">Lo que suelen preguntarnos</h2></div>
<div class="calma-faq">{faq_html}</div>
</div>
</section>
<section class="calma-section" aria-labelledby="cierre-titulo">
<div class="calma-container calma-cta">
<h2 id="cierre-titulo">¿Empezamos con calma?</h2>
<p>Cuéntanos en unas líneas qué necesitas. Te respondemos quién encaja mejor y cómo sería el primer encuentro. Si vemos que este no es el lugar, también te lo decimos.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--on-dark" href="{C}/contacto/">Solicitar una consulta</a></p>
<p class="calma-micro">hola@codigocalma.com · Te respondemos en 48 horas hábiles</p>
</div>
{URGENCIAS_LARGO}
</section>
</div>
'''
(OUT / 'servicios.html').write_text(servicios, encoding='utf-8')

# ------------------------------------------------------------------ Inicio · hero
hero = cabecera('Inicio · hero', 'Reemplaza la primera fila del Inicio (fila con "PORTAL DE CIBERPSICOLOGÍA" y la flor). Bloque "HTML personalizado" en ancho completo.') + f'''<section class="calma-hero calma-page" aria-labelledby="inicio-titulo">
<div class="calma-hero__inner calma-hero__inner--media">
<div>
<p class="calma-eyebrow">Portal de ciberpsicología</p>
<h1 id="inicio-titulo">Entiende cómo te afecta la tecnología y decide cómo quieres usarla</h1>
<p class="calma-hero__lead">Artículos, herramientas y acompañamiento uno a uno, basados en investigación y explicados con claridad.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--primary" href="{C}/contacto/">Solicitar una consulta</a><a class="calma-btn calma-btn--secondary" href="{C}/ciberpsicologia/">Explorar recursos gratuitos</a></p>
<p class="calma-micro">Te respondemos en 48 horas hábiles.</p>
</div>
<div class="calma-hero__media"><img src="{C}/wp-content/uploads/2026/05/cropped-logo512-1-300x300.png" srcset="{C}/wp-content/uploads/2026/05/cropped-logo512-1-300x300.png 300w, {C}/wp-content/uploads/2026/05/cropped-logo512-1.png 512w" sizes="(min-width: 900px) 360px, 60vw" width="300" height="300" alt="" fetchpriority="high" decoding="async"></div>
</div>
</section>
'''
(OUT / 'inicio-hero.html').write_text(hero, encoding='utf-8')

# ------------------------------------------------------------------ Contacto · intro
contacto = cabecera('Contacto · intro', 'Reemplaza en Contacto el título, el párrafo, las 3 viñetas y el párrafo en cursiva que están ENCIMA del formulario. El formulario se edita aparte (formulario-contacto.md).') + f'''<div class="calma-page calma-contact-intro">
<h1>¿Cómo podemos ayudarte?</h1>
<p style="margin-top:var(--calma-space-3)">Cuéntanos en unas líneas qué está pasando. Con eso te decimos quién del equipo encaja mejor y cómo sería el primer encuentro.</p>
<h2 style="margin-top:var(--calma-space-8);font-size:var(--calma-fs-lg)">Qué pasa después de enviar</h2>
<ol class="calma-next" style="margin-top:var(--calma-space-4)">
<li><strong>Leemos tu mensaje.</strong> En 48 horas hábiles te respondemos desde hola@codigocalma.com con quién del equipo encaja mejor.</li>
<li><strong>Te proponemos un primer encuentro.</strong> Una hora, online, para entender tu contexto y salir con un objetivo por escrito.</li>
<li><strong>Decides si seguimos.</strong> Si seguimos, trabajamos de tres a seis sesiones. Si vemos que este no es el lugar, te lo decimos y te orientamos.</li>
</ol>
</div>
'''
(OUT / 'contacto-intro.html').write_text(contacto, encoding='utf-8')

# ------------------------------------------------------------------ Equipo
indice_cards = ''.join(
    f'<article class="calma-card calma-person"><div class="calma-person__head">{avatar(p["ini"], p["nombre"])}<div><h2 style="font-size:var(--calma-fs-lg)">{p["nombre"]}</h2>'
    f'<p class="calma-person__role">{p["rol"]}</p></div></div><p>{p["linea"]}</p>'
    f'<p class="calma-person__links"><a class="calma-link" href="{C}/equipo/{p["slug"]}/">Conocer a {p["corto"]}</a></p></article>' for p in PERSONAS)
equipo = cabecera('Equipo', 'Página nueva "Equipo" (slug equipo). Un bloque "HTML personalizado". Ancho completo, sin caja, sin título de Kadence.') + f'''<div class="calma-page">
<section class="calma-hero" aria-labelledby="equipo-h1"><div class="calma-hero__inner"><div>
<h1 id="equipo-h1">El equipo de Código Calma</h1>
<p class="calma-hero__lead">Somos tres personas que miran la tecnología desde lugares distintos: la psicología, la accesibilidad cognitiva y la gestión de proyectos. Trabajamos con el mismo recorrido; cambia el terreno según lo que traigas.</p>
</div></div></section>
<section class="calma-section calma-section--white"><div class="calma-container"><div class="calma-people">{indice_cards}</div></div></section>
<section class="calma-section"><div class="calma-container calma-cta">
<h2>¿No sabes con quién hablar?</h2><p>Escríbenos y te lo decimos nosotros.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--on-dark" href="{C}/contacto/">Solicitar una consulta</a></p>
</div></section>
</div>
'''
(OUT / 'equipo.html').write_text(equipo, encoding='utf-8')

BIOS = {
    'tatiana-x-stacul': ('<p>Tatiana X. Stacul es la psicóloga detrás de Código Calma. Es psicóloga de formación y ciberpsicóloga de vocación. Le interesa cómo la tecnología influye en nuestra conducta y cómo convertir la seguridad digital y la higiene tecnológica en hábitos sostenibles.</p>'
                         f'<p>Comparte contenido basado en su formación en comportamiento. Desde Código Calma propone recursos y contenidos {ph("¿existen talleres? Si existen, añadir «talleres» y enlazarlos")} para ayudarte a comprender y regular, de forma más consciente y saludable, tu relación con el entorno digital.</p>'),
    'francisca-cortes-santoro': ('<p>Francisca trabaja en accesibilidad cognitiva. Parte de una idea sencilla: una web puede cumplir la norma técnica y seguir siendo ilegible para quien más la necesita. Su trabajo se ocupa de esa distancia, para que la información no solo se perciba, sino que se entienda.</p>'
                                 f'<p>{ph("bio de Francisca validada por ella")}</p>'),
    'emanuel-c-franco': ('<p>Emanuel trabaja en gestión de proyectos y procesos. Parte de una observación: casi ningún proyecto se desborda de golpe, sino en decisiones pequeñas que nadie llegó a registrar. Su trabajo es reconstruir dónde ocurrió y devolverle al proyecto un alcance que puedas sostener.</p>'
                         f'<p>{ph("bio de Emanuel validada por él")}</p>'),
}
FORMACION = {
    'tatiana-x-stacul': lista([f"Grado en Psicología — {ph('universidad y año')}", f"Máster en Neurociencias — {ph('institución y año')}", f"Coaching Empresarial — {ph('entidad certificadora')}", "Concienciación en ciberseguridad", "Lectura y actualización permanentes en ciberpsicología y riesgo humano", f"Colegiación: {ph('matrícula o colegiación profesional, si corresponde')}"], 'calma-person__topics')
        + f'<p style="margin-top:var(--calma-space-3)">Perfil: <a href="https://www.linkedin.com/in/tatiana-staculpsi/" rel="noopener">LinkedIn de Tatiana X. Stacul</a> · {ph("ORCID u otro perfil verificable, si existe")}</p>',
    'francisca-cortes-santoro': f'<p>{ph("formación y certificaciones declaradas de Francisca Cortés Santoro")}</p><p>Perfil: {ph("LinkedIn u otro perfil verificable de Francisca")}</p>',
    'emanuel-c-franco': f'<p>{ph("formación y certificaciones declaradas de Emanuel C. Franco")}</p><p>Perfil: {ph("LinkedIn u otro perfil verificable de Emanuel")}</p>',
}
EXTRA_TATIANA = f'''<section class="calma-section calma-section--soft" aria-labelledby="t-opiniones"><div class="calma-container">
<div class="calma-section__head"><h2 id="t-opiniones">Lo que cuentan quienes trabajaron con ella</h2><p>Reseñas publicadas en Google.</p></div>
<div class="calma-quotes">
{quote("No he encontrado nadie tan profesional y cercana.", "Alicia G.", "https://maps.app.goo.gl/xPHGALXoa8mz34K97")}
{quote("[…] siempre está aprendiendo y desarrollando nuevas habilidades porque su curiosidad natural es una de sus mejores cualidades.", "Bárbara C.", "https://maps.app.goo.gl/oNgD7cydBqaxpRiV7")}
{quote("Es sumamente profesional, presta mucha atención a los detalles y combina eso con un gran don de gentes.", "Abdi O.", "https://maps.app.goo.gl/7tzQsKYZ11AR7NXy5")}
</div></div></section>
<section class="calma-section calma-section--white" aria-labelledby="t-articulos"><div class="calma-container--text">
<h2 id="t-articulos">Artículos de Tatiana</h2>
<ul class="calma-person__topics" style="margin-top:var(--calma-space-4)"><li><a href="{C}/descubriendo-que-modela-nuestro-comportamiento/">¿Qué modela nuestro comportamiento?</a></li><li><a href="{C}/la-tecnologia-te-supera-como-identificar-y-gestionar-el-tecnoestres/">La tecnología te supera: cómo identificar y gestionar el tecnoestrés</a></li><li><a href="{C}/por-que-fallamos-al-intentar-cambiar-conductas/">¿Por qué fallamos al intentar cambiar conductas?</a></li></ul>
<p style="margin-top:var(--calma-space-4)"><a class="calma-link" href="{C}/blog/">Ver todos los artículos</a></p>
</div></section>'''

for p in PERSONAS:
    s = p['slug']
    html = cabecera(p['nombre'], f'Página nueva "{p["nombre"]}" hija de Equipo (slug {s}). Un bloque "HTML personalizado". Ancho completo, sin caja, sin título de Kadence.') + f'''<div class="calma-page">
<section class="calma-hero" aria-labelledby="persona-h1"><div class="calma-hero__inner"><div class="calma-person__head" style="gap:var(--calma-space-6);flex-wrap:wrap">
{avatar(p["ini"], p["nombre"], lg=True)}
<div><p class="calma-eyebrow"><a href="{C}/equipo/">Equipo</a></p><h1 id="persona-h1">{p["nombre"]}</h1><p class="calma-person__role" style="font-size:var(--calma-fs-lg)">{p["rol"]}</p>
<p class="calma-micro">{ph("foto profesional de " + p["nombre"] + ", con texto alternativo")}</p></div>
</div></div></section>
<section class="calma-section calma-section--white"><div class="calma-container--text">
{BIOS[s]}
<div class="calma-grid" style="margin-top:var(--calma-space-8)">
<div class="calma-card"><h2 style="font-size:var(--calma-fs-lg)">En qué acompaña</h2>{lista(p["temas"], "calma-person__topics")}</div>
<div class="calma-card"><h2 style="font-size:var(--calma-fs-lg)">Formación declarada</h2>{FORMACION[s]}</div>
</div>
</div></section>
{EXTRA_TATIANA if s == 'tatiana-x-stacul' else ''}
<section class="calma-section"><div class="calma-container calma-cta">
<h2>¿Quieres consultar con {p["corto"]}?</h2>
<p>Te respondemos en 48 horas hábiles. Si vemos que este no es el lugar, también te lo decimos.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--on-dark" href="{C}/contacto/?area={p["area"]}">Consultar con {p["corto"]}</a></p>
</div></section>
</div>
'''
    (OUT / f'equipo-{s}.html').write_text(html, encoding='utf-8')

print('bloques:', sorted(f.name for f in OUT.glob('*.html')))
