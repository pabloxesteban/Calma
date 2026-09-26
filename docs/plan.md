# Plan priorizado — Rediseño de codigocalma.com

Fecha: 26-09-2026 · Estado: **pendiente de aprobación** (no se implementó nada)
Base: `docs/auditoria/inventario.md` y los 6 informes de `docs/auditoria/informes/` (UX-01…28, SEO-01…25, GEO-01…15, CRO-01…20, A11Y-01…21 y hallazgos cognitivos).
Esfuerzo: **S** < 2 h · **M** ½–1 día · **L** 2–4 días.

---

## 1. Resumen ejecutivo

1. **El problema de acceso de las IA es real, pero no está en robots.txt**, que es permisivo. Viene de la protección antibots de Hostinger/LiteSpeed:
   - GPTBot recibe `429` en 36 de 36 intentos sobre `/blog/` y en URLs con parámetros (también en las `?utm_source=chatgpt.com`).
   - Cualquier visitante recibe `403` o una pantalla reCAPTCHA «Bot Verification» en cerca del 12 % de las páginas que no salen de caché.
   - Solo se resuelve en hPanel (GEO-01/02).
2. **La mayoría de los bugs visuales tienen tres causas concretas**, y no hace falta rehacer cada página:
   - Un documento HTML completo pegado en el inicio (su `body{padding:40px}` encoge y recorta todo).
   - CSS inline en Servicios que anula el padding de las tarjetas.
   - Las animaciones de Blocks Animation, que dejan texto fuera de pantalla o invisible (UX-01/03/04/08).
3. **SEO y GEO parten de cero:**
   - 0/28 URLs tienen meta description, Open Graph o JSON-LD.
   - La firma de la autora enlaza a una página 404 en todo el blog y el usuario de WordPress es `admin`.
   - 14 de 15 artículos no enlazan ninguna fuente, y en el cuerpo de los artículos hay un único enlace entre artículos.
4. **El camino a la consulta es largo:**
   - Sin CTA en la primera pantalla de Inicio ni de Servicios.
   - Ningún CTA en artículos.
   - Formulario con etiquetas en inglés y sin aviso de privacidad.
   - Sin aviso de urgencias ni newsletter (CRO-01…08).
5. **Accesibilidad:** 1 fallo bloqueante (el Test de consumo digital no se puede hacer con teclado) y 6 altos. El más extendido es el azul `#64b2e5` del botón global, con contraste 2,32:1 en todo el sitio.

---

## 2. Decisión previa: cómo implementamos (el repo no tiene el sitio)

El repositorio estaba vacío: el sitio es un WordPress administrado en Hostinger y no tengo acceso a wp-admin ni a hPanel. Propongo que la rama contenga **todo lo necesario para aplicar los cambios**, probado en un WordPress local, y que la publicación la haga una persona con acceso.

| Pieza en la rama | Qué contiene | Cómo se aplica |
|---|---|---|
| `wp-content/themes/kadence-child/` | Tema hijo: tokens `--calma-*` mapeados a la paleta de Kadence, componentes, correcciones mobile, CSS de impresión, `prefers-reduced-motion` | Subir por FTP o como .zip y activar |
| `wp-content/mu-plugins/codigo-calma-seo-geo.php` | Filtro de robots.txt, `/llms.txt` dinámico, JSON-LD (`@graph`), caja de autora, bloque «En resumen» | Subir a `mu-plugins` (se activa solo) |
| `contenido/` | Versión corregida de cada página y artículo en HTML de bloques (Gutenberg), lista para pegar en el editor de código, más un diff contra el original | Pegar en el editor, página por página |
| `docs/implementacion/ajustes-wp-admin.md` | Ajustes del Customizer de Kadence, redirecciones 301, usuarios, medios, hPanel (firewall), con capturas de dónde tocar | Checklist manual |
| `staging/` | WordPress local (PHP 8.4 + SQLite + Kadence) cargado con el contenido público vía API REST | Para las capturas antes/después y la QA de cada etapa |

**Alternativa:** si me das una copia del sitio (exportación WXR + lista de plugins, o un backup de Hostinger), el staging queda idéntico a producción y las capturas de QA son más fieles. **Recomiendo pedirla**, pero no bloquea el arranque.

**Plugin SEO:** Rank Math (gratis, módulos mínimos: títulos/metas, sitemap, redirecciones, monitor de 404) para lo que se edita a mano. El JSON-LD y `llms.txt` van en el mu-plugin, así no dependen del plugin. Alternativa ligera: The SEO Framework + Redirection.

---

## 3. Matriz impacto / esfuerzo

| | **Esfuerzo bajo (S)** | **Esfuerzo medio/alto (M–L)** |
|---|---|---|
| **Impacto alto** | **Quick wins → Etapa 1**: firewall de Hostinger, robots.txt, errores de texto, enlace de autora 404, quitar el HTML pegado del inicio, CSS inline de Servicios, animaciones, contraste del botón global, H1 únicos, formulario en español | **Estratégicos → Etapas 2–5**: design system en tema hijo, página de servicios y flujo de consulta, schema + metas de 27 URLs, páginas de equipo, taxonomía y clusters, «En resumen» + fuentes en 15 artículos, pilar "¿Qué es la ciberpsicología?" |
| **Impacto medio/bajo** | Relleno: imágenes rotas en testimonios, `/descargas/`, cadena de redirección www, etiquetas vacías, `alt` en inglés | Después: newsletter con lead magnet, rehacer el test accesible, rendimiento fino (fuentes locales, recorte de plugins), 12 artículos nuevos |

---

## 4. Plan por etapas

### Etapa 1 — Arreglos críticos (≈ 2 días de trabajo + tareas del cliente)
Objetivo: que nada esté roto, bloqueado o mal escrito.

| # | Tarea | Hallazgos | Impacto | Esfuerzo | Quién |
|---|---|---|---|---|---|
| 1.1 | **Firewall/antibots de Hostinger:** permitir los bots verificados (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, PerplexityBot, Google, Bing); revisar la regla que devuelve 429 a GPTBot, el reCAPTCHA de LiteSpeed (`.lsrecap`) y el límite de peticiones. Texto de ticket listo en `informes/geo.md` §2.5 | GEO-01/02, A11Y-17 | Muy alto | S (cliente en hPanel) | Cliente + geo |
| 1.2 | robots.txt con grupos explícitos por bot de IA + Sitemap (borrador listo) | GEO-04, SEO-25 | Alto | S | geo |
| 1.3 | Corregir los 64 errores de texto: 6M+, autoría, «el día a day», voseo → tuteo en test/herramientas/ciberpsicología, «Bibliografia», «quizas», puntuación, restos de un comentario HTML visibles en Herramientas, «Bienvenidos» → «Bienvenida/o» o neutro | CRO §4, GEO-12/15, SEO-21/22 | Alto | M | cro-copywriter |
| 1.4 | Campo "Sitio web" del usuario → borrar (arregla el 404 de la firma en todo el blog) | SEO-08, GEO-05 | Alto | S (wp-admin) | seo |
| 1.5 | Inicio: quitar el documento HTML pegado y rehacer la línea de tiempo como bloque nativo (o moverla a /ciberpsicologia/); quitar fila y `<p>` vacíos | UX-01/02/05, SEO-11, A11Y-07 | Muy alto | M | ux-ui |
| 1.6 | Servicios y Herramientas: eliminar los `<style>` inline (reset `.cc li/p`, CSS muerto, fuente Sora) | UX-08/09/10/12/21/28 | Alto | S | ux-ui |
| 1.7 | Desactivar Blocks Animation (o forzar `prefers-reduced-motion` y quitar `visibility:hidden`) para que nada quede fuera de pantalla | UX-03/04, A11Y-15 | Alto | S | ux-ui |
| 1.8 | Botón global de Kadence y textos pequeños en `#64b2e5` → `#1d5f94` (6,7:1) | UX-13/14, A11Y-02…05 | Alto | S | ux-ui + a11y |
| 1.9 | Un H1 por página (6 páginas sin H1, inicio con 2, bienestar-digital con 3); nada de saltos H1→H3 | SEO-10/13, A11Y-06/07 | Alto | S | seo |
| 1.10 | Mobile: layout "unboxed" en las 9 páginas encajonadas (sin franjas vacías), margen lateral de 20 px, escala tipográfica mobile (H1 42 → ~30 px) | UX-11/16/24 | Alto | M | ux-ui |
| 1.11 | Formulario: etiquetas en español y visibles, nombre obligatorio, `autocomplete`, casilla de privacidad, mensaje de "qué pasa ahora" | CRO-01/02/03, A11Y-09/10, UX-20 | Alto | S | cro + a11y |
| 1.12 | Varios: 3 imágenes 404 en testimonios, `alt` de la foto de Tatiana, botón de LinkedIn sin nombre, enlace `/descargas/`, redirección www en 1 salto | SEO-20/23, A11Y-08/16, CRO-15 | Medio | S | seo + a11y |
| 1.13 | Testimonios de "Luis R." y "Ana M." en Sobre Tatiana: ocultar hasta confirmar la fuente | CRO-10 | Medio (confianza) | S | cro |

QA: capturas antes/después a 360/390/430/1280, `mobile-qa` y `accessibility-qa`. Criterio: 0 contenido recortado, 0 violaciones de contraste en axe, un H1 por página, 0 errores de texto de la lista.

### Etapa 2 — Design system unificado (≈ 3–4 días)
| # | Tarea | Hallazgos | Impacto | Esfuerzo |
|---|---|---|---|---|
| 2.1 | Tema hijo de Kadence con tokens `--calma-*` → `--global-palette*`: color, tipografía, espaciado, radios | UX-07/13/15 | Alto | M |
| 2.2 | Tipografía: de 6 familias a 2 (Lora para títulos, Inter para el cuerpo), alojadas localmente en woff2 con preload | UX-15, SEO-18 | Alto (también LCP) | S |
| 2.3 | Header único: logo más chico, CTA "Solicitar una consulta" visible; drawer mobile claro con logo, CTA y el menú plano (sin esconder Blog/Test/Descargas) | UX-06/25/26 | Alto | M |
| 2.4 | Footer en 4 columnas: marca, navegación, recursos, contacto + newsletter; fila legal con privacidad y aviso de urgencias | UX-17, CRO-08 | Alto | M |
| 2.5 | Componentes: botón, tarjeta, tarjeta de paso (número dentro), badge por categoría, CTA navy, formulario; migrar el marcado de Servicios/Herramientas a `calma-*` | UX-08/22/23 | Alto | M |
| 2.6 | Blog y tarjetas: listado en grilla compacta, "Leer más" con nombre accesible del artículo | UX-23, A11Y-18, SEO-14 | Medio | S |
| 2.7 | Modo oscuro: **propongo no ofrecerlo en esta etapa** (duplica la QA de contraste); los tokens quedan preparados | — | Bajo | — |

QA: las mismas pruebas en todas las plantillas (página, entrada, archivo, búsqueda, 404).

### Etapa 3 — Servicios y flujo de consulta (≈ 3 días)
| # | Tarea | Hallazgos | Impacto | Esfuerzo |
|---|---|---|---|---|
| 3.1 | Servicios con estructura de conversión: hero con CTA arriba, "¿Es para ti?" / "cuándo no", proceso, equipo con foto y un CTA por profesional (`?area=`), confianza (formación declarada, testimonios reales con enlace a Google), FAQ, CTA final, aviso de urgencias | CRO-05/09/11/13, UX-18 | Muy alto | M |
| 3.2 | Inicio: hero que diga qué y para quién + CTA; recorte de la página de 14.000 px a secciones útiles | CRO-04/14 | Alto | M |
| 3.3 | Páginas de equipo `/equipo/<slug>/` (Tatiana; Francisca y Emanuel con placeholders); `/sobre_tatiana/` → 301 | CRO-09, GEO-11, SEO-06 | Alto (E-E-A-T) | M |
| 3.4 | Caja CTA al final de cada artículo, según el tema y la profesional | CRO-06 | Alto | S |
| 3.5 | Formulario: área como opción (radio), mensaje corto, anti-spam invisible, evento `generate_lead` | CRO-17/18 | Medio | S |
| 3.6 | Resultado del test con CTA claro (consulta + suscripción) | CRO-19 | Medio | S |
| 3.7 | Newsletter: bloque de Kadence con el proveedor que elijas, doble opt-in; en el pie, al final de los artículos y en Descargas (lead magnet) | CRO-07/16 | Medio–alto | M |

### Etapa 4 — SEO técnico y schema (≈ 2–3 días)
| # | Tarea | Hallazgos | Impacto | Esfuerzo |
|---|---|---|---|---|
| 4.1 | Rank Math: títulos y metas de las 27 URLs (textos listos en `informes/seo.md`, revisados por contenidos), Open Graph con imagen 1200×630 | SEO-01/02/12 | Alto | M |
| 4.2 | JSON-LD en el mu-plugin: Organization, WebSite, Person ×3, ProfessionalService, BlogPosting, BreadcrumbList, FAQPage (solo con FAQ visibles), sin datos sin verificar | SEO-03, GEO-09 | Alto | M |
| 4.3 | URLs y redirecciones: `/entradas/` → `/blog/`; liberar el slug `descargas` (renombrar el adjunto 1839); `sobre_tatiana` → `/equipo/tatiana-x-stacul/`; canonical en archivos | SEO-04/05/06/07 | Medio | S |
| 4.4 | Usuarios reales por autora/autor (nombre, bio, foto); ocultar `admin`; noindex en archivos por fecha, etiquetas finas y la categoría vacía | SEO-09/16/17, GEO-05 | Medio | S |
| 4.5 | Rendimiento: imagen LCP con `fetchpriority` (no el logo), sin lazy en la LCP, webp/avif con dimensiones, recorte de CSS/JS (Contact Form 7 sin uso, ZoloBlocks donde no se usa), LiteSpeed con WebP. Medir con PageSpeed antes y después | SEO-18/19 | Alto | M |

Objetivo medible: LCP < 2,5 s, CLS < 0,1 e INP < 200 ms en mobile (percentil 75); 0 errores en el Rich Results Test.

### Etapa 5 — GEO y reestructuración del blog (≈ 4–5 días + trabajo editorial)
| # | Tarea | Hallazgos | Impacto | Esfuerzo |
|---|---|---|---|---|
| 5.1 | `/llms.txt` (borrador listo, 25 URLs verificadas) generado por el mu-plugin | GEO-03 | Alto | S |
| 5.2 | Taxonomía nueva: 6 categorías y etiquetas limpias, una categoría por artículo, 17 redirecciones 301 (tabla en `informes/contenidos.md`) | CRO-20, SEO-24 | Alto | M |
| 5.3 | 15 artículos: bloque «En resumen», definición citable, H2 (7 artículos no tienen), fechas "Publicado/Actualizado", caja de autora, sección Fuentes con enlaces. **El texto de la autora no se toca**: solo se agrega estructura y se corrigen errores | GEO-06/07/08/13, SEO-13/15 | Muy alto | L |
| 5.4 | Pilar "¿Qué es la ciberpsicología?" (hoy tiene unas 100 palabras y no define el término) + 2 pilares más; enlazado pilar ↔ satélites ↔ servicio | GEO-10, SEO-14 | Muy alto | L |
| 5.5 | Test accesible: tarjetas como `<button>`/radio, foco y anuncios de pantalla; preguntas en el HTML del servidor | A11Y-01/11/12, GEO-14 | Alto (fallo bloqueante) | M |
| 5.6 | Calendario editorial de 3 meses (12 temas, incluidos artículos de Francisca y Emanuel) | contenidos | Medio (largo plazo) | — |

> **Recomendación:** adelantar 5.5 (test accesible) a la Etapa 1 o 2, porque es el único fallo bloqueante de WCAG.

---

## 5. Mejoras esperadas (cualitativas, sin cifras inventadas)
- **SEO:** metas y OG en el 100 % de las URLs, un H1 por página, sin duplicados ni 404 internos, schema válido y enlazado interno por clusters → más cobertura de indexación y mejor CTR en resultados; la mejora real se mide en Search Console a 8–12 semanas.
- **GEO:** bots de IA con 200 estable, `llms.txt`, respuestas directas, fuentes enlazadas y autoría verificable → condiciones para que ChatGPT, Perplexity, Gemini y Claude citen el sitio; se verifica con consultas manuales trimestrales y en los logs.
- **Conversión:** CTA arriba en Inicio y Servicios y al final de cada artículo, formulario más corto y claro, reaseguros (qué pasa después, privacidad, urgencias) y newsletter → más consultas y un canal propio; se mide con el evento `generate_lead` (hoy no hay línea base: [COMPLETAR: herramienta de analítica]).
- **Diseño y mobile:** un solo sistema visual, sin recortes ni franjas vacías, contraste AA en todo el sitio, objetivos táctiles ≥ 44 px.

---

## 6. Qué necesito de vos para arrancar
1. **Aprobar el plan** (o ajustar prioridades y etapas).
2. **Confirmar el método de implementación** de la sección 2 (tema hijo + mu-plugin + contenido listo para pegar + staging local) y, si podés, pasarme un backup o una exportación WXR.
3. **Tareas que solo podés hacer vos, sin esperar a la Etapa 1:** revisar el firewall/antibots en hPanel (1.1) y borrar el campo "Sitio web" del usuario admin (1.4).
4. **Decisiones:** plugin SEO (Rank Math o The SEO Framework), proveedor de newsletter, modo oscuro sí/no, qué hacer con CCBot/Bytespider y con los testimonios de Luis R./Ana M.
5. **Datos:** los 47 placeholders de `docs/placeholders.md`. Los más urgentes son las fotos del equipo, la matrícula (si corresponde), honorarios o cómo mostrarlos, las líneas de ayuda y la URL de la política de privacidad.
