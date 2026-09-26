# Auditoría SEO técnica y on-page — codigocalma.com

- **Fecha:** 2026-09-26 · **Autor:** subagente `seo-specialist` · **Fase:** solo diagnóstico (no se modificó nada en el sitio ni en el repo fuera de este informe).
- **Material:** `docs/auditoria/snapshot-2026-09-26/` (28 HTML, txt, API REST, robots.txt) + `curl` de solo lectura contra producción el 2026-09-26.
- **Stack:** WordPress 7.1.2 · Kadence 1.5.2 · Kadence Blocks 3.7.11.1 · ZoloBlocks 2.7.12 · Blocks Animation · CF7 6.1.7 · AddToAny · LiteSpeed Cache + CDN Hostinger (hcdn) · PHP 8.3 · sin plugin SEO.
- **Core Web Vitals:** la API de PageSpeed Insights respondió **429 (cuota diaria agotada)**. Los datos de rendimiento son **estimaciones desde el HTML** y deben medirse con PSI/Lighthouse mobile antes de cerrar la etapa.

## 1. Resumen ejecutivo

La base técnica es sana: HTTPS con 301, host único sin www, caché LiteSpeed + CDN con Brotli, `lang="es"`, canonical autorreferente en páginas y entradas, búsqueda interna con `noindex` y 404 reales. El problema es que **faltan casi todas las señales on-page que controla un plugin SEO**: ninguna de las 28 URLs tiene meta description, Open Graph, Twitter Card ni JSON-LD; `/blog/` y los archivos no tienen canonical; y los `<title>` de los artículos son el H1 + marca (13 de 15 pasan de 60 caracteres, hasta 113).

Cinco problemas pesan más que el resto:
1. **Enlace de autor roto en todo el blog:** el nombre "Tatiana X. Stacul" enlaza a `https://codigocalma.com/codigocalma` (**404**) en los 15 artículos, `/blog/` y los archivos (17 de 28 HTML). Viene del campo "Sitio web" del usuario 1. Corregirlo lleva 1 minuto y además refuerza E-E-A-T, que importa en un tema de salud mental (YMYL).
2. **Contenido duplicado y slugs mal formados:** `/blog/` (página de entradas nativa, está en el sitemap) y `/entradas/` (página con bloque, es la que enlaza el menú "Blog") muestran lo mismo. A eso se suman `sobre_tatiana` (`/sobre-tatiana/` da 404) y `descargas-2`, que existe porque el adjunto 1839 ocupa el slug `descargas`.
3. **Encabezados rotos:** 6 páginas no tienen H1. La home tiene 2, y uno de ellos sale de un **documento HTML completo incrustado** en un bloque (segundo `<!DOCTYPE>`, `<html>`, `<head>` y `<title>` dentro del `<body>`). `/bienestar-digital/` tiene 3.
4. **Enlazado interno casi inexistente:** solo 1 de los 15 artículos enlaza a otro artículo. Ninguno enlaza a `/servicios/` ni a un pilar, y los pilares no enlazan a sus artículos. Hay más de 105 anclas "Continuar"/"Leer más". Las citas a estudios se nombran pero no se enlazan (14 de 15 artículos no tienen ningún enlace externo en el cuerpo).
5. **Rendimiento probable por debajo del objetivo (estimación):** 9–15 CSS y 10–14 JS por página, Google Fonts externas (3 a 5 familias), `fetchpriority="high"` puesto en el **logo PNG de 115 KB** en lugar de en la imagen LCP, héroe de la home en PNG de 382 KB **con `loading="lazy"`** y 0 imágenes webp/avif.

**Recomendación:** instalar **Rank Math (versión gratuita, con módulos mínimos)**. Así se resuelven de una vez las descripciones, OG, canonical, noindex de archivos finos, sitemap, JSON-LD y redirecciones 301. Después toca la limpieza editorial (H1, enlaces internos, fuentes) y, en paralelo, el rendimiento (imágenes webp, fuentes locales, LCP).

## 2. Qué está bien (no tocar)

| Señal | Evidencia |
|---|---|
| http→https y www→sin www con 301 | `curl -I http://codigocalma.com/` → 301 `https://codigocalma.com/`; `https://www…` → 301 |
| Caché y compresión | `x-litespeed-cache: hit`, `x-hcdn-cache-status: HIT`, `content-encoding: br` |
| Canonical en páginas y entradas | presente en 26 de 28 HTML (core de WP) |
| Búsqueda interna con noindex | `/?s=calma` → `noindex, follow` |
| 404 reales | `/pagina-inexistente-xyz/` → 404 |
| robots.txt | 200, no bloquea CSS/JS, declara `Sitemap: https://codigocalma.com/wp-sitemap.xml`; `/sitemap.xml` → 301 al sitemap core |
| Idioma, fecha y autor visibles | `<html lang="es">`; fecha publicada/actualizada visible en los artículos |
| `width`/`height` en imágenes | presentes en todas salvo 4 en `/testimonios/` |

## 3. Tabla de hallazgos

Impacto: A = alto, M = medio, B = bajo. Esfuerzo: S (< 1 h), M (medio día), L (> 1 día).

| ID | URL / alcance | Problema | Evidencia | Imp. | Esf. | Solución |
|---|---|---|---|---|---|---|
| SEO-01 | 28 URLs | Sin meta description | ningún `<meta name="description">` en el snapshot | A | M | Plugin SEO + textos de la sección 4 |
| SEO-02 | 28 URLs | Sin Open Graph ni Twitter Card: al compartir en LinkedIn/WhatsApp sale sin imagen ni resumen | 0 coincidencias de `og:` / `twitter:` | M | S | Plugin SEO; imagen OG por defecto de 1200×630 (logo + claim) e imagen destacada en los artículos |
| SEO-03 | 28 URLs | Sin JSON-LD. Solo hay microdatos de Kadence (`itemtype=WebPage`, `itemprop` en artículos) | 0 `application/ld+json`; `home.html:2` | M | M | `@graph` Organization + WebSite + Person + BlogPosting + BreadcrumbList (skill `schema-markup`), sin campos sin verificar |
| SEO-04 | `/blog/`, `/category/*`, `/tag/*`, `/author/*`, `/2026/05/`, `/blog/page/2/` | Sin canonical | `blog.html` y `category_ciberseguridad.html` sin `rel="canonical"`; archivos comprobados con curl | M | S | El plugin SEO añade canonical autorreferente a archivos y paginación |
| SEO-05 | `/blog/` vs `/entradas/` | Duplicado: los dos listan las mismas entradas. `/blog/` es la página de entradas nativa (pagina en `/blog/page/2/`, está en el sitemap, sin H1 ni canonical). `/entradas/` es una página con bloque de posts y nube de etiquetas, y es la que enlaza el menú "Blog" | `wp-sitemap-posts-page-1.xml` incluye las dos; enlace del menú `href=".../entradas/"` en todas las páginas | A | S | Mantener **`/blog/`** (URL descriptiva y con paginación nativa), llevar a Kadence el diseño que hoy tiene `/entradas/` (título visible como H1 e intro), 301 `/entradas/` → `/blog/` y cambiar el menú |
| SEO-06 | `/sobre_tatiana/` | Slug con guion bajo; `/sobre-tatiana/` da 404 | API `pages.json` id 946; `curl /sobre-tatiana/` → 404 | M | S | Cambiar el slug a `sobre-tatiana` + 301. A futuro, `/equipo/tatiana-x-stacul/` (IDs de la skill schema) |
| SEO-07 | `/descargas-2/` | El slug `-2` existe porque el **adjunto 1839** (`descargas.jpg`) ocupa `descargas`. La home enlaza `/descargas/` (`home.html`, `href="/descargas/"`), que redirige a `/descargas-2/` | `wp-json/wp/v2/media?slug=descargas` → id 1839; `curl -I /descargas/` → 301 `x-redirect-by: WordPress` | M | S | Renombrar el slug del adjunto 1839 (p. ej. `descargas-portada`), cambiar el de la página a `descargas`, 301 `/descargas-2/` → `/descargas/` |
| SEO-08 | 15 artículos, `/blog/`, archivos | **Enlace de autor roto (404)** en todo el blog | `class="author vcard"><a href="https://codigocalma.com/codigocalma">`; `wp/v2/users` → `"url":"https://codigocalma.com/codigocalma"`; `curl` → 404 | A | S | Usuarios → Perfil → "Sitio web": dejarlo vacío o poner `https://codigocalma.com/sobre-tatiana/`; completar la biografía |
| SEO-09 | `/author/admin/`, `/wp-json/wp/v2/users`, `/?author=1` | El usuario `admin` queda expuesto e indexable: el archivo de autor está en el sitemap y duplica `/blog/` | `wp-sitemap-users-1.xml` → `/author/admin/`; `?author=1` → 301 `/author/admin/` | M | S | Cambiar el nicename a `tatiana-x-stacul` (o crear usuaria editora y reasignar), noindex o 301 del archivo de autor a `/sobre-tatiana/`, sacar usuarios del sitemap; limitar `/wp/v2/users` sin autenticación (coordinar con seguridad) |
| SEO-10 | servicios, contacto, blog, descargas-2, entradas, testimonios / home / bienestar-digital | Sin H1 (6 páginas); 2 H1 en la home; 3 H1 en bienestar-digital | extracción: `h1=[]`; `home.html:652` y `:699`; `bienestar-digital.html:251, 275, 317` | A | S | Un único H1 por URL con la palabra clave. Propuestas: servicios "Mentorías y acompañamiento uno a uno"; contacto "Cuéntanos cómo podemos ayudarte"; blog "Blog de ciberpsicología y bienestar digital"; descargas "Guías gratuitas para descargar"; testimonios "Testimonios"; home: H1 = "Comprendiendo el comportamiento humano en entornos digitales" (hoy en H4/H2); bienestar: dejar "Bienestar digital" y pasar el resto a H2 |
| SEO-11 | `/` | Documento HTML completo incrustado en un bloque de HTML personalizado: 2.º `<!DOCTYPE>`, `<html>`, `<head>` y `<title>Línea de tiempo tecnología – últimos 50 años</title>` dentro del `<body>`. Genera el H1 extra | `home.html:531-535`, `:652` | M | S | Dejar en el bloque solo el fragmento (sección + estilos con alcance + script); la cabecera de la línea de tiempo pasa a H2 |
| SEO-12 | 15 artículos + páginas | `<title>` sin optimizar: 13/15 artículos > 60 car. (el de autoevaluación tiene 113); páginas genéricas ("Servicios – Código Calma", 24); Title Case inconsistente; "autoria" sin tilde en título, H1 y `alt` | extracción de `<title>`; `ia-y-apoyo…html` | M | S | Títulos SEO de la sección 4; corregir "autoría" en el H1 (no hace falta cambiar el slug) |
| SEO-13 | 7 artículos, home | Saltos de jerarquía H1→H3 (sin H2) en fuerza-de-voluntad, querer-y-ser-capaz, ia-y-apoyo (llega a H5), estigma, infancias, autoevaluación, el-arte; el héroe de la home "PORTAL DE CIBERPSICOLOGÍA" es un H4 | secuencias `13333`, `1335533`; `home.html:292` | B | S | Pasar a H2 las secciones de primer nivel; el rótulo del héroe como `<p>` con estilo |
| SEO-14 | todo el sitio | Enlazado interno pobre: 1/15 artículos enlaza a otro artículo; 0 a `/servicios/` o a pilares; los pilares `/ciberpsicologia/` y `/bienestar-digital/` no enlazan a ningún artículo; más de 105 anclas "Continuar"/"Leer más"; las 5 tarjetas de `/ciberpsicologia/` llevan `aria-label="Herramientas útiles"` | análisis del `entry-content`; `ciberpsicologia.html` (`kt-blocks-info-box-link-wrap`) | A | M | Por artículo: ≥ 1 pilar + 2 relacionados + 1 servicio con anclas descriptivas; cada pilar enlaza a todos sus artículos; corregir los `aria-label`; "Leer más: <título>" (con content-strategist) |
| SEO-15 | 14/15 artículos | Estudios citados sin enlace (p. ej. "Frontiers in Behavioral Economics", Wendy Wood, estudio de IA y apoyo emocional); sin sección de fuentes enlazada. En YMYL resta confianza | 0 enlaces externos en el cuerpo salvo `infancias-figitales` (1) | M | M | Añadir "Fuentes" con DOI/PMC/organismos oficiales. Lo busca y valida el equipo de contenidos; sin inventar referencias |
| SEO-16 | `/tag/*`, `/2026/05/`, `/category/sin-categoria/` | Archivos finos indexables: 11 etiquetas en el sitemap (7 con 1 sola entrada), 4 etiquetas vacías, slugs con guion bajo (`salud_mental`, `inteligencia_artificial`, `redes_sociales`, `mindfulness_digital`, `transformacion_digital`, `liderazgo_consciente`, `terapia_online`), archivos de fecha indexables, "Sin categoría" vacía con 200 | `wp-sitemap-taxonomies-post_tag-1.xml`; `tags.json`; curl → `max-image-preview:large` sin noindex | M | S | `noindex, follow` en etiquetas, fechas y autor; sacarlos del sitemap; borrar las etiquetas vacías; slugs con guion + 301; renombrar "Sin categoría" |
| SEO-17 | sitemap | El sitemap del core no lleva `lastmod`, incluye usuarios y etiquetas y va a incluir las URLs que se consoliden | `wp-sitemap-*.xml` | B | S | Sitemap del plugin SEO: solo URLs indexables, con `lastmod`; enviarlo en Search Console |
| SEO-18 | todas (estimación, sin PSI) | **Riesgo de LCP > 2,5 s en mobile.** HTML de 81–249 KB (testimonios 249, home 208); 9–15 hojas CSS y 10–14 scripts por página (jQuery + migrate, AddToAny externo `static.addtoany.com`, ZoloBlocks + Kadence Blocks + Blocks Animation en todas); Google Fonts externas Lora (4 pesos) + Inter (3–4) + Jost, más Playfair Display + Inter en `/herramientas/` y Sora en `/servicios/`; `fetchpriority="high"` en el logo `cropped-logo512-1.png` (512×512, 115 KB) en las 28 páginas; héroe de la home `Gemini_Generated_Image_24frf…png` 864×1219, **382 KB, con `loading="lazy"`** (`home.html:321`); héroe de contacto en PNG de 804×1024 | extracción + `curl -I` de pesos | A | M | Logo en SVG/webp ≤ 10 KB sin `fetchpriority`; imagen LCP de cada plantilla en webp con `fetchpriority="high"` y sin lazy; fuentes locales en woff2 (≤ 2 familias) con preload; cargar ZoloBlocks/Animation/CF7/AddToAny solo donde se usan; LiteSpeed: UCSS/CCSS y JS diferido. **Medir con PSI antes y después** |
| SEO-19 | imágenes | 0 webp/avif; `alt` de stock en inglés ("Woman performing an athletic pose…", "Young man coding…", "Colorful choice…", "Close-up of a woman…", "Pink brain-shaped candle…"); `alt=""` en imágenes con contenido (foto de Tatiana `sobre_tatiana.html:273`, héroe de la home y de contacto, destacada de `descubriendo…` de 1408×768); nombres de archivo `Gemini_Generated_Image_x4xg…` | extracción `ext={'jpg','png'}` en las 28 | M | M | Conversión a webp (LiteSpeed Image Optimization o QUIC.cloud); `alt` descriptivo en español; nombres de archivo descriptivos en las imágenes nuevas |
| SEO-20 | `/testimonios/` | 3 imágenes dan 404 (`testimonio-6.jpg`, `-9.jpg`, `-10.jpg`) y 4 no tienen `width`/`height` (riesgo de CLS); los testimonios hablan de "terapia centrada en el paciente" mientras el servicio se presenta como mentoría | `curl` → 404; `testimonios.html` | M | S | Volver a subir o quitar las imágenes; declarar dimensiones. Revisar la coherencia del texto con cro-copy/legal (no se modifica ningún testimonio) |
| SEO-21 | `/test/`, `/ciberpsicologia/`, `/contacto/` | Voseo en lugar del tuteo de marca ("Descubrí", "Elegís", "¿De qué generación sos?", "Contactanos"); etiquetas del formulario CF7 en inglés ("Name", "Message") | `txt/test.txt`, `txt/ciberpsicologia.txt`, `txt/contacto.txt` | B | S | Unificar en tuteo; traducir las etiquetas |
| SEO-22 | `/` | Cifra mal expresada: "6M+ · Más de 6 mil millones de personas" (6M = 6 millones) | `txt/home.txt` | B | S | "6.000 M+" o "6 mil millones+", con la fuente enlazada (UIT) |
| SEO-23 | host | Cadena de redirección `http://www` → `https://www` → `https://` (2 saltos); sin cabecera HSTS | `curl -I http://www.codigocalma.com/` | B | S | Regla única a `https://codigocalma.com/` en el hPanel/.htaccess; activar HSTS cuando todo sea estable |
| SEO-24 | taxonomía | Categorías que no corresponden: "¿Por qué fallamos al intentar cambiar conductas?" está en *Ciberseguridad*; "5 puntos… Meta" y "El estigma de la estructura" en *Neurociencia y tecnología* | `posts.json` → `categories` | B | S | Revisar con content-strategist al definir los pilares |
| SEO-25 | robots.txt / IA | robots.txt mínimo y correcto; `/llms.txt` → 404; sin política para bots de IA | `robots.txt`, curl | B | S | Coordinar con `geo-specialist` (no se toca aquí) |

## 4. Propuesta de title + meta description

Formato: `Palabra clave: beneficio | Código Calma`. Longitudes medidas con script (en caracteres). Tuteo, sin promesas de resultados. El equipo de contenidos debe validar que cada descripción refleje el artículo antes de publicarla.

### 4.1 Páginas (12)

| URL (final) | Title (car.) | Meta description (car.) |
|---|---|---|
| `/` | Ciberpsicología y bienestar digital en calma \| Código Calma (59) | Artículos, herramientas y acompañamiento uno a uno para entender cómo la tecnología influye en tu conducta y construir una relación más consciente con ella. (156) |
| `/servicios/` | Mentoría en ciberpsicología uno a uno \| Código Calma (52) | Acompañamiento online, una persona por vez, de tres a seis sesiones: hábitos digitales, accesibilidad cognitiva y gestión de proyectos. Cuéntanos qué necesitas. (160) |
| `/contacto/` | Contacto: escríbenos y cuéntanos qué te pasa \| Código Calma (59) | Escríbenos con unas líneas sobre lo que te ocurre y te respondemos quién del equipo encaja contigo y qué puedes esperar del primer encuentro. Sin compromiso. (157) |
| `/sobre-tatiana/` | Tatiana X. Stacul, psicóloga y ciberpsicóloga \| Código Calma (60) | Conoce a Tatiana X. Stacul, psicóloga detrás de Código Calma, y su enfoque: ciencias del comportamiento aplicadas a tu relación diaria con la tecnología. (153) |
| `/ciberpsicologia/` | Qué es la ciberpsicología y cómo te influye \| Código Calma (58) | Descubre qué estudia la ciberpsicología: por qué algunas plataformas crean hábitos difíciles de romper y cómo los entornos digitales afectan tus emociones. (155) |
| `/bienestar-digital/` | Bienestar digital: primeros pasos con calma \| Código Calma (58) | Aprende qué es el bienestar digital y cómo empezar a usar tus dispositivos con intención, cuidar tu privacidad y decidir qué lugar ocupa la tecnología. (151) |
| `/herramientas/` | Apps para bienestar digital y productividad \| Código Calma (58) | Explora apps de meditación, sueño y enfoque seleccionadas como punto de partida para tu bienestar digital. Son un apoyo y no reemplazan la atención profesional. (160) |
| `/test/` | Test de consumo digital gratuito y educativo \| Código Calma (59) | Responde 12 preguntas en unos cinco minutos y reflexiona sobre tu relación con la tecnología. Es un test educativo: no reemplaza una evaluación profesional. (156) |
| `/descargas/` | Guías gratuitas de ciberpsicología en PDF \| Código Calma (56) | Descarga guías gratuitas de Tatiana X. Stacul sobre salud mental digital, ciberseguridad para psicólogos y psicología para devs, y léelas a tu ritmo. (149) |
| `/testimonios/` | Testimonios de personas que acompañamos \| Código Calma (54) | Lee las experiencias de personas que hicieron un acompañamiento con Código Calma y conoce cómo trabajamos antes de escribirnos para tu primer encuentro. (152) |
| `/blog/` | Blog de ciberpsicología y bienestar digital \| Código Calma (58) | Lee artículos sobre ciberpsicología, bienestar digital, neurociencia y ciberseguridad explicados con claridad, para entender mejor tu vida entre pantallas. (155) |
| `/entradas/` | — (se consolida con 301 a `/blog/`; si se mantuviera, `noindex, follow`) | — |

### 4.2 Artículos (15)

| Slug | Title (car.) | Meta description (car.) |
|---|---|---|
| por-que-tu-fuerza-de-voluntad-es-mas-lista-de-lo-que-crees | Fuerza de voluntad: más lista de lo que crees \| Código Calma (60) | ¿Tu fuerza de voluntad es un depósito que se vacía? Descubre qué dice hoy la ciencia sobre el «agotamiento del ego» y cómo influye en tus decisiones diarias. (157) |
| la-diferencia-entre-querer-y-ser-capaz-entendiendo-la-autoeficacia | Autoeficacia: diferencia entre querer y poder \| Código Calma (60) | Entiende qué es la autoeficacia y por qué tener ganas no siempre basta para actuar. Una mirada desde la psicología a esa parálisis que a veces sentimos. (152) |
| por-que-fallamos-al-intentar-cambiar-conductas | Por qué fallamos al cambiar una conducta \| Código Calma (55) | Descubre por qué saber qué hacer no basta para cambiar un hábito y qué aporta el «paternalismo afectivo» al entender cómo se siente cada decisión en tu equipo. (159) |
| ia-y-apoyo-emocional-saber-la-autoria-cambia-tu-perspectiva | IA y apoyo emocional: importa la autoría \| Código Calma (55) | Un estudio muestra que saber si un mensaje de apoyo lo escribió una IA o una persona cambia cómo lo valoramos. Descubre qué implica para tu bienestar digital. (158) |
| el-estigma-de-la-estructura-x-entonces-y | «X entonces Y»: la claridad no es cosa de IA \| Código Calma (59) | ¿Un texto claro y lógico es señal de IA? Descubre de dónde viene la estructura «X, entonces Y» y por qué la claridad es una herencia humana, no artificial. (155) |
| infancias-figitales | Infancias figitales: criar sin offline \| Código Calma (53) | Reflexiona sobre la crianza en un mundo donde lo físico y lo digital ya no se separan, y descubre claves para acompañar a niñas y niños en su vida figital. (155) |
| calidad-vs-cantidad-la-hipotesis-de-ricitos-de-oro | Tiempo de pantalla y Ricitos de Oro \| Código Calma (50) | ¿Importa más cuánto tiempo pasas frente a pantallas o cómo lo usas? Descubre la hipótesis de Ricitos de Oro y por qué la calidad del uso digital pesa tanto. (156) |
| autoevaluacion-del-consumo-digital-… | Autoevaluación de tu consumo digital \| Código Calma (51) | Aprende a evaluar tu consumo digital con preguntas sencillas sobre tiempo, hábitos y emociones, y da un primer paso hacia un uso más consciente. (144) |
| preguntas-clave-para-entender-y-cuidar-nuestro-cerebro | Salud cerebral: preguntas clave para cuidarte \| Código Calma (60) | Descubre qué es la salud cerebral y qué hábitos cotidianos la favorecen, en un recorrido por las preguntas clave para entender y cuidar mejor tu cerebro. (153) |
| 5-puntos-clave-que-el-caso-de-meta-nos-deja-en-salud-mental | Caso Meta y salud mental: 5 puntos clave \| Código Calma (55) | Repasa cinco aprendizajes que deja el caso de Meta sobre redes sociales y salud mental, y qué preguntas conviene hacerte sobre tu propio uso de plataformas. (156) |
| reflexiones-eticas-sobre-el-desarrollo-de-la-inteligencia-artificial | Ética de la inteligencia artificial \| Código Calma (50) | Explora los principales dilemas éticos del desarrollo de la inteligencia artificial, desde los sesgos hasta la privacidad, y cómo afectan a tu vida digital. (156) |
| descubriendo-que-modela-nuestro-comportamiento | Qué modela tu comportamiento según la ciencia \| Código Calma (60) | Descubre qué es la ciencia del comportamiento y qué factores moldean tus decisiones diarias, dentro y fuera de las pantallas, explicado de forma clara. (151) |
| la-tecnologia-te-supera-como-identificar-y-gestionar-el-tecnoestres | Tecnoestrés: cómo identificarlo y gestionarlo \| Código Calma (60) | Aprende a reconocer las señales del tecnoestrés, entiende por qué aparece y conoce estrategias prácticas para gestionar tu relación diaria con la tecnología. (157) |
| el-arte-de-redisenar-tu-entorno | Rediseñar tu entorno para liberar tu mente \| Código Calma (57) | Descubre qué muestran los estudios de Wendy Wood sobre hábitos y entorno, y cómo pequeños cambios en tu espacio te ayudan sin depender solo de la voluntad. (155) |
| como-un-te-quiero-infecto-45-millones-de-computadoras-en-todo-el-mundo | ILOVEYOU: el virus que hackeó el afecto \| Código Calma (54) | Conoce la historia del virus ILOVEYOU, que en el año 2000 se propagó por millones de equipos, y qué enseña sobre el phishing y tu seguridad digital. (148) |

Notas: el H1 visible de cada artículo **no cambia** (salvo "autoría"); el title SEO se configura aparte en el plugin. No se proponen cambios de slug en los artículos: ya están indexados y el beneficio de acortarlos no compensa.

## 5. Redirecciones 301 propuestas

Todas de un solo salto, a la URL final con barra. Se cargan en el gestor de redirecciones del plugin SEO (o en `.htaccess`) **después** de cambiar los slugs, y luego se actualizan los enlaces internos para que apunten directamente a la URL final.

| Origen | Destino | Motivo |
|---|---|---|
| `/sobre_tatiana/` | `/sobre-tatiana/` | SEO-06 |
| `/entradas/` | `/blog/` | SEO-05 (cambiar también el menú) |
| `/descargas-2/` | `/descargas/` | SEO-07 (antes, liberar el slug del adjunto 1839; comprobar que no haya bucle con la redirección automática de WP) |
| `/codigocalma` | `/sobre-tatiana/` | SEO-08 (URL rota que puede estar ya rastreada) |
| `/author/admin/` | `/sobre-tatiana/` (o `/author/tatiana-x-stacul/` si se mantienen archivos de autor) | SEO-09 |
| `/tag/salud_mental/`, `/tag/inteligencia_artificial/`, `/tag/redes_sociales/`, `/tag/mindfulness_digital/`, `/tag/transformacion_digital/` | la misma ruta con guion (`/tag/salud-mental/`…) | SEO-16 (las etiquetas vacías `liderazgo_consciente`, `terapia_online`, `neuroplasticidad`, `awareness-humano` se borran, sin redirección) |
| `/category/sin-categoria/` | `/blog/` | SEO-16 (o renombrar la categoría por defecto) |
| `http://www.codigocalma.com/*` | `https://codigocalma.com/*` | SEO-23 (hoy son 2 saltos) |

Futuro (si se crea la sección de equipo): `/sobre-tatiana/` → `/equipo/tatiana-x-stacul/`, pero no antes de que esa URL exista.

## 6. Plugin SEO: comparación y recomendación

| Opción | A favor | En contra |
|---|---|---|
| **Rank Math (gratis)** | Todo en uno: title/description por URL, OG/Twitter, canonical en archivos, noindex por tipo, sitemap con `lastmod`, **gestor de redirecciones 301 y monitor de 404 incluidos**, schema editable (Article/Person/Organization/FAQ), migas compatibles con Kadence; el sitio queda con un solo plugin | Pesado si se activan todos los módulos; avisos de la versión Pro; hay que desactivar el análisis de contenido, el módulo de analytics y los que no se usen; volcado de schema algo rígido para `Person` con `@id` propios |
| Yoast SEO (gratis) | Muy estable y documentado; grafo schema limpio (WebSite/Organization/Person/Article enlazados por `@id`) | Las redirecciones son de pago (hay que sumar el plugin Redirection); interfaz y peso similares o mayores; más publicidad dentro del panel |
| The SEO Framework | Muy ligero y rápido, sin anuncios, buenos valores por defecto (canonical y noindex de archivos) | Sin redirecciones (hace falta Redirection), schema básico (sin Person/BlogPosting a medida sin extensiones de pago), OG limitado |
| Código en tema hijo | Control total, cero peso extra, schema exacto de la skill `schema-markup` | Requiere crear y mantener un tema hijo de Kadence; las editoras no pueden cambiar títulos ni descripciones desde el editor sin campos a medida; sitemap y redirecciones hay que resolverlos aparte; más riesgo de errores |

**Recomendación: Rank Math gratis** con estos módulos: SEO de entradas y páginas, sitemap, schema, redirecciones, monitor de 404, OG/redes. Desactivar: análisis de contenido, SEO local, analytics, rol manager, imagen SEO. Configuración mínima:
- noindex en etiquetas, fechas, autor y "Sin categoría";
- quitar los usuarios del sitemap;
- título por defecto `%title% | Código Calma`;
- imagen OG por defecto de 1200×630.

Si hiciera falta un `Person` con credenciales verificadas, se completaría con un filtro pequeño (`rank_math/json_ld`) en un tema hijo o un plugin propio. Alternativa si el rendimiento manda: **The SEO Framework + Redirection** (dos plugins ligeros), aceptando un schema más pobre.

## 7. Orden sugerido

1. **S, inmediato:** SEO-08 (enlace de autor), SEO-10/11 (H1), SEO-20 (imágenes rotas), SEO-22.
2. **Plugin SEO:** SEO-01, 02, 03, 04, 12, 16, 17 + redirecciones de la sección 5 (SEO-05, 06, 07, 09, 23).
3. **Editorial (con content-strategist):** SEO-14, 15, 13, 21, 24.
4. **Rendimiento:** SEO-18, 19. Medir PSI mobile en inicio, servicios, contacto, un artículo largo y blog, antes y después.
5. **Validación:** Rich Results Test + validator.schema.org; Search Console (enviar sitemap, inspeccionar las URLs redirigidas).
