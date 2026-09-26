# QA — Etapa 4 (SEO técnico, datos estructurados, rendimiento)

Fecha: 26-09-2026.

## 1. Verificación en WordPress real

Entorno: WordPress 7 local (PHP 8.4 + SQLite) con Kadence, Kadence Blocks, Rank Math y el plugin `codigo-calma` 1.3.0 enlazado desde el repo. Contenido equivalente: Inicio, Servicios, Contacto, Equipo, Tatiana, Francisca, Blog y 3 entradas en 2 categorías. `WP_DEBUG` activo: **0 avisos del plugin** en `debug.log`.

| Comprobación | Resultado |
|---|---|
| `wp calma seo-import` | 11 URLs existentes actualizadas; las 23 que no existen en el entorno local se reportan "no encontrado" (sin errores) |
| Rank Math imprime los metadatos importados | ✅ `<title>` "Mentoría uno a uno: tecnología y trabajo \| Código Calma", `meta description`, `canonical`, `og:title` con el H1 |
| Un solo JSON-LD por página (Schema de Rank Math desactivado) | ✅ `script.calma-schema` |
| Tipos por página | Inicio: Organization, WebSite · Servicios: + ProfessionalService, FAQPage, BreadcrumbList · Equipo: + 3 Person · Tatiana: + Person, ProfilePage · Entrada: + Person, BlogPosting, BreadcrumbList (Inicio › Blog › Categoría › Título) |
| Placeholders dentro del JSON-LD | 0 |
| Etapas 1–3 en WordPress real | ✅ CSS y fuentes locales cargan, 0 peticiones a Google Fonts, `calma-conversion.js` en el pie, cajas de consulta correctas (Tatiana / Emanuel por `calma_cta_area` / equipo en ciberseguridad sin aviso), newsletter oculto sin formulario, ajustes en Lectura, aviso con enlace cuando hay URL de líneas de ayuda, H1 "Blog" cuando Kadence oculta el título |

Pendiente de validar en producción: validator.schema.org y la prueba de resultados enriquecidos (no hay acceso desde este entorno), Search Console y PageSpeed Insights.

## 2. Rendimiento de laboratorio (390 px, CPU 4× más lenta, mediana de 3 cargas)

Antes = producción · Después = vista previa Etapas 1–3 (`staging/preview/rendimiento.js`).

| Página | CLS | Peticiones a Google Fonts | Peticiones totales | KB transferidos | Elemento LCP |
|---|---|---|---|---|---|
| inicio | 0.262 → 0 | 3 → 0 | 38 → 34 | 867 → 835 | IMG.wp-image-2382 → H1. |
| servicios | 0 → 0 | 5 → 0 | 29 → 24 | 638 → 581 | P.cc-lead → H1. |
| blog | 0 → 0 | 3 → 0 | 29 → 27 | 751 → 736 | IMG.attachment-medium_large  → IMG.attachment-medium_large  |
| articulo | 0 → 0 | 3 → 0 | 38 → 36 | 681 → 697 | IMG.post-top-featured wp-pos → IMG.post-top-featured wp-pos |
| contacto | 0 → 0 | 4 → 0 | 34 → 30 | 696 → 662 | P.has-text-align-center wp-b → P. |

- **CLS del inicio: 0,262 → 0** (el umbral es 0,1): lo causaban el documento HTML pegado y las animaciones.
- **Google Fonts: 3–5 peticiones por página → 0**, y 2 fuentes locales precargadas.
- El LCP del inicio pasa del logo de 512 px (`wp-image-2382`) al H1 del hero; en Servicios y Contacto, al H1.
- Los tiempos de LCP no se informan como cifra: la vista previa sirve los archivos interceptando las peticiones y la simulación de red no se aplica. El LCP real se mide con PageSpeed Insights después de aplicar las etapas (guía, paso 7). El peso sigue alto por las imágenes JPG/PNG: el paso 6 (WebP/AVIF de LiteSpeed y carga diferida) es el que más lo reduce.

## 3. Mobile y accesibilidad
La Etapa 4 no cambia el diseño (solo `fetchpriority` del logo y el `<head>`). Siguen vigentes los resultados de `qa-etapa-3.md`: 0 violaciones axe, 0 contenido recortado, un H1 por página.

## Veredicto
**Aprueba**, con la validación externa (schema, Search Console, PageSpeed) pendiente de producción.
