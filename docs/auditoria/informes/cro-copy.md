# Auditoría CRO y copy — codigocalma.com

- **Fecha:** 2026-09-26 · **Fase:** diagnóstico (no se modificó el sitio)
- **Agente:** `cro-copywriter` (skill `conversion-page`, `reglas-comunes.md`)
- **Material:** `docs/auditoria/snapshot-2026-09-26/{html,txt}/`, `docs/auditoria/capturas-antes/` (`servicios-390.png`, `contacto-390.png`, `metricas.json`)
- **Estado:** todo el copy propuesto queda **pendiente de revisión humana** por las autoras. Los placeholders `[COMPLETAR: …]` están listados en §7 y hay que pasarlos a `docs/placeholders.md` (este informe no toca otros archivos).

---

## 1. Resumen

La página de servicios ya explica bien la oferta: 3 pasos, 3 profesionales, respuesta en 48 h hábiles y el cierre "¿Empezamos con calma?". Las consultas se pierden **antes y después** de esa página:

1. **El CTA está lejos.** En inicio, el único "Solicitar una consulta" está al final de una página de unos 14.100 px (360 px de ancho). En servicios aparece solo en la caja final, sin CTA en el hero. Los artículos y "Sobre Tatiana" no tienen ninguno.
2. **El formulario frena.** Labels en inglés ("Name", "Message"), botón "Enviar" de bajo contraste, sin consentimiento de privacidad, sin decir qué pasa después y sin aviso de urgencias. Además, el formulario es un **Kadence Advanced Form** (`form#kb-adv-form-2625-cpt-id`) y no Contact Form 7: CF7 está cargado (`wpcf7 = {` en `contacto.html`) pero no se usa. Esto cambia dónde se editan los textos.
3. **No se captan emails.** Hay dos imanes listos (test, descargas) pero ningún formulario de suscripción.
4. **La voz no es coherente.** Tuteo en servicios y artículos, voseo en el test y en herramientas, y "Bienvenidos" en plural en inicio.
5. **Hay prueba social real, pero escondida.** `/testimonios/` tiene 14 testimonios, cada uno enlazado a una reseña de Google Maps. En cambio, los 2 de "Sobre Tatiana" no tienen fuente.

**Prioridad 1 (poco esfuerzo, mucho impacto):** CRO-01, 02, 03, 04, 05 y 08.

---

## 2. Recorrido actual hasta la consulta

| Origen | Recorrido en móvil (390 px) | Clics o toques | Observación |
|---|---|---|---|
| Inicio | Scroll hasta el final (unos 14.000 px, tras la línea de tiempo y los 6 escenarios) → "Solicitar una consulta" → `/contacto/` | 1 clic + scroll muy largo | CTA con contraste 2,32:1 (blanco sobre `#64B2E5`, `metricas.json`) |
| Inicio (menú) | ☰ → Contacto | 2 | No hay botón fijo de consulta en el header |
| Inicio → Servicios | ☰ → Servicios → scroll hasta la caja final (unos 3.400 px de 3.779 en `servicios-390.png`) → CTA → formulario | 3 + scroll | No hay CTA en el hero. El texto del CTA (`#334155` sobre `#64B2E5`) da unos 4,4:1, al límite |
| Artículo | No hay CTA. Opciones: ☰ → Contacto / Servicios | 2–3 | Sin puente entre el tema del artículo y el servicio (p. ej. "fuerza de voluntad" → Tatiana) |
| Sobre Tatiana | No hay CTA. Solo "Más testimonios" | 2 (menú) | Es la página de mayor intención y no tiene salida a la consulta |
| Test (resultado) | "Contactanos →" → `/contacto/` | 1 | El único CTA en contexto, pero con voseo y sin decir qué ocurre después |
| Formulario | 3 campos, "Enviar" | 1 | Sin consentimiento, sin mensaje de "qué pasa después", sin aviso de urgencias |

Hay 2 páginas con CTA de consulta (`grep -c "Solicitar una consulta"`: home 1, servicios 1; sobre_tatiana, blog y artículos 0).

---

## 3. Hallazgos

Impacto y esfuerzo: A = alto, M = medio, B = bajo.

| ID | Hallazgo y evidencia | Impacto | Esfuerzo | Solución |
|---|---|---|---|---|
| CRO-01 | Labels en inglés "Name"/"Message", pequeñas y dentro de la caja (`contacto.html` l. 281–289, `contacto-390.png`). Nombre no obligatorio. Sin `autocomplete` | A | B | Labels en español visibles fuera del campo, `autocomplete="name"/"email"`, nombre obligatorio (copy en §6.3) |
| CRO-02 | Sin consentimiento de privacidad ni enlace a la política en el formulario | A (confianza y legal) | B | Casilla obligatoria con enlace a la [COMPLETAR: URL política de privacidad] |
| CRO-03 | No se dice qué pasa tras enviar. Las 48 h solo aparecen en servicios (`servicios.txt` l. 63) | A | B | Texto bajo el botón y mensaje de éxito con plazo y siguiente paso (§6.3) |
| CRO-04 | El CTA de inicio está al final y con contraste 2,32:1. No hay CTA en el hero | A | B | Hero con CTA primario "Solicitar una consulta" + secundario "Explorar recursos". Botón con texto oscuro o fondo más oscuro (≥ 4,5:1), alto ≥ 48 px (§6.1) |
| CRO-05 | El hero de servicios no tiene CTA. El único está a unos 3.400 px | A | B | CTA primario en el hero, repetido tras "Cómo trabajamos", tras el equipo y al final (§6.2) |
| CRO-06 | Los artículos no tienen caja CTA ni suscripción al final. Solo "Compartir" y navegación (`por-que-fallamos…txt` l. 71) | A | M | Caja CTA temática + bloque de newsletter (§6.4 y §6.5) |
| CRO-07 | Sin newsletter pese a las integraciones de Kadence (MailerLite/FluentCRM/GetResponse) | A (a medio plazo) | M | Formulario solo con email + consentimiento, doble opt-in, en final de artículo, footer, `/descargas-2/` y resultado del test (§6.5) |
| CRO-08 | No hay aviso de urgencias en ninguna página (servicios, contacto, test, artículos de salud mental) | A (ética) | B | Aviso breve en contacto, servicios, test y pie de artículos (§6.6) |
| CRO-09 | "Sobre Tatiana" no tiene CTA de consulta ni menciona el servicio. Es la única página de equipo y no hay fotos del equipo | M–A | B/M | CTA "Consultar con Tatiana" (`/contacto/?area=habitos`), enlace a servicios. Fotos [COMPLETAR: fotos del equipo]. Páginas de Francisca y Emanuel [COMPLETAR: bio verificada] |
| CRO-10 | Prueba social: `/testimonios/` tiene 14 testimonios con nombre + inicial y cada uno enlaza a Google Maps (`maps.app.goo.gl/…`). Parecen reales y verificables. En cambio, "Luis R." y "Ana M." (`sobre_tatiana.txt` l. 31–32) **no están en /testimonios/**, no tienen enlace a la fuente y sus fotos son `luisr.jpg`/`anam.jpg` | M | B | Usar 2–3 de los 14 verificables en servicios y en Sobre Tatiana, con enlace "Ver reseña en Google". Retirar Luis R./Ana M. hasta confirmar su origen [COMPLETAR: fuente y consentimiento de Luis R. y Ana M.] |
| CRO-11 | Los testimonios hablan de "terapia", "terapeuta", "mi psicóloga" (l. 18, 27, 33, 39), mientras servicios presenta "mentoría y acompañamiento" | M | B | Aclarar en servicios la diferencia entre mentoría y psicoterapia (FAQ) y si Tatiana también ofrece psicoterapia [COMPLETAR: modalidades reales y habilitación] |
| CRO-12 | Voz incoherente: voseo en test y herramientas, "Bienvenidos" en plural en inicio, tuteo en el resto | M | B | Unificar en tuteo (ver §5, errores V-*) |
| CRO-13 | Faltan honorarios, duración y precio de la sesión, y FAQ en servicios | M | B (copy) | FAQ de 4–6 preguntas con [COMPLETAR: honorarios / modalidad de pago] |
| CRO-14 | El hero de inicio no dice qué ofrece ni para quién. La frase de la l. 23–25 no tiene verbo principal | M | B | Nuevo H1 y subtítulo (§6.1) |
| CRO-15 | "Recursos gratuitos" en inicio enlaza a `/descargas/`, pero la página es `/descargas-2/` (`home.html`) | M | B | Apuntar a `/descargas-2/` o crear una redirección 301 (y valorar renombrar el slug a `/descargas/`) |
| CRO-16 | Las descargas no piden email. Títulos con formato de archivo ("Ansiedad-Funcional-vs-Ansiedad-Desbordada") | M | M | Mantener acceso libre y ofrecer suscripción opcional junto al botón. Corregir los títulos (§5) |
| CRO-17 | En el formulario el área se pide en texto libre (`contacto.txt` l. 22–30). Tres preguntas en viñetas generan una sensación de "deberes" | M | M | Campo opcional "Área" preseleccionable por `?area=`. Reemplazar las viñetas por una sola ayuda (§6.3) |
| CRO-18 | No se ve ningún evento de conversión. Anti-spam: no se ve honeypot ni Turnstile en el HTML | M | M | Evento `generate_lead` al enviar con éxito si hay analítica [COMPLETAR: herramienta de analítica]. Honeypot o Turnstile sin CAPTCHA visual |
| CRO-19 | El resultado del test no ofrece ni consulta ni suscripción de forma clara ("Contactanos →" y "Volver a jugar →") | M | B | CTA primario "Recibir ideas para aplicar tu resultado" (email) + secundario "Solicitar una consulta" |
| CRO-20 | Categorías incoherentes: "¿Por qué fallamos al intentar cambiar conductas?" aparece en "Ciberseguridad" | B | B | Recategorizar en Psicología / Comportamiento (propuesta a la autora) |

---

## 4. Lista completa de errores de texto

Leyenda: O = ortografía o tilde, P = puntuación, V = voz o registro, I = inglés mezclado, C = cifra o coherencia. Los extractos en listados (inicio, blog, relacionados) heredan la corrección del artículo.

| # | Archivo:línea | Tipo | Texto actual | Corrección propuesta |
|---|---|---|---|---|
| 1 | home.txt:28–29 | C | "6M+" / "Más de 6 mil millones" | "+6.000 M" o "+6 mil millones" |
| 2 | home.txt:26 | C | "74%+" | "+74 %" (y citar la fuente [COMPLETAR: fuente del 74 %, p. ej. UIT]) |
| 3 | home.txt:21 | V | "Bienvenidos a" | "Te damos la bienvenida a" (o eliminar, ver §6.1) |
| 4 | home.txt:23 | P | "Nuestras decisiones digitales, importan." | "Nuestras decisiones digitales importan." (sin coma entre sujeto y verbo) |
| 5 | home.txt:23–25 | P/C | "Desde la ciberpsicología a través de investigaciones… para ayudarte" (no tiene verbo) | "Desde la ciberpsicología, te acercamos investigaciones, artículos y herramientas explicadas de forma clara…" |
| 6 | home.txt:61,68; blog/entradas/relacionados; ia-y-apoyo…:1,19 | O/P | "saber la autoria, cambia tu perspectiva" | "saber la autoría cambia tu perspectiva" (tilde y sin coma entre sujeto y verbo) |
| 7 | home.txt:66 (extracto) | P | "dos respuestas posibles…." | "dos respuestas posibles…" |
| 8 | servicios.txt:58 | I | "el día a day" | "el día a día" |
| 9 | contacto.txt:32,35 | I | "Name", "Message" | "¿Cómo te llamas?", "Cuéntanos qué te trae" (§6.3) |
| 10 | contacto.txt:18–20 | C | "ayudart / e" (salto en el H1 en el txt; en la captura se ve bien) | Revisar el marcado del H1 (posible `<span>`/`<mark>` que corta la palabra y afecta a lectores de pantalla) |
| 11 | test.txt:20 | V | "Descubrí cómo es tu relación…" | "Descubre cómo es tu relación…" |
| 12 | test.txt:27,30,33 | V | "Elegís / Respondés / Obtenés" | "Eliges / Respondes / Obtienes" |
| 13 | test.txt:38–39 | V | "¿De qué generación sos? / Elegí la que…" | "¿De qué generación eres? / Elige la que…" |
| 14 | test.txt:61 | V | "Contactanos →" | "Solicitar una consulta →" |
| 15 | test.txt:62 | C | "Volver a jugar →" | "Repetir el test" (el test se presenta como reflexivo, no como juego) |
| 16 | test.txt:41–51 | C | Solo 3 generaciones (sin Baby boomers ni Alfa) | Proponer "Otra / prefiero no decirlo" |
| 17 | herramientas.txt:33–34 | V | "lo que sentís… cómo procesás" | "lo que sientes… cómo procesas" |
| 18 | herramientas.txt:54 | V | "elegís cómo te sentiste" | "eliges cómo te sentiste" |
| 19 | herramientas.txt:24–25 | C | "Bloque HTML personalizado" / "═══ -->" (restos de código visibles en el texto) | Eliminar el comentario HTML mal cerrado |
| 20 | herramientas.txt:52 | I | "Diario, hábitos & rastreo" | "Diario, hábitos y seguimiento" |
| 21 | herramientas.txt:56 | O | "Ejercicio de respiración" (describe varios) | "Ejercicios de respiración" |
| 22 | ciberpsicologia.txt:19 | P | Dobles espacios: "cómo  nos", "día.  Una" | Un espacio |
| 23 | ciberpsicologia.txt:24–25 | C | "S / elección de recursos" | Revisar la letra capital (lectores de pantalla leen "S elección") |
| 24 | ciberpsicologia.txt:32 | V | "Descubrí tu relación con la tecnología." | "Descubre tu relación con la tecnología." |
| 25 | bienestar-digital.txt:28 | O | "El objetivo final, quizas, una vida…" | "El objetivo final: quizás, una vida…" |
| 26 | descargas-2.txt:21 | C | "Ansiedad-Funcional-vs-Ansiedad-Desbordada" | "Ansiedad funcional vs. ansiedad desbordada" |
| 27 | descargas-2.txt:25 | O | "Guia de Ciberseguridad para Psicologos" | "Guía de ciberseguridad para psicólogos" (o "para profesionales de la psicología") |
| 28 | descargas-2.txt:29 | P | "Psicología para devs>" | "Psicología para devs" |
| 29 | descargas-2.txt:33–36 | I | "The Psychology of Trust…" en inglés sin aviso | Añadir "(en inglés)" |
| 30 | descargas-2.txt:18–19 | C | "Libros de descarga gratuita" (son guías o e-books) | "Guías de descarga gratuita" (a confirmar con la autora) |
| 31 | sobre_tatiana.txt:20–21 | P | "…ciberpsicóloga de vocación, me fascina…" (arranca con coma tras el salto) | "Psicóloga de formación y ciberpsicóloga de vocación. Me fascina…" |
| 32 | sobre_tatiana.txt:28–29 | C | "Te invito a explorar recursos, talleres y contenidos" (no hay página de talleres) | Quitar "talleres" o enlazarlos [COMPLETAR: ¿hay talleres?] |
| 33 | testimonios.txt:18 | P | Cierra con comillas de apertura: "…más profundos. «" | "…más profundos.»" |
| 34 | testimonios.txt:27 | O | "a la practica… lo mas valioso" | "a la práctica… lo más valioso" |
| 35 | testimonios.txt:33 | O | "muchisímo… acesibilidad… Gracias Tatiana!" | "muchísimo… accesibilidad… ¡Gracias, Tatiana!" |
| 36 | testimonios.txt:24 | O | "aún sin estar programada" | "aun sin estar programada" |
| 37 | testimonios.txt:39 | O | "en el cuál… dejando KAO… escuchad@ y comprendid@" | "en el cual… dejando KO… escuchado/a" |
| 38 | testimonios.txt:42 | C | "mientras desarrolles ser una mejor persona… Me ha ayudado enfrentar" | "a ser… Me ha ayudado a enfrentar" |

Los testimonios (33–38) son citas de terceros: corregir solo con permiso o marcar [sic]. Lo prudente es copiar el texto tal como está en Google.

| # | Archivo:línea | Tipo | Texto actual | Corrección propuesta |
|---|---|---|---|---|
| 39 | ia-y-apoyo…txt:51 | P | "…al plano emocional, La pregunta deja de ser "¿puede la IA responder bien?". Sino más bien "¿Cómo…"" | "…al plano emocional. La pregunta deja de ser «¿puede la IA responder bien?» y pasa a ser «¿cómo…?»" |
| 40 | ia-y-apoyo…txt:48 | P | "muchas críticas hacia la IA, frialdad, distancia, falta de personalización, aparecían" | "…hacia la IA (frialdad, distancia, falta de personalización) aparecían" |
| 41 | ia-y-apoyo…txt:59 | O | "Bibliografia:" | "Bibliografía:" |
| 42 | ia-y-apoyo…txt:60 | P/C | "…advice Vol.20,No.2(2026) Petter Bae Brandtzaeg , Marita…" | "Brandtzaeg, P. B., Skjuve, M. y Følstad, A. (2026). *Effects of author disclosure…* [COMPLETAR: revista], 20(2). DOI" |
| 43 | por-que-tu-fuerza…txt:39 | O | "Si, la creencia importa" | "Sí, la creencia importa" |
| 44 | por-que-tu-fuerza…txt:45 | C | "En Código Calma no buscamos entendernos." (contradice el sentido del texto) | Preguntar a la autora. Posible: "no buscamos exigirnos más, sino entendernos" |
| 45 | por-que-tu-fuerza…txt:56–57 | V | "como director… ¿Eres de los que se rinden…?" (masculino genérico) | "Y tú tienes la última palabra." / "¿Te rindes o negocias con tu cerebro?" (propuesta) |
| 46 | la-diferencia…txt:38 | O | "(La fuente reina)" | "(la fuente reina)" |
| 47 | la-diferencia…txt:45 | P | "¿Cómo interpretas tu pulso acelerado o tus manos sudorosas." | "…manos sudorosas?" |
| 48 | la-diferencia…txt:57 | O | "microurlogros" | "micrologros" |
| 49 | la-diferencia…txt:62–64 | C | "[ Por qué tu fuerza de voluntad… ]" (corchetes visibles alrededor del enlace) | Quitar los corchetes y dejar solo el enlace |
| 50 | la-diferencia…txt:51 | V | "Estoy cansado" (masculino) | Opcional: "Tengo cansancio" (a criterio de la autora) |
| 51 | infancias-figitales.txt:30–31 | P | "Viven en un mundo integrado Sus amistades" | "…integrado. Sus amistades" |
| 52 | infancias-figitales.txt:64–66 | P | "Sé el modelo de «Desconexión Consciente «:" | "Sé el modelo de «desconexión consciente»:" |
| 53 | infancias-figitales.txt:75 | I | "Te dejamos el link hacia sus proyectos:" + URL desnuda | "Te dejamos el enlace a sus proyectos: Proyectos de Cibervoluntarios" (con texto de enlace) |
| 54 | infancias-figitales.txt:62 | O | «Silencio Digital» | «silencio digital» |
| 55 | como-un-te-quiero…txt:19 | O | "Cómo un «Te quiero» Infectó 45 millones…" | "Cómo un «te quiero» infectó 45 millones…" |
| 56 | como-un-te-quiero…txt:27 | P/O | "LOVE-LETTER-FOR-YOU.TXT.Vbs" / "ciberpsicología,  fue" | "LOVE-LETTER-FOR-YOU.TXT.vbs" / un solo espacio |
| 57 | el-estigma…txt:29 | P | "“Esto lo escribió una IA” .¿La prueba" | "«Esto lo escribió una IA». ¿La prueba" |
| 58 | el-estigma…txt:39 | P | "autenticidad.Hoy" | "autenticidad. Hoy" |
| 59 | el-estigma…txt:40–45 | P | Mayúsculas irregulares tras los dos puntos ("si la IA…", "Es más fácil…") | Unificar en minúscula tras dos puntos |
| 60 | autoevaluacion…txt:93 | P | "eliminar la tecnología , lo cual" | "eliminar la tecnología, lo cual" |
| 61 | por-que-fallamos…txt:18 | C | Categoría "Ciberseguridad" | "Psicología" (ver CRO-20) |
| 62 | por-que-fallamos…txt:37 | O | "El Nudge simplifica…" | "El *nudge* simplifica…" (cursiva y minúscula, igual que en el resto del texto) |
| 63 | Varios títulos (blog.txt:83,105,115) | O | Mayúsculas de estilo inglés: "Calidad vs. Cantidad: La Hipótesis de Ricitos de Oro", "Preguntas Clave para Entender…", "5 Puntos Clave que el Caso de Meta Nos Deja…" | "Calidad vs. cantidad: la hipótesis de Ricitos de Oro", "Preguntas clave para entender y cuidar nuestro cerebro", "5 puntos clave que el caso de Meta nos deja en salud mental" |
| 64 | Varios | V/I | Comillas mezcladas (“ ” y « ») | Unificar en « » (lo más usado en el sitio) |

---

## 5. Coherencia de voz (resumen)

- **Tuteo** (la voz de marca): servicios, contacto, artículos. Se mantiene.
- **Voseo**: test (líneas 20–39, 61), herramientas (33, 34, 54), ciberpsicología (32). Se pasa a tuteo (errores 11–14, 17, 18, 24).
- **Plural**: "Bienvenidos" (home:21). Se reemplaza.
- **Primera persona singular vs. plural**: Sobre Tatiana ("soy", "te invito") y los artículos ("me encontré") frente a servicios ("trabajamos"). Es coherente (autora vs. equipo). Mantener, pero en los CTA de artículos hablar como equipo e indicar qué profesional.

---

## 6. Propuestas de copy (pendiente de revisión de las autoras)

### 6.1 Hero de inicio
**Versión breve**
- Eyebrow: PORTAL DE CIBERPSICOLOGÍA
- H1: **Entiende cómo te afecta la tecnología y decide cómo quieres usarla**
- Subtítulo: Artículos, herramientas y acompañamiento uno a uno, basados en investigación y explicados con claridad.
- CTA primario: **Solicitar una consulta** → `/contacto/` · Secundario: **Explorar recursos gratuitos** → `/ciberpsicologia/`
- Microcopy bajo los botones: Te respondemos en 48 horas hábiles.

**Versión larga (subtítulo)**: Desde la ciberpsicología te acercamos investigaciones, artículos y herramientas claras para vivir entre pantallas con más calma. Si prefieres hacerlo acompañado, trabajamos contigo uno a uno.

*Por qué:* dice qué y para quién en 5 segundos (claridad), pone el CTA sin scroll a 390 px (fricción) y quita "Bienvenidos" y el problema de sintaxis. Las cifras 74 % / 6.000 M bajan debajo del hero, ya corregidas y con fuente.

### 6.2 Hero de servicios
- Eyebrow: ACOMPAÑAMIENTO INDIVIDUAL
- H1: **Mentoría uno a uno para ordenar tu relación con la tecnología y tu trabajo**
- Subtítulo: Una persona por vez, de tres a seis sesiones online, con un plan por escrito para que puedas sostenerlo sin nosotros.
- CTA primario: **Solicitar una consulta** · Secundario: **Ver cómo trabajamos** (ancla a #como-trabajamos)
- Datos de encuadre (se mantienen): Una persona por vez · De tres a seis sesiones · Online
- Línea de confianza: Respondemos en 48 horas hábiles · Honorarios: [COMPLETAR: honorarios o "te los contamos en la respuesta"]
- Repetir el CTA tras "Cómo trabajamos" ("Empezar por el paso 1") y en cada profesional: "Consultar con Tatiana" (`?area=habitos`), "Consultar con Francisca" (`?area=accesibilidad`), "Consultar con Emanuel" (`?area=proyectos`).
- Bloque nuevo "¿Es para ti?": Es para ti si… "Intento cambiar hábitos digitales y no se sostienen" · "Siento la atención fragmentada todo el día" · "Mi proyecto se desbordó y no sé por dónde empezar". **No es para ti si** necesitas atención urgente o un tratamiento clínico: en ese caso te orientamos hacia otros recursos.

*Por qué:* el H1 actual ("Mentorías y acompañamiento uno a uno") dice el formato pero no el resultado. El CTA en el hero ahorra unos 3.400 px de scroll.

### 6.3 Formulario de consulta
Encabezado: **¿Cómo podemos ayudarte?**
Intro (sustituye las 3 viñetas): Cuéntanos en unas líneas qué está pasando. Con eso te decimos quién del equipo encaja mejor y cómo sería el primer encuentro.

| Campo | Label visible | Ayuda / placeholder | Obligatorio | Técnico |
|---|---|---|---|---|
| Nombre | ¿Cómo te llamas? | — | Sí | `autocomplete="name"` |
| Email | ¿A qué correo te respondemos? | Solo lo usamos para responderte. | Sí | `type="email"`, `autocomplete="email"` |
| Área | ¿Sobre qué quieres consultar? | Hábitos digitales y comportamiento · Accesibilidad cognitiva · Gestión de proyectos · Todavía no lo sé | No | radio, preselección por `?area=` |
| Mensaje | Cuéntanos qué te trae | Con unas líneas basta. Por favor, evita incluir datos sensibles de salud: este mensaje puede leerlo más de una persona del equipo. | Sí | 3–4 filas |
| Consentimiento | He leído la [política de privacidad] y acepto que usen mis datos para responder a mi consulta. | — | Sí | enlace [COMPLETAR: URL política] |

- **Botón:** Enviar mi consulta
- **Bajo el botón:** Te respondemos en 48 horas hábiles. Si vemos que este no es el lugar, también te lo decimos.
- **Aviso de urgencias** (ver §6.6, versión breve) justo antes del botón.
- **Éxito (en pantalla):** **Recibimos tu mensaje, [nombre].** Te respondemos en 48 horas hábiles desde hola@codigocalma.com con quién del equipo encaja mejor y cómo sería el primer encuentro. Si no lo ves, revisa la carpeta de spam. Mientras tanto, puedes [hacer el test de consumo digital].
- **Email automático** (asunto): Recibimos tu consulta — Código Calma. Cuerpo: el mismo texto de éxito + "Si lo que te pasa es urgente, no esperes nuestra respuesta: [COMPLETAR: líneas de ayuda]".
- **Errores (bajo cada campo):**
  - Nombre vacío: Escribe tu nombre para que sepamos cómo llamarte.
  - Email vacío o mal escrito: Revisa el correo; parece que falta algo (ejemplo: nombre@correo.com).
  - Mensaje vacío: Cuéntanos al menos en una línea qué te trae.
  - Consentimiento: Para responderte necesitamos que aceptes la política de privacidad.
  - Error general (sustituye "errores para continuar"): No pudimos enviar tu mensaje. Revisa los campos marcados o escríbenos directamente a hola@codigocalma.com.
  - Fallo del servidor: Algo falló de nuestro lado. Inténtalo en unos minutos o escríbenos a hola@codigocalma.com.

*Por qué:* labels en español y visibles (accesibilidad y claridad), 5 campos como máximo (fricción), plazo y siguiente paso explicados (confianza). Los textos se editan en el bloque Kadence Advanced Form 2625, no en CF7.

### 6.4 Caja CTA al final de un artículo
Plantilla (un solo CTA de consulta por artículo, adaptado a la categoría):
> **¿Te identificas con esto?**
> Tatiana acompaña procesos de cambio de hábitos digitales, uno a uno y online. En unas líneas nos cuentas qué te pasa y te respondemos en 48 horas hábiles.
> **[Solicitar una consulta]** (`/contacto/?area=habitos`) · [Ver cómo trabajamos](/servicios/)

Variantes: gestión de proyectos o procesos (p. ej. "¿Por qué fallamos…") → "Emanuel ayuda a equipos a reconducir procesos que no se sostienen." (`?area=proyectos`). Accesibilidad y lenguaje → "Francisca revisa webs y documentos para que se entiendan." (`?area=accesibilidad`).
Pie en artículos de salud mental: aviso de urgencias, versión breve (§6.6).

### 6.5 Bloque newsletter
- **Título:** Una reflexión breve sobre bienestar digital, cada [COMPLETAR: frecuencia real, p. ej. 15 días]
- **Texto:** Ideas basadas en investigación para usar la tecnología con más intención. Sin spam y sin prisas: puedes darte de baja cuando quieras.
- **Campo:** Tu correo electrónico (label visible) · **Botón:** Quiero recibirla
- **Consentimiento:** Acepto recibir el boletín y la [política de privacidad]. · Doble opt-in.
- **Tras enviar:** Revisa tu correo y confirma la suscripción. Si no lo ves en unos minutos, mira en spam.
- **Confirmado:** Listo, ya estás dentro. Mientras llega la primera reflexión, aquí tienes las [guías gratuitas](/descargas-2/).
- **Variante en el resultado del test:** ¿Quieres ideas concretas para tu perfil? Te enviamos una reflexión breve cada [COMPLETAR: frecuencia].
- **Variante en descargas:** La guía es gratis y no te pedimos nada. Si quieres recibir las próximas, deja tu correo.
- **Proveedor:** [COMPLETAR: MailerLite / FluentCRM / GetResponse] (ya hay integraciones de Kadence).

Nada de pop-ups de entrada ni cuentas regresivas.

### 6.6 Aviso de urgencias
- **Breve (formulario, test, pie de artículo):** Este espacio no es un servicio de urgencias. Si estás en crisis o en riesgo, contacta ahora con los servicios de emergencia de tu país. [Ver líneas de ayuda]
- **Largo (servicios y página de recursos):** Código Calma ofrece mentoría y acompañamiento; no reemplaza la atención psicológica o médica de urgencia. Si estás pasando por una crisis, piensas en hacerte daño o te preocupa alguien cercano, no esperes nuestra respuesta: llama al número de emergencias de tu país o a una línea de ayuda. [COMPLETAR: líneas de ayuda por país (España, Argentina, México, Chile, Colombia…), verificadas con fuente oficial]

---

## 7. Placeholders para registrar en `docs/placeholders.md`

1. [COMPLETAR: honorarios / modalidad de pago] — servicios, FAQ
2. [COMPLETAR: líneas de ayuda por país, verificadas] — aviso de urgencias, email automático
3. [COMPLETAR: proveedor de email] — newsletter
4. [COMPLETAR: frecuencia real del boletín] — newsletter
5. [COMPLETAR: URL de la política de privacidad] — formulario, newsletter
6. [COMPLETAR: fotos del equipo] y [COMPLETAR: bio verificada de Francisca y Emanuel]
7. [COMPLETAR: fuente y consentimiento de Luis R. y Ana M.]; confirmar el consentimiento para reutilizar las reseñas de Google en otras páginas
8. [COMPLETAR: modalidades reales (mentoría / psicoterapia) y habilitación profesional]
9. [COMPLETAR: fuente del 74 %] (cifras de inicio)
10. [COMPLETAR: revista y DOI del estudio Brandtzaeg et al. 2026]
11. [COMPLETAR: herramienta de analítica para `generate_lead`]
12. [COMPLETAR: ¿existen talleres?] (Sobre Tatiana)
