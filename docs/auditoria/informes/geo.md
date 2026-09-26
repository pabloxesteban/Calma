# Auditoría GEO — codigocalma.com

**Fecha:** 26-09-2026 · **Alcance:** acceso de crawlers de IA, llms.txt, citabilidad de los 15 artículos, autoría y entidad.
**Material:** `docs/auditoria/snapshot-2026-09-26/` (html, txt, api, robots.txt) y pruebas `curl` de solo lectura contra https://codigocalma.com (26-09-2026, 20:00–20:15 UTC).
**Borradores:** `docs/auditoria/borradores/robots.txt`, `borradores/llms.txt`, `borradores/resumenes-ejemplo.md`.

## 1. Resumen

1. **robots.txt no bloquea a nadie.** Solo tiene `Disallow: /wp-admin/`. La sospecha del cliente sobre robots.txt es infundada.
2. **El firewall sí interviene, y no en el sitio donde se probó al principio.** Las páginas que sirve la caché del CDN (hcdn) devuelven 200 a todos los bots. Pero cuando la petición llega al servidor (página no cacheada, URL con parámetros, 404, `/blog/`, que no se cachea):
   - **GPTBot recibe `429 Too Many Requests` de forma sistemática en `/blog/` y en cualquier URL con parámetros** (36 de 36 intentos), y a veces en archivos y 404. En cambio, OAI-SearchBot y ChatGPT-User, con la misma URL y en el mismo momento, reciben 200 (GEO-01).
   - **Cualquier user-agent, incluido un navegador normal, recibe de forma intermitente un 403** (≈12 % de las peticiones no cacheadas): o una página «403 Forbidden» de LiteSpeed o una pantalla **«Bot Verification» con reCAPTCHA** (`/.lsrecap/recaptcha`). Es lo mismo que vio el auditor de accesibilidad con Playwright en `/blog/` (GEO-02).
3. **El contenido no es citable como está:** ningún artículo abre con un resumen (solo 2 de 15 responden el título en el primer párrafo), **los 15 artículos suman 0 enlaces a fuentes académicas** (DOI/PMC/PubMed/organismos), 7 no tienen ni un H2 y la firma de autora enlaza a una URL **404** (`/codigocalma`).
4. **Lo que está bien:** todo el contenido editorial va en el HTML del servidor (no depende de JS; las tarjetas ZoloBlocks y las animaciones están en el DOM). Las fechas de publicación y de modificación salen en `<time>`, el nombre «Tatiana X. Stacul» es consistente en todo el sitio y la home ya enlaza 5 fuentes (PMC, PubMed, SAGE, Comisión Europea).
5. **Prioridad:** (a) revisar hPanel/soporte por el 429 a GPTBot y el reCAPTCHA; (b) publicar `llms.txt` y el robots.txt explícito; (c) arreglar el enlace y la página de autora; (d) añadir «En resumen», fuentes enlazadas y H2 a los 15 artículos.

## 2. Pruebas de acceso por bot

### 2.1 Método
- `curl` con el UA oficial completo de cada bot (p. ej. `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)`), además de un Chrome de escritorio y un HeadlessChrome como control.
- **A — URLs limpias (5):** `/`, `/robots.txt`, `/la-tecnologia-te-supera-como-identificar-y-gestionar-el-tecnoestres/`, `/wp-json/`, `/feed/`.
- **B — los 15 artículos**, URL canónica (5 UAs).
- **C — artículo con parámetro** para saltarse la caché (`?v=N`, 6 rondas por UA, más 10 rondas alternadas con 5 UAs).
- **D — `/blog/`** (la página se sirve `x-hcdn-cache-status: DYNAMIC`, con `cache-control: no-cache`), 8 peticiones seguidas por UA.
- Cabeceras revisadas: código, tamaño, `server`, `x-hcdn-cache-status`, `x-hcdn-request-id` (nodo del CDN), `x-litespeed-cache`, `retry-after` y el cuerpo (búsqueda de «Bot Verification», «recaptcha», «challenge»).

### 2.2 Resultados

| User-agent | A: URLs limpias (5) | B: 15 artículos | C: artículo con `?param` | D: `/blog/` ×8 | Observación |
|---|---|---|---|---|---|
| Chrome (control) | 200 ×5, mismo tamaño | 15/15 200 | 5/6 200 · 1×403 (+1×403 en ronda alterna) | 7×200 · 1×403 | También se le bloquea a veces |
| HeadlessChrome | — | — | — | 6×200 · 2×403 | Como el control |
| **GPTBot** | 200 ×5 (caché HIT) | 15/15 200 | **0/6 · 6×429** (+10/10×429) | **8×429** | 429, cuerpo vacío, sin `retry-after` |
| OAI-SearchBot | 200 ×5 | 15/15 200 | 6/6 200 | 8×200 | OK |
| ChatGPT-User | 200 ×5 | — | 6/6 200 | 8×200 | OK |
| ClaudeBot | 200 ×5 | 15/15 200 | 6/6 200 (2×403 en ronda alterna, 1×403 en la primera prueba) | 8×200 | Intermitente |
| Claude-User | 200 ×5 | — | 4/6 · 2×403 | 7×200 · 1×403 (reCAPTCHA) | Intermitente |
| Claude-SearchBot | 200 ×5 | — | 3/6 · 3×403 | 7×200 · 1×403 (reCAPTCHA) | Intermitente |
| PerplexityBot | 200 ×5 | 15/15 200 | 4/6 · 2×403 | 7×200 · 1×403 (reCAPTCHA) | Intermitente |
| Perplexity-User | 200 ×5 | — | 4/6 · 2×403 | 6×200 · 2×403 | Intermitente |
| Google-Extended | 200 ×5 | — | 6/6 200 | 8×200 | OK |
| Googlebot | 200 ×5 | — | 6/6 200 | 8×200 | OK |
| bingbot | 200 ×5 | — | 6/6 200 | 8×200 | OK |
| Applebot-Extended | 200 ×5 | — | 5/6 · 1×403 | 7×200 · 1×403 | Intermitente |
| CCBot | 200 ×5 | — | 6/6 200 | 6×200 · 2×403 (1 reCAPTCHA) | Intermitente |
| Bytespider | 200 ×5 | — | 5/6 · 1×403 | 6×200 · 2×403 | Intermitente |

Tamaños en A, iguales para todos los UAs: `/` 214 190 B · `/robots.txt` 116 B · artículo 113 474 B · `/wp-json/` 696 855 B · `/feed/` 80 805 B. `/llms.txt` y `/llms-full.txt` → **404**. `/wp-sitemap.xml` → 200.

### 2.3 Evidencia de los tres tipos de bloqueo

**(1) 429 a GPTBot.** Cabeceras: `HTTP/2 429`, `content-length: 0`, `server: hcdn`, `platform: hostinger`, `panel: hpanel`, sin `x-hcdn-cache-status` ni `x-powered-by`. Se repite en nodos distintos (`bos-edge7`, `imm-edge3`, `mum-edge10`, `phx-…`). Detalles:
- Se activa con `GPTBot/1.1` y `GPTBot/1.2` (UA oficial o corto), pero **no** con la palabra suelta `GPTBot` ni con `Mozilla/5.0 GPT Bot`. Con `gptbot` en minúsculas salió un 403. Todo apunta a una **regla por firma de user-agent** en el CDN o el servidor de Hostinger.
- Afecta a: URLs con parámetros (`/?p=1600`, `/?s=…`, `?utm_source=chatgpt.com`), `/blog/`, 404, `/wp-json/wp/v2/posts?per_page=1` y, de forma variable, archivos (`/2025/02/`, `/blog/page/2/`). Las URLs limpias que ya están en caché (HIT) y algunas MISS (`/servicios/`, `/testimonios/`, `/category/psicologia/`) devuelven 200.
- Por qué importa: `/blog/` es la puerta de entrada a los artículos y no se cachea. Los enlaces que ChatGPT comparte suelen llevar `?utm_source=chatgpt.com`. Y cada artículo nuevo o recién purgado de la caché es un MISS.

**(2) «Bot Verification» (reCAPTCHA de LiteSpeed).** Cabeceras: `HTTP/2 403`, `content-type: text/html`, `cache-control: no-cache,no-store,private`, `x-frame-options: SAMEORIGIN`, `server: hcdn`, sin `platform:`. Cuerpo: `<title>Bot Verification</title>`, «Verifying that you are not a robot...», formulario `action="/.lsrecap/recaptcha?"` y script `recaptcha.net/recaptcha/api.js`. La ruta `/.lsrecap/` corresponde a la **protección reCAPTCHA del servidor web LiteSpeed**, no al plugin LiteSpeed Cache. Ningún crawler de IA resuelve un reCAPTCHA: para ellos esa página es contenido vacío.
- Condiciones observadas: solo en respuestas **no cacheadas** (MISS/DYNAMIC). Aparece en ráfagas de peticiones seguidas desde una misma IP y con cualquier UA, incluidos Chrome y HeadlessChrome. En Playwright, que carga además los recursos de la página, aparece antes (dato del auditor de accesibilidad).

**(3) 403 genérico de LiteSpeed.** «403 Forbidden — Access to this resource on the server is denied!» (787 B), mismas condiciones que (2). Es compatible con un límite de peticiones o con una regla anti-flood por IP.

En esta muestra, Googlebot, bingbot, Google-Extended, OAI-SearchBot y ChatGPT-User **nunca** recibieron 403. Podría haber una lista blanca por UA, pero la muestra (14 peticiones no cacheadas por UA) es pequeña para afirmarlo.

### 2.4 Qué se puede y qué no se puede verificar desde aquí

| Se pudo verificar | No se puede verificar desde aquí |
|---|---|
| robots.txt permisivo (no bloquea a ningún bot) | Cómo trata Hostinger las **IP reales** de OpenAI, Anthropic, Perplexity y Google. Las reglas por IP o ASN, o por «bot verificado», solo se ven con tráfico real |
| El CDN responde distinto según la **firma de UA** (429 a GPTBot) | Si el 429 a GPTBot viene de una opción del cliente en hPanel o de una política global de Hostinger |
| Existe protección reCAPTCHA/403 en el servidor para peticiones no cacheadas | El umbral exacto (peticiones/minuto, reputación de IP). Nuestra salida es una IP de centro de datos compartida, que puede tener peor reputación que la de un visitante |
| El HTML servido a los bots es el mismo que ve una persona (mismo tamaño, sin cloaking) | Si los bots reales se encuentran reCAPTCHA en producción. Eso solo lo dicen los **logs de acceso** |

### 2.5 Qué debe revisar el cliente en hPanel (y cómo confirmarlo)

1. **hPanel → Sitios web → codigocalma.com → Seguridad** y **→ Rendimiento → CDN**: buscar opciones del tipo «Bloqueo/limitación de bots de IA», «AI crawlers», «Bot protection», «Protección DDoS/antibots», «Rate limiting» o «reCAPTCHA». Los nombres cambian con frecuencia. Si GPTBot aparece limitado o bloqueado, **permitirlo**, y dejar permitidos OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended y bingbot.
2. Si no hay opción visible, **abrir un ticket con soporte de Hostinger** y adjuntar esta evidencia: «GPTBot/1.2 recibe 429 en URLs no cacheadas, p. ej. request-id `b67779d5139bc8486413d51150cfa2dd-bos-edge7`; la página `/.lsrecap/recaptcha` (Bot Verification) aparece en `/blog/`, p. ej. `6e4ebb72672e66ffe3e90fc46badcf1d-imm-edge6`». Pedir que (a) excluyan de la limitación a los crawlers de IA verificados y (b) indiquen qué dispara el reCAPTCHA de LiteSpeed y si puede relajarse.
3. **Plugins de seguridad** en WordPress: el snapshot no muestra ninguno, pero conviene confirmarlo en Plugins.
4. **Confirmar en los logs de acceso** (hPanel → Sitios web → Registros / Access logs; descargar varios días):
   ```bash
   grep -E "GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-User|Claude-SearchBot|PerplexityBot|Perplexity-User|Applebot|bingbot" access.log \
     | awk '{ua=$0; sub(/.*compatible; /,"",ua); split(ua,a,"[/;)]"); print a[1], $9}' | sort | uniq -c | sort -rn
   grep -c "/.lsrecap/" access.log        # desafíos reCAPTCHA servidos
   ```
   Lo esperable es mayoría de 200 por bot. Muchos 403/429 confirman el bloqueo. Validar que las IP son de verdad del proveedor comparándolas con los rangos que publica cada uno (openai.com/gptbot.json, searchbot.json, chatgpt-user.json; perplexity.com/perplexitybot.json; anthropic documenta los suyos). Ojo: las respuestas servidas desde la caché del CDN pueden no aparecer en el log del servidor; si hPanel ofrece analíticas o logs del CDN, revisarlos también.
5. **Prueba funcional:** pedir a ChatGPT (con búsqueda), Perplexity y Claude que lean `https://codigocalma.com/blog/` y un artículo reciente, y anotar si citan el contenido o dicen que no pudieron acceder. Repetirlo después de cada cambio.

## 3. Hallazgos

| ID | Hallazgo | Evidencia | Impacto | Esfuerzo | Solución |
|---|---|---|---|---|---|
| GEO-01 | GPTBot recibe 429 en `/blog/`, en URLs con parámetros y a veces en archivos o 404 | §2.3 (1); 36/36 intentos con parámetro o en `/blog/` | **Alto**: páginas nuevas, `/blog/` y enlaces con `utm` no llegan al rastreador de entrenamiento/indexación de OpenAI | Bajo (configuración o ticket) | hPanel/soporte, §2.5. Volver a probar con el comando del §2.1 y revisar logs |
| GEO-02 | reCAPTCHA «Bot Verification» y 403 de LiteSpeed intermitentes (≈12 % de las peticiones no cacheadas, cualquier UA) | §2.3 (2)(3); `/.lsrecap/recaptcha`; coincide con la captura de Playwright | **Alto**: un bot de IA que se topa con el reCAPTCHA indexa o cita una página vacía. También afecta a personas y a pruebas automáticas | Bajo–medio | Pedir a Hostinger que relaje el umbral o que ponga en lista blanca a los bots verificados. Cachear `/blog/` (hoy `no-cache`) reduce la exposición |
| GEO-03 | No existe `/llms.txt` | `curl` → 404 | Medio | Bajo | Subir `borradores/llms.txt` a la raíz tras completar los placeholders |
| GEO-04 | robots.txt sin grupos explícitos para IA | `snapshot/robots.txt` | Bajo (hoy ya permite todo), pero deja constancia de la intención | Bajo | Subir `borradores/robots.txt` como archivo físico. Decidir sobre CCBot/Bytespider |
| GEO-05 | La firma de autora enlaza a una URL 404 y el usuario es `admin` | `a.url.fn.n href="https://codigocalma.com/codigocalma"` → 404; `/wp-json/wp/v2/users` → `slug: "admin"`, `url: …/codigocalma`, `description: ""`; `/?author=1` → `/author/admin/` | **Alto** para E-E-A-T/GEO: la autoría no se puede verificar desde el artículo | Bajo | En Usuarios: cambiar el «Sitio web» del perfil a `https://codigocalma.com/sobre_tatiana/`, completar la biografía y mostrar un nombre público. Idealmente, usuario nuevo con slug `tatiana-x-stacul` (quitar `admin`, que además es un riesgo de seguridad) |
| GEO-06 | 0 enlaces a fuentes académicas en los 15 artículos | Único enlace externo en el cuerpo: cibervoluntarios.org (Infancias). Se citan sin enlace Bandura, Przybylski, Wendy Wood, Kahneman, Skinner, Frontiers in Behavioral Economics, Brandtzaeg et al. (2026), Nielsen 2020, Proyecto Mercury | **Alto**: los motores generativos priorizan afirmaciones verificables; en salud mental, además, es una regla del proyecto | Medio (la autora debe localizar las referencias) | Sección «Fuentes» con DOI/PMC en cada artículo y cita en contexto con año. Cifras sin fuente (tecnoestrés: «70 % de los jóvenes y 56 % de los profesionales») → `[COMPLETAR: fuente]` o retirar |
| GEO-07 | Ningún artículo tiene bloque «En resumen»; solo 2 de 15 responden la pregunta del título en el primer párrafo (4 abren con una anécdota o una introducción genérica) | Tabla §4 | **Alto** (lo primero que extrae un LLM es el primer párrafo) | Medio | Bloque de 40–60 palabras tras el H1, sin cambiar el cuerpo. Ejemplos en `borradores/resumenes-ejemplo.md` |
| GEO-08 | Jerarquía de encabezados débil | 7 artículos con 0 H2 (usan H3 como secciones). Solo 4 H2 en forma de pregunta en todo el blog (3 en «Preguntas clave», 1 en tecnoestrés; «¿Qué es, realmente, la autoeficacia?» es H3) | Medio | Bajo | Pasar los H3 de sección a H2 y reformular como preguntas cuando sea natural. No toca el texto |
| GEO-09 | Sin datos estructurados JSON-LD ni meta description ni Open Graph | 0 `application/ld+json`, 0 `name="description"`, 0 `og:` en home, artículo y Sobre Tatiana. Solo microdatos del tema (`schema.org/Blog`, `WebPage`) | Medio | Medio | Article + Person + Organization (con `sameAs` a LinkedIn). Coordinar con el informe SEO y la skill `schema-markup` |
| GEO-10 | Las páginas pilar no abren con una definición | `/ciberpsicologia/`: «Una parte de la ciberpsicología estudia esa influencia» no define. `/bienestar-digital/`: la definición llega en el 2.º párrafo | Medio | Bajo | Primera oración del tipo «La ciberpsicología es…». Texto a proponer a la autora |
| GEO-11 | Entidad de equipo incompleta | Francisca Cortés Santoro y Emanuel C. Franco solo aparecen en `/servicios/`: sin página propia, sin enlaces ni perfiles. «Sobre Tatiana» vive en `/sobre_tatiana/` (con guion bajo). No hay página de «Código Calma» como organización | Medio | Medio | Página de persona para cada integrante con nombre, rol y bio idénticos en servicios, página, schema y LinkedIn. `[COMPLETAR: perfiles verificables de Francisca y Emanuel]` |
| GEO-12 | Datos citables con errores | Home: «**6M+** · Más de 6 mil millones de personas acceden a Internet» (6M ≠ 6 000 millones) y «74 %+ de la población global…» sin fuente. Título «IA y apoyo emocional: saber la **autoria,** cambia…» (tilde y coma). `/servicios/`: «el día a **day**». Autoeficacia: «microurlogros» | Medio (una IA puede citar la cifra errónea) | Bajo | Corregir (son errores de forma, permitidos por la regla 3) y añadir fuente y año a 74 % y 6 000 M |
| GEO-13 | Fechas visibles sin etiqueta | Los artículos muestran dos fechas seguidas sin «Publicado»/«Actualizado» («19 de julio de 2026 19 de julio de 2026»). 9 artículos con `dateModified` idéntico (2026-06-08 18:09:24), señal de edición masiva sin cambio de contenido | Bajo | Bajo | Etiquetar las fechas en Kadence (Personalizar → Entradas → meta). Solo actualizar `dateModified` ante revisiones reales |
| GEO-14 | Contenido que depende de JS | El test (`/test/`) guarda sus 12 preguntas y los perfiles de resultado en `<script>`, fuera del HTML. Las tarjetas ZoloBlocks (flip-box de la home), las animaciones de Blocks Animation y los listados **sí** están en el HTML | Bajo | Bajo | Añadir en `/test/` un párrafo HTML con las 4 dimensiones que mide y la base del test |
| GEO-15 | Voz inconsistente (voseo/tuteo) | Voseo en `/test/` («Descubrí», «Elegís», «sos»), `/ciberpsicologia/` («Descubrí»), `/herramientas/` («sentís», «procesás») y en «¿Con cuál… conectás más?» (Qué modela). El resto tutea | Bajo para GEO; afecta a la consistencia de marca | Bajo | Unificar en tuteo según las reglas comunes |

## 4. Citabilidad por artículo

Leyenda: ✅ cumple · ⚠️ parcial · ❌ no cumple. «Fuentes» = enlaces externos en el cuerpo (académicos entre paréntesis). «Autoría» = en todos los artículos el nombre es visible, pero el enlace da 404 y no hay rol ni caja de autora, por eso ⚠️. «Fechas» = publicación y modificación visibles en `<time>` (sin etiqueta).

| # | Artículo (slug abreviado) | Resumen inicial | Respuesta directa en el 1.er párrafo | Definición citable | H2 (preguntas) | Fuentes | Autoría | Fechas | Pregunta principal que responde |
|---|---|---|---|---|---|---|---|---|---|
| 1 | por-que-tu-fuerza-de-voluntad… | ❌ | ❌ anécdota | ⚠️ «Tu fuerza de voluntad no es una reserva que se agota; es un sistema dinámico…» (al final) | 0 (4 H3) | ❌ 0 (0) | ⚠️ | ✅ | ¿La fuerza de voluntad se agota como un músculo o una batería? |
| 2 | la-diferencia-entre-querer-y-ser-capaz… | ❌ | ⚠️ nombra «baja percepción de autoeficacia» | ✅ «la autoeficacia es un juicio sobre lo que puedes hacer…» | 0 (5 H3, 2 preguntas) | ❌ 0 (0); Bandura sin enlace | ⚠️ | ✅ | ¿Qué es la autoeficacia y en qué se diferencia de querer hacer algo? |
| 3 | por-que-fallamos-al-intentar-cambiar-conductas | ❌ | ❌ | ⚠️ nombra «paternalismo afectivo», *nudge*/*cudge* sin definirlos | 1 (0) | ❌ 0 (0); Frontiers sin enlace | ⚠️ | ✅ | ¿Por qué no basta con informar o simplificar para cambiar conductas? |
| 4 | ia-y-apoyo-emocional… | ❌ | ❌ anécdota | ❌ | 0 (4 H3) | ⚠️ 0 (0); bibliografía en texto sin enlace (Brandtzaeg et al., 2026) | ⚠️ | ✅ | ¿Cambia la valoración de un consejo emocional si sabemos que lo escribió una IA? |
| 5 | el-estigma-de-la-estructura-x-entonces-y | ❌ | ⚠️ tesis en la 1.ª línea | ⚠️ «el condicional lógico… es la base…» | 0 (5 H3, 1 pregunta) | ❌ 0 (0) | ⚠️ | ✅ | ¿Un texto con estructura lógica indica que lo escribió una IA? |
| 6 | infancias-figitales | ❌ | ⚠️ | ❌ «figital» no se define | 0 (4 H3) | ⚠️ 1 (0): cibervoluntarios.org | ⚠️ | ✅ | ¿Cómo acompañar a infancias que viven sin frontera entre lo digital y lo físico? |
| 7 | calidad-vs-cantidad… | ❌ | ⚠️ | ⚠️ hipótesis descrita en el H2 2 | 3 (0) | ❌ 0 (0); Przybylski sin enlace | ⚠️ | ✅ | ¿Importa más la cantidad de horas de pantalla o la calidad del uso? |
| 8 | autoevaluacion-del-consumo-digital… | ❌ | ✅ define «consumo digital» | ✅ «El consumo digital comprende el tiempo…» | 0 (3 H3, 1 pregunta) | ❌ 0 (0); «diversas investigaciones» sin citar | ⚠️ | ✅ | ¿Cómo evaluar mi consumo digital? |
| 9 | preguntas-clave-para-entender… | ❌ | ✅ | ✅ «La salud cerebral abarca…» | 3 (3) | ❌ 0 (0) | ⚠️ | ✅ | ¿Qué es la salud cerebral y cómo cuidarla? |
| 10 | 5-puntos-clave-caso-de-meta… | ❌ | ⚠️ contexto | ⚠️ Proyecto Mercury descrito | 4 (0) | ❌ 0 (0); Nielsen 2020 y documentos judiciales sin enlace | ⚠️ | ✅ | ¿Qué revela el caso Meta/Proyecto Mercury sobre redes sociales y salud mental? |
| 11 | reflexiones-eticas… IA | ❌ | ❌ intro genérica sobre IA | ✅ «La inteligencia artificial (IA) es un campo multidisciplinario…» | 6 (0) | ❌ 0 (0) | ⚠️ | ✅ | ¿Qué dilemas éticos plantea el desarrollo de la IA? |
| 12 | descubriendo-que-modela-nuestro-comportamiento | ❌ | ⚠️ | ✅ «La ciencia del comportamiento se ocupa del estudio sistemático…» | 4 (0) | ❌ 0 (0); Skinner, Kahneman, Bandura sin enlace | ⚠️ | ✅ | ¿Qué factores modelan nuestro comportamiento? |
| 13 | la-tecnologia-te-supera… tecnoestrés | ❌ | ⚠️ define, pero no resume cómo identificarlo y gestionarlo | ✅ «Este término se refiere al estrés o ansiedad…» | 4 (1) | ❌ 0 (0); 70 %/56 % sin fuente | ⚠️ | ✅ | ¿Qué es el tecnoestrés y cómo identificarlo y gestionarlo? |
| 14 | el-arte-de-redisenar-tu-entorno | ❌ | ⚠️ tesis («no somos nosotros, es nuestro escenario») | ❌ | 1 (0) + 4 H3 | ❌ 0 (0); Wendy Wood sin enlace | ⚠️ | ✅ | ¿Por qué cambiar el entorno funciona mejor que la fuerza de voluntad para cambiar hábitos? |
| 15 | como-un-te-quiero-infecto… | ❌ | ⚠️ hecho (mayo de 2000, 45 M equipos) | ⚠️ ILOVEYOU descrito | 0 (1 H3) | ❌ 0 (0); cifras (45 M, 10 000 M USD) sin fuente | ⚠️ | ✅ | ¿Por qué tanta gente abrió el virus ILOVEYOU? |

Totales: resumen inicial 0/15 · definición citable ✅ 6/15 · artículos con algún H2 en forma de pregunta 2/15 · fuentes académicas enlazadas 0/15 · autoría completa (nombre + rol + enlace válido) 0/15 · fechas 15/15.

## 5. Plan recomendado

1. **Esta semana (sin tocar contenido):** ticket/hPanel (GEO-01, GEO-02); subir robots.txt y llms.txt (GEO-03, GEO-04); corregir el enlace y el slug de autora (GEO-05); corregir las cifras y erratas (GEO-12).
2. **2–4 semanas (con la autora):** «En resumen», H2 y sección «Fuentes» en los 15 artículos, empezando por los de mayor demanda de búsqueda (tecnoestrés, autoeficacia, calidad vs. cantidad, salud cerebral); definiciones en las páginas pilar (GEO-06/07/08/10).
3. **Después:** schema Article/Person/Organization, páginas de equipo y consistencia de voz (GEO-09/11/15). Prueba trimestral en ChatGPT, Perplexity, Gemini y Claude con preguntas de los pilares, registrando si citan el sitio.

## 6. Placeholders abiertos

Registrados en los borradores (no se modificó `docs/placeholders.md` por el alcance de esta tarea; conviene copiarlos allí):
- `[COMPLETAR: matrícula/colegiación profesional, si corresponde]` (llms.txt, Tatiana X. Stacul).
- `[COMPLETAR: URL de su página de persona cuando exista]` ×2 (Francisca Cortés Santoro, Emanuel C. Franco).
- `[COMPLETAR: decisión del cliente]` sobre CCBot/Bytespider (robots.txt).
- `[COMPLETAR: fuente, año y enlace de la estadística 70 % / 56 %]`, `[COMPLETAR: referencias… (DOI/PMC)]`, `[COMPLETAR: referencia de Bandura…]`, `[COMPLETAR: referencia y enlace DOI del trabajo de Przybylski…]` (resumenes-ejemplo.md).
