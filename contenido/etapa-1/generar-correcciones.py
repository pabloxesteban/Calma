#!/usr/bin/env python3
"""Genera correcciones.json (fuente única de las correcciones de texto y
encabezados de la Etapa 1). Lo usan la guía de implementación y la vista
previa (staging/preview). Ejecutar: python3 contenido/etapa-1/generar-correcciones.py"""
import json, pathlib

C = []
def add(id, tipo, paginas, donde, antes, despues, html_buscar=None, html_reemplazar=None, origen='', nota=''):
    C.append({k: v for k, v in dict(id=id, tipo=tipo, paginas=paginas, donde=donde, antes=antes, despues=despues,
             html_buscar=html_buscar, html_reemplazar=html_reemplazar, origen=origen, nota=nota).items() if v not in (None, '')})

TODAS = ['*']
MARK2 = '<mark style="background-color:rgba(0, 0, 0, 0)" class="has-inline-color has-theme-palette-2-color">'

# ---------------------------------------------------------------- Títulos de entradas
# Se cambian en el campo Título de cada entrada. El slug (URL) NO se toca.
tit = [
 ('T01', 'IA y apoyo emocional: saber la autoria, cambia tu perspectiva', 'IA y apoyo emocional: saber la autoría cambia tu perspectiva', 'CRO #6'),
 ('T02', 'La diferencia entre «querer» y «ser capaz»: Entendiendo la autoeficacia', 'La diferencia entre «querer» y «ser capaz»: entendiendo la autoeficacia', 'CRO #63'),
 ('T03', 'Calidad vs. Cantidad: La Hipótesis de Ricitos de Oro', 'Calidad vs. cantidad: la hipótesis de Ricitos de Oro', 'CRO #63'),
 ('T04', 'Autoevaluación del Consumo Digital: ¿Cómo estamos manejando nuestro tiempo frente a las pantallas?', 'Autoevaluación del consumo digital: ¿cómo estamos manejando nuestro tiempo frente a las pantallas?', 'CRO #63'),
 ('T05', 'Preguntas Clave para Entender y Cuidar Nuestro Cerebro', 'Preguntas clave para entender y cuidar nuestro cerebro', 'CRO #63'),
 ('T06', '5 Puntos Clave que el Caso de Meta Nos Deja en Salud Mental', '5 puntos clave que el caso de Meta nos deja en salud mental', 'CRO #63'),
 ('T07', 'Reflexiones Éticas sobre el Desarrollo de la Inteligencia Artificial', 'Reflexiones éticas sobre el desarrollo de la inteligencia artificial', 'CRO #63'),
 ('T08', 'La tecnología te supera: Cómo identificar y gestionar el tecnoestrés', 'La tecnología te supera: cómo identificar y gestionar el tecnoestrés', 'CRO #63'),
 ('T09', 'Cómo un «Te quiero» Infectó 45 millones de computadoras en todo el mundo', 'Cómo un «te quiero» infectó 45 millones de computadoras en todo el mundo', 'CRO #55'),
]
for id, a, d, o in tit:
    add(id, 'titulo', TODAS, 'Entradas > editar la entrada > campo Título (no cambiar el enlace permanente)', a, d, origen=o,
        nota='Aparece también en el inicio, el blog, las relacionadas y el <title>.')

# ---------------------------------------------------------------- Inicio
add('I01', 'encabezado', ['home'], 'Inicio > bloque Advanced Heading "PORTAL DE CIBERPSICOLOGÍA…" > Nivel: de H4 a P (párrafo)',
    'H4 «PORTAL DE CIBERPSICOLOGÍA…»', 'Párrafo (eyebrow, sin cambiar estilo)',
    '<h4 class="kt-adv-heading1204_179e11-cf', '<p class="kt-adv-heading1204_179e11-cf', origen='A11Y-07',
    nota='El cierre </h4> de ese bloque pasa a </p> (lo hace el editor al cambiar el nivel).')
add('I02', 'encabezado+texto', ['home'], 'Inicio > Advanced Heading "Bienvenidos a Código Calma" > Nivel H2 → H1 y texto',
    'H2 «Bienvenidos a Código Calma»', 'H1 «Te damos la bienvenida a Código Calma»',
    '<h2 class="kt-adv-heading1204_e36b0d-85 wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading1204_e36b0d-85">Bienvenidos a ' + MARK2 + 'Código Calma</mark></h2>',
    '<h1 class="kt-adv-heading1204_e36b0d-85 wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading1204_e36b0d-85">Te damos la bienvenida a ' + MARK2 + 'Código Calma</mark></h1>',
    origen='SEO-10, CRO #3', nota='Única H1 de la página. El hero con propuesta de valor llega en la Etapa 3.')
add('I03', 'texto', ['home'], 'Inicio > párrafo bajo la bienvenida',
    'Nuestras decisiones digitales, importan. Desde la ciberpsicología a través de investigaciones, artículos y herramientas explicadas de forma clara y simple para ayudarte a vivir entre dispositivos en una relación más consciente.',
    'Nuestras decisiones digitales importan. Desde la ciberpsicología, te acercamos investigaciones, artículos y herramientas explicadas de forma clara y simple para ayudarte a vivir entre dispositivos en una relación más consciente.',
    'Nuestras decisiones digitales, importan. Desde la <strong>ciberpsicología</strong> a través de investigaciones',
    'Nuestras decisiones digitales importan. Desde la <strong>ciberpsicología</strong>, te acercamos investigaciones',
    origen='CRO #4, #5', nota='Sin coma entre sujeto y verbo; la frase tenía el verbo principal ausente.')
add('I04', 'texto', ['home'], 'Inicio > Info Box de estadística 1 > título', '74%+', '+74 %',
    '<h3 class="kt-blocks-info-box-title"><strong>74%+</strong></h3>', '<h3 class="kt-blocks-info-box-title"><strong>+74 %</strong></h3>',
    origen='CRO #2', nota='Falta la fuente: ver placeholders (Etapa 5 agrega la cita).')
add('I05', 'texto', ['home'], 'Inicio > Info Box de estadística 2 > título y texto',
    '6M+ / Más de 6 mil millones de personas acceden a Internet', '+6 mil millones / de personas acceden a Internet',
    '<h3 class="kt-blocks-info-box-title">6M+</h3><p class="kt-blocks-info-box-text">Más de 6 mil millones de personas acceden a Internet</p>',
    '<h3 class="kt-blocks-info-box-title">+6 mil millones</h3><p class="kt-blocks-info-box-text">de personas acceden a Internet</p>',
    origen='CRO #1, SEO-22, GEO-12', nota='"6M" significa 6 millones, no 6 mil millones.')
add('I06', 'encabezado', ['home'], 'Inicio > Advanced Heading "¿Cómo son tus momentos con la tecnología?" > Nivel H1 → H2',
    'H1', 'H2', '<h1 class="kt-adv-heading1580_3776ad-7d', '<h2 class="kt-adv-heading1580_3776ad-7d', origen='SEO-10, A11Y-07',
    nota='El cierre del bloque pasa a </h2>.')
add('I07', 'encabezado', ['home'], 'Inicio > encabezado "6 escenarios en los que…" > Nivel H6 → Párrafo',
    'H6 «6 escenarios…»', 'Párrafo', '<h6 class="wp-block-heading has-text-align-center">6 escenarios', '<p class="has-text-align-center calma-sub">6 escenarios',
    origen='A11Y-07')

# ---------------------------------------------------------------- Contacto
add('C01', 'encabezado+texto', ['contacto'], 'Contacto > Advanced Heading "¿Cómo podemos ayudarte?" > Nivel H2 → H1; borrar el texto y escribirlo de nuevo (hay negritas que parten la palabra "ayudarte")',
    'H2 «¿Cómo podemos ayudart|e|?» (con <strong> que corta la palabra)', 'H1 «¿Cómo podemos ayudarte?»',
    '<h2 class="kt-adv-heading790_ebf638-02 wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading790_ebf638-02"><strong>¿Cómo podemos ayudart</strong>e<strong>?</strong> </h2>',
    '<h1 class="kt-adv-heading790_ebf638-02 wp-block-kadence-advancedheading" data-kb-block="kb-adv-heading790_ebf638-02">¿Cómo podemos ayudarte?</h1>',
    origen='SEO-10, CRO #10')

# ---------------------------------------------------------------- Test
test = [
 ('E01', 'Descubrí cómo es tu relación con la tecnología en 5 minutos', 'Descubre cómo es tu relación con la tecnología en 5 minutos', 'CRO #11'),
 ('E02', '<strong>Elegís tu generación</strong>', '<strong>Eliges tu generación</strong>', 'CRO #12'),
 ('E03', '<strong>Respondés 12 preguntas</strong>', '<strong>Respondes 12 preguntas</strong>', 'CRO #12'),
 ('E04', '<strong>Obtenés tu perfil</strong>', '<strong>Obtienes tu perfil</strong>', 'CRO #12'),
 ('E05', '¿De qué generación sos?', '¿De qué generación eres?', 'CRO #13'),
 ('E06', 'Elegí la que mejor te representa', 'Elige la que mejor te representa', 'CRO #13'),
 ('E07', 'Contactanos →', 'Solicitar una consulta →', 'CRO #14'),
 ('E08', 'Volver a jugar →', 'Repetir el test', 'CRO #15'),
 ('E09', 'te quedás sin batería, ¿cómo te sentís?', 'te quedas sin batería, ¿cómo te sientes?', 'CRO §5 (voseo en preguntas del test)'),
 ('E10', '<h1 style="color:#4F86C6">Test de Consumo Digital</h1>', '<h1 style="color:#1d5f94">Test de consumo digital</h1>', 'CRO #63, A11Y-05'),
]
for id, a, d, o in test:
    add(id, 'texto', ['test'], 'Test > bloque HTML personalizado del test (buscar el texto con Ctrl+F en el editor de código)', a, d, origen=o)

# ---------------------------------------------------------------- Herramientas / Ciberpsicología / Bienestar / Descargas / Sobre
add('H01', 'texto', ['herramientas'], 'Herramientas > bloque HTML personalizado > tarjeta "Llevar un diario"',
    'Escribir lo que sentís activa el pensamiento reflexivo.\n        Cinco minutos al día pueden cambiar cómo procesás el estrés.',
    'Escribir lo que sientes activa el pensamiento reflexivo.\n        Cinco minutos al día pueden cambiar cómo procesas el estrés.', origen='CRO #17')
add('H02', 'texto', ['herramientas'], 'Herramientas > texto de la app de diario (Daylio)', 'elegís cómo te sentiste', 'eliges cómo te sentiste', origen='CRO #18')
add('H03', 'texto', ['herramientas'], 'Herramientas > encabezado de sección', 'Diario, hábitos &amp; rastreo', 'Diario, hábitos y seguimiento', origen='CRO #20')
add('H04', 'texto', ['herramientas'], 'Herramientas > descripción de Mindfulness Coach', 'Ejercicio de respiración, relajación y rastreo de síntomas.', 'Ejercicios de respiración, relajación y seguimiento de síntomas.', origen='CRO #21')
add('P01', 'texto', ['ciberpsicologia'], 'Ciberpsicología > Info Box "Test de consumo digital"', 'Descubrí tu relación con la tecnología.', 'Descubre tu relación con la tecnología.', origen='CRO #24')
add('P02', 'texto', ['ciberpsicologia'], 'Ciberpsicología > párrafo introductorio (dobles espacios)', 'cómo  nos relacionamos y qué decisiones tomamos cada día.  Una parte', 'cómo nos relacionamos y qué decisiones tomamos cada día. Una parte', origen='CRO #22')
add('B01', 'texto', ['bienestar-digital'], 'Bienestar digital > Info Box "Bienestar Humano"', 'El objetivo final, quizas, una vida donde', 'El objetivo final: quizás, una vida donde', origen='CRO #25')
add('B02', 'encabezado', ['bienestar-digital'], 'Bienestar digital > Advanced Heading "La intersección" > Nivel H1 → H2', 'H1', 'H2', '<h1 class="kt-adv-heading1604_8f6d6d-41', '<h2 class="kt-adv-heading1604_8f6d6d-41', origen='SEO-10')
add('B03', 'encabezado', ['bienestar-digital'], 'Bienestar digital > Advanced Heading "Primeros pasos hacia la calma" > Nivel H1 → H2', 'H1', 'H2', '<h1 class="kt-adv-heading1604_247975-2f', '<h2 class="kt-adv-heading1604_247975-2f', origen='SEO-10')
add('D01', 'texto', ['descargas-2'], 'Descargas > imagen de la guía 1 > Texto alternativo', 'alt="Ansiedad-Funcional-vs-Ansiedad-Desbordada"', 'alt="Portada de la guía Ansiedad funcional vs. ansiedad desbordada"', origen='CRO #26')
add('D02', 'texto', ['descargas-2'], 'Descargas > imagen de la guía 2 > Texto alternativo', 'alt="Guia de Ciberseguridad para Psicologos"', 'alt="Portada de la Guía de ciberseguridad para psicólogos"', origen='CRO #27')
add('D03', 'texto', ['descargas-2'], 'Descargas > título de la guía 3', 'Psicología para devs&gt;</h3>', 'Psicología para devs</h3>', origen='CRO #28')
add('D04', 'texto', ['descargas-2'], 'Descargas > título de la guía 4', 'The Psychology of Trust</h3>', 'The Psychology of Trust (en inglés)</h3>', origen='CRO #29')
add('D05', 'encabezado', ['descargas-2'], 'Descargas > Advanced Heading "Libros de descarga gratuita" > Nivel H2 → H1', 'H2', 'H1', '<h2 class="kt-adv-heading1666_f0c6ba-66', '<h1 class="kt-adv-heading1666_f0c6ba-66', origen='SEO-10',
    nota='El texto ("Libros" vs. "Guías") queda para confirmar con la autora (CRO #30).')
add('S01', 'texto', ['sobre_tatiana'], 'Sobre Tatiana > párrafo de presentación', '<strong>Psicóloga de formación y ciberpsicóloga de vocación</strong>, me fascina', '<strong>Psicóloga de formación y ciberpsicóloga de vocación.</strong> Me fascina', origen='CRO #31')

# ---------------------------------------------------------------- Artículos (solo ortografía y puntuación; el texto de la autora no cambia)
art = [
 ('A01', 'ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva', 'Bibliografia', 'Bibliografía', None, None, 'CRO #41'),
 ('A02', 'ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva', 'deja el plano técnico para pasar al plano emocional, La pregunta deja de ser “¿puede la IA responder bien?”. Sino más bien “¿Cómo interpreta una persona que la respuesta provenga de algo que no siente?”.',
    'deja el plano técnico para pasar al plano emocional. La pregunta deja de ser «¿puede la IA responder bien?» y pasa a ser «¿cómo interpreta una persona que la respuesta provenga de algo que no siente?».', None, None, 'CRO #39'),
 ('A03', 'ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva', 'muchas críticas hacia la IA, frialdad, distancia, falta de personalización, aparecían', 'muchas críticas hacia la IA (frialdad, distancia, falta de personalización) aparecían', None, None, 'CRO #40'),
 ('A04', 'por-que-tu-fuerza-de-voluntad-es-mas-lista-de-lo-que-crees', 'Si, la creencia importa', 'Sí, la creencia importa', None, None, 'CRO #43'),
 ('A05', 'la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia', '(La fuente reina)', '(la fuente reina)', None, None, 'CRO #46'),
 ('A06', 'la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia', 'tu pulso acelerado o tus manos sudorosas. ¿Es miedo', 'tu pulso acelerado o tus manos sudorosas? ¿Es miedo', None, None, 'CRO #47'),
 ('A07', 'la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia', 'microurlogros', 'micrologros', None, None, 'CRO #48'),
 ('A08', 'la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia', '[Por qué tu fuerza de voluntad es más lista de lo que crees]', 'Por qué tu fuerza de voluntad es más lista de lo que crees (sin corchetes)',
    '[<strong>Por qué tu fuerza de voluntad es más lista de lo que crees</strong>]', '<strong>Por qué tu fuerza de voluntad es más lista de lo que crees</strong>', 'CRO #49'),
 ('A09', 'infancias-figitales', 'Viven en un mundo integrado (sin punto final)', 'Viven en un mundo integrado.',
    'Viven en un mundo <strong>integrado</strong></p>', 'Viven en un mundo <strong>integrado</strong>.</p>', 'CRO #51'),
 ('A10', 'infancias-figitales', 'Sé el modelo de «Desconexión Consciente«:', 'Sé el modelo de «desconexión consciente»:',
    '«Desconexión ' + MARK2 + 'Consciente</mark>«:', '«desconexión ' + MARK2 + 'consciente</mark>»:', 'CRO #52'),
 ('A11', 'infancias-figitales', '«Silencio Digital»', '«silencio digital»', None, None, 'CRO #54'),
 ('A12', 'infancias-figitales', 'Te dejamos el link hacia sus proyectos: https://www.cibervoluntarios.org/…', 'Te dejamos el enlace a sus proyectos: Proyectos de Cibervoluntarios',
    'Te dejamos el link hacia sus proyectos: <a href="https://www.cibervoluntarios.org/es/que-hacemos/proyectos">https://www.cibervoluntarios.org/es/que-hacemos/proyectos</a>',
    'Te dejamos el enlace a sus proyectos: <a href="https://www.cibervoluntarios.org/es/que-hacemos/proyectos">Proyectos de Cibervoluntarios</a>', 'CRO #53'),
 ('A13', 'como-un-te-quiero-infecto-45-millones-de-computadoras-en-todo-el-mundo', 'LOVE-LETTER-FOR-YOU.TXT.Vbs', 'LOVE-LETTER-FOR-YOU.TXT.vbs', None, None, 'CRO #56'),
 ('A14', 'como-un-te-quiero-infecto-45-millones-de-computadoras-en-todo-el-mundo', 'ciberpsicología,  fue', 'ciberpsicología, fue', None, None, 'CRO #56'),
 ('A15', 'el-estigma-de-la-estructura-x-entonces-y', '“Esto lo escribió una IA”.¿La prueba', '«Esto lo escribió una IA». ¿La prueba',
    '<em>“Esto lo escribió una IA”</em>.¿La prueba', '<em>«Esto lo escribió una IA»</em>. ¿La prueba', 'CRO #57'),
 ('A16', 'el-estigma-de-la-estructura-x-entonces-y', 'autenticidad.Hoy', 'autenticidad. Hoy', None, None, 'CRO #58'),
 ('A17', 'autoevaluacion-del-consumo-digital-como-estamos-manejando-nuestro-tiempo-frente-a-las-pantallas', 'eliminar la tecnología , lo cual', 'eliminar la tecnología, lo cual', None, None, 'CRO #60'),
 ('A18', 'por-que-fallamos-al-intentar-cambiar-conductas', 'El Nudge simplifica', 'El <em>nudge</em> simplifica', None, None, 'CRO #62'),
]
for id, slug, a, d, hb, hr, o in art:
    add(id, 'texto', [slug], 'Entrada > editor de bloques (buscar el texto)', a, d, hb, hr, origen=o)

# Extractos de listados heredan las correcciones de los artículos:
add('X01', 'texto', TODAS, 'Automático: extracto del artículo en listados (se corrige al editar la entrada)', 'dos respuestas posibles….', 'dos respuestas posibles…',
    'dos respuestas posibles&#8230;.</p>', 'dos respuestas posibles&#8230;</p>', origen='CRO #7', nota='El extracto sale del primer párrafo de la entrada "IA y apoyo emocional…": quitar el punto extra después de los puntos suspensivos.')
add('X02', 'texto', TODAS, 'Automático: extracto de "Infancias «Figitales»" en listados (se corrige con A09)', 'Viven en un mundo integrado Sus amistades', 'Viven en un mundo integrado. Sus amistades', origen='CRO #51')

# ---------------------------------------------------------------- Taxonomía (interino hasta la Etapa 5)
add('K01', 'categoria', ['por-que-fallamos-al-intentar-cambiar-conductas', 'blog', 'entradas', 'home'], 'Entradas > "¿Por qué fallamos al intentar cambiar conductas?" > Categorías: quitar Ciberseguridad, marcar Psicología',
    'Ciberseguridad', 'Psicología', origen='CRO-20, SEO-24',
    nota='Interino: la taxonomía completa se rehace en la Etapa 5.')

# ---------------------------------------------------------------- Excluidas a propósito (necesitan a la autora o permiso)
EXCLUIDAS = [
 ('CRO #44', 'por-que-tu-fuerza…: "no buscamos entendernos" parece decir lo contrario de lo que se quiere', 'Preguntar a la autora'),
 ('CRO #45, #50', 'Masculino genérico ("como director", "Estoy cansado")', 'Decisión de estilo de la autora'),
 ('CRO #30', '"Libros de descarga gratuita" → ¿"Guías"?', 'Confirmar con la autora'),
 ('CRO #32', '"talleres" en Sobre Tatiana', '[COMPLETAR: ¿existen talleres?]'),
 ('CRO #33–38', 'Ortografía en testimonios', 'Son citas de terceros: corregir solo con permiso o marcar [sic]'),
 ('CRO #42', 'Formato de la bibliografía de Brandtzaeg et al.', 'Etapa 5 (fuentes), falta la revista'),
 ('CRO #64', 'Unificar comillas “ ” → « »', 'Etapa 5, al reestructurar cada artículo'),
 ('CRO #10, #19, #23', '"ayudart/e", "═══ -->", "S / elección"', 'Falsos positivos de la extracción de texto, salvo "ayudart/e" (corregido en C01): el comentario HTML y la letra capital no se ven en pantalla'),
]

out = pathlib.Path(__file__).with_name('correcciones.json')
out.write_text(json.dumps({'version': 'etapa-1', 'correcciones': C,
    'excluidas': [dict(origen=a, que=b, motivo=c) for a, b, c in EXCLUIDAS]}, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(C), 'correcciones ->', out)

# ---------------------------------------------------------------- Versión legible
NOMBRES = {'home': 'Inicio', 'contacto': 'Contacto', 'test': 'Test de consumo digital', 'herramientas': 'Herramientas',
           'ciberpsicologia': 'Ciberpsicología', 'bienestar-digital': 'Bienestar digital', 'descargas-2': 'Descargas',
           'sobre_tatiana': 'Sobre Tatiana', '*': 'Todo el sitio (títulos y extractos)'}
def celda(t):
    return str(t).replace('|', '\\|').replace('\n', ' ')
md = ['# Correcciones de texto y encabezados — Etapa 1', '',
      'Generado desde `correcciones.json` (no editar a mano; editar `generar-correcciones.py`).',
      'Regla: solo se corrigen errores y niveles de encabezado; el texto de las autoras no cambia.', '']
grupos = {}
for c in C:
    clave = c['paginas'][0] if len(c['paginas']) == 1 else c['paginas'][0]
    grupos.setdefault(clave, []).append(c)
for clave, items in grupos.items():
    md += [f'## {NOMBRES.get(clave, clave)}', '', '| ✓ | ID | Tipo | Dónde | Antes | Después | Nota |', '|---|---|---|---|---|---|---|']
    for c in items:
        md.append(f"| ☐ | {c['id']} | {c['tipo']} | {celda(c['donde'])} | {celda(c['antes'])} | {celda(c['despues'])} | {celda(c.get('origen',''))}{' — ' + celda(c['nota']) if c.get('nota') else ''} |")
    md.append('')
md += ['## Excluidas a propósito', '', '| Origen | Qué | Motivo |', '|---|---|---|']
md += [f'| {a} | {celda(b)} | {celda(m)} |' for a, b, m in EXCLUIDAS]
out.with_name('correcciones.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print('correcciones.md generado')
