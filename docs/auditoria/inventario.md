# Fase 0 — Diagnóstico e inventario de codigocalma.com

Fecha: 26-09-2026 · Fuente: sitio en producción (solo lectura) · Rama: `claude/focused-babbage-403shx`

## Hallazgo estructural: el repositorio no contiene el sitio
El repositorio `pabloxesteban/Calma` estaba **vacío** (sin commits). El sitio vive en un WordPress administrado en Hostinger, sin código versionado. Todo este diagnóstico se hizo sobre el sitio público y la API REST de WordPress; el snapshot quedó en `snapshot-2026-09-26/` como línea base.

## Stack detectado
| Capa | Detalle | Evidencia |
|---|---|---|
| CMS | WordPress 7.1.2, PHP 8.3 | `<meta name="generator">`, header `x-powered-by` |
| Hosting / CDN | Hostinger (hPanel) + CDN `hcdn` | headers `platform: hostinger`, `server: hcdn` |
| Caché | LiteSpeed Cache | header `x-litespeed-cache`, namespace `litespeed/v3` |
| Tema | Kadence (sin tema hijo detectado) | `wp-content/themes/kadence` |
| Bloques | Kadence Blocks (+ Pro: `kbp/v1`), ZoloBlocks, Blocks Animation | rutas de plugins en HTML |
| Formularios | Formulario de Kadence Blocks (`kb-adv-form-2625`) en /contacto/; Contact Form 7 instalado y cargado pero **sin uso** | `contact-form-7/v1`, HTML de /contacto/ |
| Compartir | AddToAny | |
| Email marketing | Integraciones de Kadence disponibles (MailerLite, FluentCRM, GetResponse) **sin uso visible** | namespaces `kb-mailerlite`, `kb-fluentcrm`, `kb-getresponse` |
| SEO | **Ninguno** (sin meta description, OG ni JSON-LD); sitemap nativo `wp-sitemap.xml` | |
| Fuentes | Google Fonts externas: Lora, Inter, Jost | `fonts.googleapis.com` |

## robots.txt actual
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Sitemap: https://codigocalma.com/wp-sitemap.xml
```
Es permisivo. Desde este entorno, peticiones con user-agent GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot y Googlebot devolvieron 200 con idéntico contenido. Si hay bloqueo de IA, es probable que esté en la capa de Hostinger (bloqueo por IP/firma de bots), no en robots.txt → ver `informes/geo.md`. `/llms.txt` → 404.

## Páginas (12)
| ID | Slug | Título | Observaciones |
|---|---|---|---|
| 1204 | `/` | Inicio | 2 H1; hero con animación que desplaza texto fuera de pantalla en mobile; "6M+"; línea de tiempo suelta al final |
| 1741 | `/servicios/` | Servicios | sin H1; tarjetas de pasos sin padding; "el día a day" |
| 790 | `/contacto/` | Contacto | sin H1; formulario Kadence con labels en inglés |
| 946 | `/sobre_tatiana/` | Sobre Tatiana | slug con guion bajo; única página de equipo |
| 1638 | `/ciberpsicologia/` | Ciberpsicología | candidata a pilar |
| 1604 | `/bienestar-digital/` | Bienestar digital | 3 H1 |
| 1618 | `/herramientas/` | Herramientas | |
| 1941 | `/test/` | Test de consumo digital | lead magnet potencial |
| 1666 | `/descargas-2/` | Descargas | slug con `-2`; sin H1 |
| 1787 | `/testimonios/` | Testimonios | sin H1; 4 imágenes sin dimensiones |
| 1410 | `/blog/` | Blog | sin H1 ni canonical |
| 2337 | `/entradas/` | Entradas | posible duplicado de `/blog/` |

## Plantillas en uso (Kadence)
Portada estática (página), página, entrada individual, archivo de categoría/etiqueta, archivo de autor (`/author/admin/`), búsqueda, 404. Ninguna página usa plantilla personalizada (`template: ""`); los diseños están armados con bloques dentro del contenido de cada página, con estilos inline por bloque (`kt-adv-heading1204_…`, `kadence-column1204_…`). **Consecuencia:** unificar el estilo exige una capa global de CSS (tema hijo) que normalice los bloques, más ajustes puntuales en el editor.

## Estilos
- Paleta global Kadence: `#64b2e5` (1), `#4f86c6` (2), `#0f172a` (3), `#1f2937` (4), `#334155` (5), `#64748b` (6), `#dad4f6` lavanda (7), `#f8fafc` (8), `#ffffff` (9) + acentos 11–15.
- Tres familias tipográficas desde Google Fonts.
- Dos lenguajes visuales conviven (header/menú oscuro vs. páginas claras/lavanda), estilos inline por bloque y CSS de 3 plugins de bloques.

## Artículos (15) y taxonomía actual
| Fecha | Artículo | Categorías | Etiquetas |
|---|---|---|---|
| 2026-07-19 | Por qué tu fuerza de voluntad es más lista de lo que crees | Psicología | — |
| 2026-07-19 | La diferencia entre «querer» y «ser capaz»: autoeficacia | Psicología | — |
| 2026-06-30 | ¿Por qué fallamos al intentar cambiar conductas? | **Ciberseguridad** ⚠️ | — |
| 2026-06-04 | IA y apoyo emocional: saber la **autoria** ⚠️… | Ciberpsicología | — |
| 2026-05-13 | El estigma de la estructura: «X entonces Y» | Neurociencia y tecnología | — |
| 2026-05-13 | Infancias «Figitales» | Bienestar digital, Ciberpsicología | Ciberpsicología, Salud mental |
| 2026-05-06 | Calidad vs. Cantidad: la hipótesis de Ricitos de Oro | Bienestar digital, Ciberpsicología | Ciberpsicología, Salud mental |
| 2026-05-06 | Autoevaluación del consumo digital | Bienestar digital, Ciberpsicología | Ciberpsicología, Consumo digital, Salud mental |
| 2026-05-06 | Preguntas clave para entender y cuidar nuestro cerebro | Neurociencia y tecnología | Ciberpsicología, Mindfulness digital, Salud mental |
| 2026-05-06 | 5 puntos clave que el caso de Meta nos deja en salud mental | Neurociencia y tecnología | Ciberpsicología, Redes sociales, Salud mental |
| 2026-05-06 | Reflexiones éticas sobre el desarrollo de la IA | Ciberpsicología, Neurociencia y tecnología | Ciberpsicología, IA, Neurociencias, Tecnología |
| 2026-05-05 | ¿Qué modela nuestro comportamiento? | Bienestar digital | Ciberpsicología, Mindfulness digital |
| 2026-05-05 | La tecnología te supera: tecnoestrés | Bienestar digital, Ciberpsicología | Ciberpsicología, Salud mental, Tecnoestrés |
| 2025-02-12 | El arte de rediseñar tu entorno | Bienestar digital, Ciberpsicología | — |
| 2024-03-09 | Cómo un «Te quiero» infectó 45 millones de computadoras | Ciberseguridad | Ciberseguridad, Transformación digital |

Categorías: Bienestar digital (6), Ciberpsicología (7), Ciberseguridad (2), Neurociencia y tecnología (4), Psicología (2), Sin categoría (0).
Etiquetas: 15, de las cuales 4 sin uso (Awareness humano, Liderazgo consciente, Neuroplasticidad, Terapia Online). "Ciberpsicología" duplica categoría y etiqueta. Autor de todas las entradas: usuario `admin` (se muestra "Tatiana X. Stacul").

## Señales SEO por URL (resumen)
- 0/28 URLs con meta description, Open Graph o JSON-LD.
- Sin canonical: `/blog/`, archivos de categoría.
- Sin H1: servicios, contacto, blog, descargas, entradas, testimonios. Con varios H1: inicio (2), bienestar-digital (3).
- 0 imágenes en webp/avif.

## Métricas mobile de línea base (`capturas-antes/metricas.json`)
- Sin scroll horizontal medible (el sitio recorta con `overflow: clip` en `.wp-site-blocks`), **pero hay contenido recortado**: en inicio a 390 px el H2 de bienvenida arranca en x = −49 px y los títulos de las tarjetas de blog se cortan.
- Contraste CTA "Solicitar una consulta": inicio 2,32:1 ❌ (blanco sobre `#64b2e5`); servicios 4,46:1 (límite, borde del mismo color que el fondo).
- Objetivos táctiles < 44 px: inicio 17, blog 37, testimonios 18, artículo 13.

## Errores de texto confirmados
| Dónde | Actual | Corrección |
|---|---|---|
| Inicio (contador) | 6M+ / "Más de 6 mil millones…" | "+6.000 M" o "6 mil millones+" (M = millones; 6M = 6 millones) |
| Título de artículo y listados | saber la autoria, cambia tu perspectiva | saber la autoría cambia tu perspectiva (tilde y sin coma entre sujeto y verbo) |
| Servicios | Normativa y procesos que no traben el día a day | …que no traben el día a día |
Lista ampliada en `informes/cro-copy.md`.
