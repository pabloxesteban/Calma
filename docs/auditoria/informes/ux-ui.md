# Auditoría UX/UI y mobile — codigocalma.com

Fecha: 26-09-2026 · Autor: subagente `ux-ui-designer` · Fase: solo diagnóstico (no se modificó nada del sitio).
Fuentes: HTML de producción (`docs/auditoria/snapshot-2026-09-26/html/`), capturas `docs/auditoria/capturas-antes/`, y mediciones nuevas con Playwright a 390 px y 1280 px sobre producción (drawer abierto, pie, recortes de viewport; capturas de trabajo en el scratchpad, no versionadas).

## 1. Resumen ejecutivo

1. **El 70 % de los bugs visuales tienen 3 causas raíz, no 20:** (a) un documento HTML completo pegado en un bloque HTML personalizado de **Inicio** con CSS global (`body{padding:40px;font-family:"Segoe UI"}`) que encoge todo el sitio en esa página; (b) CSS inline de **Servicios** cuyo reset `.cc li{padding:0}` / `.cc p{margin:0}` pisa a `.cc-step{padding:26px}` y a todos los márgenes; (c) dos plantillas de Kadence mezcladas (9 páginas "boxed" con franjas grises y blancas y 3 "fullwidth").
2. El **"menú negro"** no es un header distinto: el header es blanco y el mismo en todas las plantillas. Lo negro es el **drawer mobile de Kadence** (`#mobile-drawer .drawer-inner` = `#090c10`, valor por defecto sin personalizar) más la búsqueda (`rgba(9,12,16,.97)`) y el pie (`#0f172a`). Conviven 4 oscuros distintos (#090c10, #0f172a, #14276D, #1B2A4A).
3. **Tipografía y color fragmentados:** 6 familias en uso (Lora, Inter, Jost, Sora, Playfair Display, Segoe UI/Roboto de sistema), H1 fijo de 42 px con line-height 1,5 en mobile, y el color de botón global de Kadence (`#fff` sobre `#64b2e5` = 2,32:1) hace fallar **todos** los botones del sitio, no solo el de Inicio.
4. Faltan piezas de confianza: el pie tiene solo 2 íconos + ©, no hay fotos de Francisca ni Emanuel en ningún lado, y la foto de Tatiana no tiene `alt`.
5. Recomendación: tema hijo de Kadence con un archivo de tokens mapeado a `--global-palette*` + ajustes del Customizer (drawer, pie, layout) + **3 intervenciones puntuales de contenido** (quitar el HTML pegado en Inicio, reemplazar el CSS inline de Servicios y Herramientas, desactivar animaciones de entrada). Ojo: el prefijo `.cc-*` del design system **ya está usado** por el CSS inline de Servicios y Herramientas; hay que eliminar ese CSS antes de cargar el global.

## 2. Causas raíz (evidencia)

### CR-1 · Documento HTML pegado dentro de Inicio (page-id 1204)
Entre el bloque de filas y `kb-row-layout-id1204_7ce0f7-d0` hay un bloque HTML personalizado con `<html><head><meta charset><title><style>…</style></head><body><h1>Línea de tiempo…</h1><p class="sub">…<section class="timeline">…</body></html>` (en `home.html`, ~offset 98 800–157 000). Su `<style>` no está acotado:
```css
body { margin:0; padding:40px; background:#f7f7fb; font-family:"Segoe UI",sans-serif; color:#2f3440; }
h1 { margin-bottom:6px; font-weight:600; }
```
Efectos medidos: a 390 px `#masthead`, `main` y `#colophon` quedan en x = 40…350 (medido: `header {l:40, r:40, w:310}`); `.wp-site-blocks` (overflow: clip) recorta lo que sale de ese ancho (títulos de tarjetas del blog, columnas animadas); en 1280 px todo el sitio aparece "enmarcado" con 40 px lavanda-gris; el cuerpo y el título del sitio pasan a Segoe UI/Arial (en Linux/Android se ve la fuente de sistema: el logo "Código Calma" cambia de fuente solo en Inicio). Es también la **"línea de tiempo suelta"**: H1 de 42 px + tarjeta blanca sin relación visual con el resto.

### CR-2 · CSS inline de Servicios (page-id 1741) con especificidad invertida
Hay **dos** bloques `<style>` dentro del contenido: `.cc-servicios{…}` (código muerto: ningún elemento usa esa clase) y `.cc{…}` (el activo, contenedor `.cc-full-container > .cc`). El reset del segundo:
```css
.cc p, .cc ul, .cc ol, .cc li, .cc h2, .cc h3 { margin:0; padding:0; }   /* especificidad 0,1,1 */
.cc a { color: inherit; }                                                  /* 0,1,1 */
```
gana sobre las reglas de componente (0,1,0): `.cc-step{padding:26px}` → las `<li class="cc-step">` quedan **sin padding** y el círculo `.cc-step-n` toca el borde; `.cc-lead{margin-top:16px}`, `.cc-h1{margin-top:18px}`, `.cc-facts{margin:26px auto 0}`, `.cc-steps{margin:32px auto 0}` se anulan (títulos, bajadas y listas pegados); `.cc-cta{color:#0F172A}` se vuelve `#334155` heredado (4,46:1 sobre `#64B2E5`, apenas bajo 4,5). Además carga **Sora** desde Google Fonts (4.ª familia).

### CR-3 · Dos plantillas de página de Kadence
- `content-width-fullwidth content-style-unboxed content-vertical-padding-hide`: Inicio, Contacto, Sobre Tatiana.
- `content-width-normal content-style-boxed content-vertical-padding-show`: Servicios, Blog, Ciberpsicología, Testimonios, Test, Descargas, Herramientas, Bienestar digital, artículos (`content-width-narrow`).

En las "boxed", a 390 px: `.content-area{margin:2rem 0}` (franja gris `#f8fafc` de 32 px) + `.entry-content-wrap{padding:1.5rem}` (franja blanca de 24 px) + filas `alignfull` con fondo propio (`has-theme-palette8-background-color`) → **56 px de franjas arriba y abajo** del contenido (visible en Servicios, Ciberpsicología, Testimonios, Test, Descargas, Herramientas, Bienestar). En desktop sube a 80 + 32 px. Es la causa de las "franjas blancas vacías arriba del contenido y antes del pie".

## 3. Tabla de hallazgos

Impacto: A alto · M medio · B bajo. Esfuerzo: S < 2 h · M ½–1 día · L > 1 día.

| ID | Página | Problema | Evidencia (selector / clase / origen) | Imp. | Esf. | Solución propuesta |
|---|---|---|---|---|---|---|
| UX-01 | Inicio (afecta header, pie y todo el layout) | Sitio encogido 40 px por lado, recorte de títulos de tarjetas, fuente del cuerpo cambiada a Segoe UI | Bloque HTML personalizado con documento completo; `body{padding:40px}` y `h1{}` globales (CR-1) | A | S | Eliminar el bloque HTML; si se quiere conservar la línea de tiempo, rehacerla como bloque/patrón con CSS acotado a `.cc-timeline` en el tema hijo |
| UX-02 | Inicio | Línea de tiempo "suelta" antes del cierre: H1 duplicado (2.º H1 de la página), estilo ajeno (Segoe, sombra fuerte, colores `--calma-*` propios) | `<h1>Línea de tiempo…</h1>`, `section.timeline`, `.event::before` | M | M | Decidir con contenidos si se queda; si se queda: H2, componente `.cc-timeline` con tokens, ubicada junto a "Bienvenidos" o en Ciberpsicología |
| UX-03 | Inicio 390 px | H2 "Bienvenidos a Código Calma" y párrafo en x = −49 px; estadísticas "74 %+" fuera de cuadro | Columnas con `animated fadeInLeft/Right` (plugin Blocks Animation) → `transform: translateX(-74px)` + `.wp-site-blocks{overflow:clip}`; custom CSS `.kb-row-layout-id1204_239f87-24 .change{position:absolute;width:457px;left:-168px}` (≤1024: `left:-50px`) | A | S | Quitar animaciones de entrada en columnas con texto; CSS global `@media (prefers-reduced-motion:reduce)` y, en mobile, `.animated{animation:none!important;transform:none!important}`; revisar `.change` (ancho fijo 457 px) |
| UX-04 | Inicio, Sobre, Herramientas, Descargas | Contenido invisible hasta que el observador de scroll lo activa: con scroll rápido o salto al final se ven bloques en blanco (p. ej. Herramientas: ~1 100 px vacíos antes del aviso final; Sobre: testimonios a media opacidad) | `.animated:not(.o-anim-ready){visibility:hidden}` (estilo `o-anim-hide-inline-css`); fila `kb-row-layout-id1618_d7de32-ac … animated fadeIn slower`; 12 elementos `.animated` en Inicio | A | S | Desactivar Blocks Animation en contenido (o limitar a `opacity` ≤ 300 ms sin `visibility:hidden`); nunca ocultar contenido por defecto |
| UX-05 | Inicio (bloque final) | Tres tarjetas "Test / Solicitar una consulta / Recursos gratuitos" aparecen cortadas a los lados y lavadas; franja vacía antes del pie | `kb-row-layout-id1204_6c7f8b-e0` (3 columnas `fadeInLeft/Right slower`, `margin-bottom:50px`) + fila vacía `kb-row-layout-id1204_addcaa-c1` (48 px, sin texto) + `<p>` vacío final | A | S | Quitar animación; eliminar fila vacía y `<p>` vacío; separación con `--cc-section-y` |
| UX-06 | Global (mobile) | "Menú negro": drawer mobile casi negro, sin logo ni CTA, contrasta con el resto claro/lavanda | `#mobile-drawer .drawer-inner` bg `rgb(9,12,16)` (default Kadence); `.mobile-navigation ul li > a{color:var(--global-palette8)}`; `#search-drawer .drawer-inner{background:rgba(9,12,16,.97)}` | A | S | Customizer › Header › Mobile/Off-Canvas: fondo `--cc-surface`, texto `--cc-text`, activo `--cc-primary`, separadores `--cc-border`; agregar botón "Solicitar una consulta" (`.cc-btn--primary`) y logo en el drawer; búsqueda con fondo `--cc-navy` o claro |
| UX-07 | Global | Cuatro oscuros distintos compitiendo | Drawer `#090c10`, pie `#0f172a` (palette3), CTA Servicios `#14276D` (`--cc-deep`), Herramientas `#1B2A4A` | M | S | Un solo `--cc-navy #16214d` para pie y bloques CTA; drawer claro |
| UX-08 | Servicios | Tarjetas de pasos sin padding; número sobre el borde; textos pegados al borde | `.cc li{padding:0}` (0,1,1) pisa `.cc-step{padding:26px}` (0,1,0) (CR-2) | A | S | Retirar el CSS inline y usar `.cc-step` del design system (número dentro del padding, grid `auto 1fr`) |
| UX-09 | Servicios | Márgenes verticales anulados: badge, H1, bajada, pills y secciones sin respiro | `.cc p,.cc ul,.cc h2{margin:0}` pisa `.cc-lead`, `.cc-h1`, `.cc-facts`, `.cc-steps`, `.cc-note` | M | S | Mismo arreglo que UX-08; ritmo vertical con tokens `--cc-space-*` |
| UX-10 | Servicios | CSS duplicado/muerto y fuente extra | Bloque `.cc-servicios{…}` sin uso; `<link>` a Sora; clases `.cc-btn`, `.cc-card`, `.cc-badge`, `.cc-final` definidas 2 veces | M | S | Eliminar ambos `<style>` inline y el `<link>` de Sora al migrar |
| UX-11 | Servicios y 8 páginas "boxed" | Franjas gris + blanca (≈ 56 px mobile, ≈ 112 px desktop) arriba del contenido y antes del pie | CR-3: `.content-area{margin-top/bottom:2rem}`, `.entry-content-wrap{padding:1.5rem}`, `body.content-style-boxed`, filas `alignfull` con fondo propio | A | S | Unificar todas las páginas a `fullwidth + unboxed + vertical-padding-hide` (Customizer › Page Layout, y en cada página "Page Settings"); artículos quedan `narrow` pero sin caja; secciones controlan su propio `padding-block` |
| UX-12 | Servicios | Rompe-contenedor `100vw` dentro de la caja | `.cc-full-container{width:100vw;left:50%;margin-left:-50vw}` dentro de `.content-style-boxed` | B | S | Innecesario con UX-11; usar fila `alignfull` |
| UX-13 | Global | Botón primario con contraste insuficiente en todo el sitio (no solo Inicio) | `--global-palette-btn-bg: var(--global-palette1)` (#64b2e5) + `--global-palette-btn:#fff` → 2,32:1 ("Solicitar una consulta", "Recursos gratuitos", "Descargar", "Más testimonios"); Servicios `#334155` sobre `#64B2E5` = 4,46:1 | A | S | Tokens: `--global-palette-btn-bg:#1d5f94` (6,74:1 con blanco), hover `#174d78`; `.cc-btn--on-dark` (blanco/navy) en bloques oscuros |
| UX-14 | Global | Texto pequeño en `#64b2e5` ilegible | Menú activo `.current-menu-item > a{color:var(--global-palette1)}`, etiquetas de categoría (`.entry-taxonomies a`), "Ver testimonio completo" en Testimonios, `.cc-eyebrow` de Herramientas `#4ECDC4` (1,93:1) | A | S | `--global-palette1` pasa a ser `--cc-primary #1d5f94` para texto; `#64b2e5` queda como `--cc-accent` decorativo (mapear a otra ranura de paleta) |
| UX-15 | Global | Tipografía: 6 familias; cuerpo en Lora serif 19 px y títulos en Inter (al revés que el design system); Inter solo cargado en 700–900 pero usado en 400 (negrita sintética) | `--global-body-font-family:Lora`, `--global-heading-font-family:Inter`; botones `font-family:Jost`; Sora (Servicios), Playfair Display (Herramientas), Segoe UI (Inicio), Roboto (Test) | M | M | 2 familias locales (Lora títulos, Inter cuerpo/UI), `font-display:swap`; quitar Jost, Sora, Playfair |
| UX-16 | Global mobile | Escala tipográfica sin versión mobile: H1 42 px, H2 36 px, H3 32 px con `line-height:1.5`; títulos de 5–6 líneas (Test, artículos, tarjetas del blog) | `kadence-global-inline-css`: `h1{font-size:42px;line-height:1.5}`, `h2{36px}`, `h3{32px}`, sin media queries | A | S | Escala fluida `--cc-fs-*` (H1 30→48, H2 24→36), `--cc-lh-heading:1.2`; mapear en Customizer › Typography (tamaños por dispositivo) o en tokens |
| UX-17 | Global | Pie casi vacío: solo LinkedIn, correo y © | `#colophon` una sola fila `.site-top-footer-wrap` con `.footer-social-wrap` + `.footer-html`; íconos 38×38 px | A | M | Pie de 4 columnas según design system (marca, navegación, recursos, contacto) + fila legal con aviso "no es un servicio de urgencias" y privacidad; íconos ≥ 44 px |
| UX-18 | Sobre, Servicios | Sin fotos del equipo: Francisca Cortés Santoro y Emanuel C. Franco no tienen foto; la de Tatiana (`efe-e1786203233715.png`) no tiene `alt` y en mobile aparece recién después de todo el texto | `sobre_tatiana.html` `<img … alt="">`; `article.cc-person` en Servicios sin imagen | A | M | Componente "persona" con foto 1:1 (`width/height`, webp) arriba del nombre; `[COMPLETAR: foto de Francisca Cortés Santoro]`, `[COMPLETAR: foto de Emanuel C. Franco]`; alt descriptivo; en mobile foto primero |
| UX-19 | Sobre Tatiana | Texto largo centrado en mobile (bio con listas centradas) | Encabezados avanzados `kt-adv-heading946_79a33d-59` con `text-align:center` | M | S | Alinear a la izquierda el texto corrido > 2 líneas; medida `--cc-measure` |
| UX-20 | Contacto | Formulario con etiquetas en inglés ("Name", "Email", "Message") de 12 px dentro del borde; es Kadence Advanced Form, no Contact Form 7 | `label.kb-adv-form-label`; bloque `kb-adv-form` | A | S | Etiquetas en español ≥ 16 px encima del campo, `min-height:48px`, foco `--cc-primary`; confirmar con CRO qué plugin se conserva |
| UX-21 | Herramientas | Texto demasiado pequeño y fino: cuerpo 13,5 px peso 300, eyebrow 10 px; slider horizontal sin indicios claros en mobile | `.cc-wrap` inline: `.cc-card-body{font-size:13.5px;font-weight:300}`, `.cc-eyebrow{font-size:10px}`, `.cc-slider{overflow-x:auto;scrollbar-width:none}`; reset `.cc-wrap *{margin:0;padding:0}` | M | S | Migrar a tarjetas del design system (cuerpo ≥ 16 px); en mobile apilar tarjetas en vez de slider |
| UX-22 | Ciberpsicología | Resaltado con fondo `#64b2e5` detrás de texto de 36 px: aspecto de selección de texto | `<mark style="background-color:var(--global-palette1)">` y `var(--global-palette7)` | B | S | Reemplazar por cita destacada (`.cc-card` + borde izquierdo `--cc-accent`) |
| UX-23 | Blog | Listado de 11 400 px a 390 px: una entrada por pantalla con título de 36 px, "Leer más" de 19 px de alto; imágenes de stock con alt en inglés | `.loop-entry`, `h2.entry-title`, `a.post-more-link` (105×19); categorías `a.category-link-*` 17 px de alto | M | M | Grilla de tarjetas (imagen 16:9, badge de categoría, H3 `--cc-fs-lg`, extracto 2–3 líneas, toda la tarjeta clicable ≥ 44 px) |
| UX-24 | Global mobile | Áreas táctiles < 44 px | Botón menú `.menu-toggle-open` 37×31; íconos del pie 38×38; categorías/autor 17–19 px | M | S | `min-block-size:44px` en toggle y pie; padding vertical en enlaces de metadatos |
| UX-25 | Global (navegación) | En el drawer, Blog, Test, Descargas, Herramientas y Bienestar quedan escondidos dentro del submenú "Ciberpsicología"; no hay CTA en el header desktop | Menú primario: `Inicio · Ciberpsicología ▾ · Servicios · Sobre Tatiana · Contacto` | M | S | Proponer a CRO/IA: "Recursos ▾" (Blog, Test, Descargas, Herramientas) + botón "Solicitar una consulta" en el header |
| UX-26 | Global | Header de 92 px con logo de 80 px; en Inicio el título del sitio se parte en 2 líneas a 390 px | `.site-main-header-inner-wrap{min-height:92px}`, `.site-branding a.brand img{max-width:80px}` | B | S | Mobile: logo 48 px, header 64 px; título en una línea |
| UX-27 | Descargas | Portadas y textos en inglés ("The Psychology of Trust"), H3 con nombre de archivo ("Ansiedad-Funcional-vs-Ans…") | `h3.kt-adv-heading1666_29dc57-d9` | B | S | Títulos legibles (derivar a contenidos); tarjeta de descarga del design system |
| UX-28 | Global | Clases `.cc-*` ya usadas por CSS inline (Servicios: `.cc-btn`, `.cc-card`, `.cc-step`, `.cc-badge`; Herramientas: `.cc-wrap`, `.cc-card`, `.cc-dot`) chocan con los componentes del design system | `<style>` dentro del contenido de páginas 1741 y 1618 | A (riesgo de implementación) | S | Etapa 0: eliminar esos `<style>` antes de encolar `cc-design-system.css` |

## 4. Recomendación de implementación técnica

**Enfoque: tema hijo de Kadence con tokens + Customizer, y solo 4 ediciones de contenido acotadas.** No editar bloque por bloque para estilos: casi todo el color, la tipografía y el espaciado de Kadence Blocks sale de `--global-palette*` y de las variables `--global-kb-*`, así que reasignarlas arregla el sitio entero sin tocar las páginas.

1. **Tema hijo** `kadence-child` con `assets/css/cc-design-system.css` encolado después de `kadence-global` (dependencia `kadence-global`), baja especificidad (`:where()` para los resets) y `!important` solo donde haya estilos inline de bloque, documentado.
2. **Mapear tokens a la paleta de Kadence** (en el Customizer y también en `:root` del hijo, para que no dependa de la base de datos):
   - `--global-palette1` → `#1d5f94` (primario: texto/enlaces/botones); `--global-palette2` → `#174d78` (hover).
   - `--global-palette12` (o una libre) → `#64b2e5` como acento decorativo; revisar bloques que usen `palette1` como fondo de sección.
   - `--global-palette3` → `#0f172a` texto; pie y CTA con `--cc-navy #16214d`.
   - `--global-palette7` lavanda y `--global-palette8` `#f8fafc` se mantienen.
   - Tipografía: `--global-heading-font-family: Lora`, `--global-body-font-family: Inter`, botones sin Jost; fuentes locales (woff2) y desactivar Google Fonts en Kadence (Customizer › General › Performance › "Load Google Fonts Locally").
3. **Customizer (sin código):** layout de páginas `fullwidth / unboxed / vertical padding off` por defecto y en las 9 páginas "boxed" (UX-11); drawer mobile claro (UX-06); constructor de pie con 4 columnas + fila legal (UX-17); tamaños de encabezados por dispositivo (UX-16); header mobile 64 px (UX-26).
4. **Ediciones de contenido imprescindibles** (no se resuelven con CSS global sin hacks):
   - Inicio: borrar el bloque HTML con `<html><body>` (UX-01/02), la fila vacía `1204_addcaa-c1` y el `<p>` vacío (UX-05).
   - Servicios y Herramientas: quitar los `<style>` y `<link>` inline; el marcado `.cc-step`, `.cc-person`, `.cc-final` puede quedarse y heredar los componentes globales (UX-08/09/10/21/28).
   - Desactivar Blocks Animation en filas/columnas con texto (UX-03/04/05); si el cliente quiere movimiento, solo `opacity` dentro de `prefers-reduced-motion: no-preference`.
   - Sobre/Servicios: agregar fotos del equipo cuando existan (UX-18) — hasta entonces `[COMPLETAR]` visible.
5. **Orden sugerido:** Etapa 0 (limpieza de contenido, 2–3 h) → Etapa 1 (tema hijo + tokens + Customizer, 1 día) → Etapa 2 (componentes: pie, persona, tarjetas del blog, formulario, 1–2 días) → QA con `mobile-qa` en 360/390/430/1280 y revisión de `accessibility-qa`.

**Por qué no editar bloques uno por uno:** hay ~40 filas con CSS generado por ID (`kb-row-layout-id…`) y un bloque sincronizado (ID 1580) reutilizado en Inicio; editar cada una duplica valores y vuelve a divergir. Los tokens resuelven contraste, tipografía y color en un solo lugar; las ediciones de contenido se limitan a quitar lo que rompe el layout.

## 5. Placeholders a registrar en `docs/placeholders.md`
- `[COMPLETAR: foto de Francisca Cortés Santoro, 1:1, mín. 800 px]`
- `[COMPLETAR: foto de Emanuel C. Franco, 1:1, mín. 800 px]`
- `[COMPLETAR: texto alternativo de la foto de Tatiana X. Stacul]`
- `[COMPLETAR: logo en SVG para header y pie]` (hoy PNG `cropped-logo512-1.png` a 80 px)

## 6. Criterios de verificación (después de implementar)
`overflowX = 0`, sin elementos con `left < 0` (incluye esperar o desactivar animaciones), margen lateral ≥ 20 px, `.cc-step` con padding ≥ 20 px, ninguna franja vacía > 48 px antes del contenido o del pie, botón primario ≥ 4,5:1 y ≥ 48 px de alto, drawer y pie con los mismos tokens en todas las plantillas (página, entrada, archivo, búsqueda, 404), máximo 2 familias tipográficas en la pestaña Network.
